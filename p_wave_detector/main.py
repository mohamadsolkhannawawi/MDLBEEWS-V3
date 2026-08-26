"""
P-Wave Detector — Kafka Consumer Mode
Consumes seismic traces from p_wave_topic, detects P-wave onset using deep learning,
and publishes detection results to loc_mag_topic.

Instrumented with Prometheus metrics: Counter, Gauge, Histogram.
"""

import sys
import os
import json
import threading
from time import sleep, time
from typing import Dict, Any

import obspy
import numpy as np
import tensorflow as tf

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import (
    ENABLE_METRICS,
    METRICS_PORT_PWAVE_DETECTOR,
    KAFKA_BROKERS,
    KAFKA_BROKERS_PWAVE,
    KAFKA_TOPIC_PWAVE,
    KAFKA_TOPIC_LOCMAG
)
from utils.kafka_helper import create_topic_if_not_exists, get_consumer, get_producer
from utils.logger import get_logger

logger = get_logger("PWaveDetector")

# =============================================================================
# Prometheus Metrics
# =============================================================================
if ENABLE_METRICS:
    from prometheus_client import start_http_server, Counter, Gauge, Histogram

    PWAVE_REQUESTS = Counter(
        'pwave_requests_total',
        'Total number of trace messages received for P-wave detection'
    )
    PWAVE_DETECTIONS = Counter(
        'pwave_detections_total',
        'Total number of positive P-wave detections'
    )
    PWAVE_ERRORS = Counter(
        'pwave_inference_errors_total',
        'Total number of inference errors'
    )
    PWAVE_CACHE_SIZE = Gauge(
        'pwave_waveform_cache_size',
        'Number of station-channel entries in waveform cache'
    )
    PWAVE_INFERENCE_LATENCY = Histogram(
        'pwave_inference_latency_seconds',
        'Latency of P-wave model inference',
        buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
    )
    PWAVE_E2E_LATENCY = Histogram(
        'pwave_end_to_end_latency_seconds',
        'End-to-end latency from data provider to P-wave detection',
        buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0]
    )
else:
    PWAVE_REQUESTS = None
    PWAVE_DETECTIONS = None
    PWAVE_ERRORS = None
    PWAVE_CACHE_SIZE = None
    PWAVE_INFERENCE_LATENCY = None
    PWAVE_E2E_LATENCY = None


