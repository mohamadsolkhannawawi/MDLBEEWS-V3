import os
from obspy.clients.seedlink.easyseedlink import EasySeedLinkClient
from kafka import KafkaProducer
import json
import time
import concurrent.futures
import threading

# --- Prometheus Metrics (imported from main.py module-level) ---
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"

if ENABLE_METRICS:
    from prometheus_client import Counter, Gauge
    TRACES_SENT = Counter(
        'data_provider_traces_sent_total',
        'Total number of trace messages sent to Kafka',
        ['topic']
    )
    PUBLISH_ERRORS = Counter(
        'data_provider_publish_errors_total',
        'Total number of Kafka publish errors'
    )
    ACTIVE_STREAMS = Gauge(
        'data_provider_active_streams',
        'Number of active SeedLink streams'
    )
else:
    TRACES_SENT = None
    PUBLISH_ERRORS = None
    ACTIVE_STREAMS = None


class SeedlinkClient(EasySeedLinkClient):
    """
    Custom SeedLink client that ingests seismic data and publishes to Kafka.
    Instrumented with Prometheus Counter and Gauge metrics.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_servers = os.getenv("KAFKA_BROKERS", "kafka1:9092,kafka2:9093").split(",")
        bootstrap_servers_pwave = os.getenv("KAFKA_BROKERS_PWAVE", "kafka3:9094").split(",")

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: json.dumps(v).encode('utf-8'),
        )
        self.producer2 = KafkaProducer(
            bootstrap_servers=bootstrap_servers_pwave,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: json.dumps(v).encode('utf-8'),
        )

        self.data_station_channel = {}

    def down_sampling(self, trace):
        """Down-sample trace to 20 Hz if sampling rate is higher."""
        if trace.stats.sampling_rate > 20:
            before_sampling_rate = trace.stats.sampling_rate
            trace.interpolate(sampling_rate=20)
            after_sampling_rate = trace.stats.sampling_rate
            print(f"Down sampling {trace.stats.station}\t{trace.stats.channel} : {before_sampling_rate} -> {after_sampling_rate}")
        return trace

    def log_data(self, data, type="LOG", stat="-"):
        print(f"[+] <{stat}> <{type}>  {data}")

    def on_send_success(self, record_metadata):
        pass

    def on_send_error(self, excp):
        print(f"I am an errback {excp}")
        if ENABLE_METRICS and PUBLISH_ERRORS:
            PUBLISH_ERRORS.inc()

    def calculate_gap_time(self, trace):
        key = f"{trace.stats.station}-{trace.stats.channel}"
        if key in self.data_station_channel:
            gap = trace.stats.starttime - self.data_station_channel[key].stats.endtime
            if gap > trace.stats.delta * 2:
                print(f"[{trace.stats.station}-{trace.stats.channel}]\tDelta: {trace.stats.delta}\tGap : {gap}\tDelay : {time.time() - trace.stats.endtime.timestamp}")
            self.data_station_channel[key] = trace
        else:
            self.data_station_channel[key] = trace

    def send_to_kafka(self, trace):
        """Serialize trace data and publish to Kafka topics."""
        if time.time() - trace.stats.endtime.timestamp > 60:
            return

        data = {
            'network': trace.stats.network,
            'station': trace.stats.station,
            'location': trace.stats.location,
            'channel': trace.stats.channel,
            'start_time': trace.stats.starttime.timestamp,
            'end_time': trace.stats.endtime.timestamp,
            'sampling_rate': trace.stats.sampling_rate,
            'delta': trace.stats.delta,
            'npts': trace.stats.npts,
            'calib': trace.stats.calib,
            'data_quality': trace.stats.dataquality,
            'num_samples': trace.stats.numsamples,
            'sample_cnt': trace.stats.samplecnt,
            'sample_type': trace.stats.sampletype,
            'data_provider_time': time.time(),
            'data': trace.data.tolist()
        }

        topic_trace = os.getenv("KAFKA_TOPIC_TRACE", "trace_topic")
        topic_pwave = os.getenv("KAFKA_TOPIC_PWAVE", "p_wave_topic")

        try:
            self.producer.send(
                topic_trace, data, key=f"{data['station']}-{data['channel']}"
            ).add_callback(self.on_send_success).add_errback(self.on_send_error)
            self.producer.flush()

            if ENABLE_METRICS and TRACES_SENT:
                TRACES_SENT.labels(topic=topic_trace).inc()

            if trace.stats.channel.endswith('Z'):
                self.producer2.send(
                    topic_pwave, data, key=f"{data['station']}-{data['channel']}"
                ).add_callback(self.on_send_success).add_errback(self.on_send_error)
                self.producer2.flush()

                if ENABLE_METRICS and TRACES_SENT:
                    TRACES_SENT.labels(topic=topic_pwave).inc()

        except Exception as e:
            print(f"Error sending to Kafka: {e}")
            if ENABLE_METRICS and PUBLISH_ERRORS:
                PUBLISH_ERRORS.inc()

        print(f"Delay {data['station']}\t{data['channel']} : {time.time() - trace.stats.endtime.timestamp}")
        data = None

    def on_data(self, trace):
        self.send_to_kafka(trace)

    def on_seedlink_error(self):
        print('Seedlink error')

    def on_terminate(self):
        print('Terminating')


def run_client(server, station_configs, process_id):
    """Run a SeedLink client process for a subset of station configurations."""
    client = SeedlinkClient(server)

    if ENABLE_METRICS and ACTIVE_STREAMS:
        ACTIVE_STREAMS.inc(len(station_configs))

    for config in station_configs:
        client.select_stream(config['network'], config['station'], config['seedname'])
    print('Run client', process_id, 'with', len(station_configs), 'station configs finished')
    client.run()