class TraceConsumer:
    """Kafka consumer that performs P-wave detection on incoming seismic traces."""

    def __init__(self):
        self.consumer = None
        self.producer = None
        self.model = tf.keras.models.load_model('./model_p_wave.h5', compile=False)
        self.last_waveform: Dict[str, list] = {}
        self.cache_lock = threading.Lock()

    def setTrace(self, data: Dict[str, Any]) -> obspy.Trace:
        """Reconstruct an ObsPy Trace from deserialized Kafka message."""
        trace = obspy.Trace(np.array(data['data']))
        trace.stats.network = data['network']
        trace.stats.station = data['station']
        trace.stats.location = data['location']
        trace.stats.channel = data['channel']
        trace.stats.starttime = obspy.UTCDateTime(data['start_time'])
        trace.stats.sampling_rate = data['sampling_rate']
        trace.stats.delta = data['delta']
        trace.stats.npts = data['npts']
        trace.stats.calib = data['calib']
        trace.stats.dataquality = data['data_quality']
        trace.stats.numsamples = data['num_samples']
        trace.stats.samplecnt = data['sample_cnt']
        trace.stats.sampletype = data['sample_type']
        trace.interpolate(sampling_rate=20)
        return trace

    def preprocessingPWave(self, data: np.ndarray) -> np.ndarray:
        return data / np.max(np.abs(data), axis=0)

    def predict(self, trace: obspy.Trace, data_provider_time: float) -> None:
        """Run P-wave detection model on a trace and publish results."""
        try:
            converter_np_array = np.array([trace.data, trace.data, trace.data]).T
            sliding_array = np.lib.stride_tricks.sliding_window_view(
                converter_np_array, (160, 3)).reshape(-1, 160, 3)
            preprocessed_array = np.apply_along_axis(
                self.preprocessingPWave, axis=1, arr=sliding_array)

            # Inference with latency measurement
            inference_start = time()
            predictions_p_wave = self.model.predict(preprocessed_array, verbose=0)
            inference_duration = time() - inference_start

            if ENABLE_METRICS and PWAVE_INFERENCE_LATENCY:
                PWAVE_INFERENCE_LATENCY.observe(inference_duration)

            # Find best P-wave detection window
            idx = 0
            max_value = 0
            n = 20
            for i in range(len(predictions_p_wave) - n + 1):
                if np.all(predictions_p_wave[i:i + n] >= 0.9):
                    if max_value < np.max(predictions_p_wave[i:i + n]):
                        max_value = np.max(predictions_p_wave[i:i + n])
                        idx = i

            if max_value == 0:
                return

            # P-wave detected!
            if ENABLE_METRICS and PWAVE_DETECTIONS:
                PWAVE_DETECTIONS.inc()

            p_wave_time = trace.stats.starttime.timestamp + idx * trace.stats.delta
            p_wave_waveform = trace.data.tolist()[idx + 40:idx + 120]

            data = {
                'network': trace.stats.network,
                'station': trace.stats.station,
                'location': trace.stats.location,
                'channel': trace.stats.channel,
                'sampling_rate': trace.stats.sampling_rate,
                'p_wave_time': p_wave_time,
                'data_provider_time': data_provider_time,
                'p_wave_detector_time': time(),
                'data': p_wave_waveform
            }

            self.producer.send(KAFKA_TOPIC_LOCMAG, data, key=f"{data['station']}-{data['channel']}")
            self.producer.flush()

            # End-to-end latency
            if ENABLE_METRICS and PWAVE_E2E_LATENCY:
                PWAVE_E2E_LATENCY.observe(time() - data_provider_time)

            logger.info(f"P-Wave detected for {trace.stats.station}-{trace.stats.channel}")

        except Exception as e:
            logger.error(f"Error predicting {trace.stats.station} {trace.stats.channel}: {e}")
            if ENABLE_METRICS and PWAVE_ERRORS:
                PWAVE_ERRORS.inc()

    def process(self, data: Dict[str, Any], data_delay: float) -> None:
        """Process incoming trace data: concatenate, detect, predict."""
        start_time = time()
        key = f"{data['station']}-{data['channel']}"

        with self.cache_lock:
            cached_data = self.last_waveform.get(key)
        
        if cached_data:
            data['data'] = cached_data + data['data']
            data['start_time'] = data['start_time'] - 4
            data['npts'] = len(data['data'])
            data['sample_cnt'] = len(data['data'])
            data['num_samples'] = len(data['data'])

        sampling_rate = data['sampling_rate']
        ratio = sampling_rate / 20
        new_length = int(len(data['data']) / ratio)
        
        if new_length >= 160:
            trace = self.setTrace(data)
            self.predict(trace, data['data_provider_time'])
            
            with self.cache_lock:
                self.last_waveform[key] = []

        process_time = time() - start_time
        logger.debug(f"Delay Kafka: {data_delay:.4f}s | Process Time: {process_time:.4f}s")

    def connectConsumer(self) -> None:
        """Main consumer loop: receive messages, spawn processing threads."""
        logger.info(f"Starting consumer loop on topic {KAFKA_TOPIC_PWAVE}...")
        for msg in self.consumer:
            data = msg.value
            data_delay = time() - data['data_provider_time']

            if ENABLE_METRICS and PWAVE_REQUESTS:
                PWAVE_REQUESTS.inc()

            threading.Thread(target=self.process, args=(data, data_delay)).start()

            # Update waveform cache safely
            key = f"{data['station']}-{data['channel']}"
            with self.cache_lock:
                if key in self.last_waveform:
                    self.last_waveform[key].extend(data['data'])
                else:
                    self.last_waveform[key] = data['data']

                cut_length = int(4 * data['sampling_rate'])
                if len(self.last_waveform[key]) > cut_length:
                    self.last_waveform[key] = self.last_waveform[key][-cut_length:]
                    
                cache_size = len(self.last_waveform)

            # Update cache size gauge
            if ENABLE_METRICS and PWAVE_CACHE_SIZE:
                PWAVE_CACHE_SIZE.set(cache_size)


if __name__ == '__main__':
    if ENABLE_METRICS:
        try:
            start_http_server(METRICS_PORT_PWAVE_DETECTOR)
            logger.info(f"Prometheus metrics server started on port {METRICS_PORT_PWAVE_DETECTOR}")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")

    traceConsumer = TraceConsumer()
    
    create_topic_if_not_exists(
        topic_name=KAFKA_TOPIC_LOCMAG,
        num_partitions=3,
        replication_factor=1,
        bootstrap_servers=KAFKA_BROKERS
    )

    traceConsumer.consumer = get_consumer(KAFKA_TOPIC_PWAVE, 'trace_group', KAFKA_BROKERS_PWAVE)
    traceConsumer.producer = get_producer(KAFKA_BROKERS)
    
    traceConsumer.connectConsumer()