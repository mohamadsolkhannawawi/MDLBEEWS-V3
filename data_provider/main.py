import sys
import os
import shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from config.settings import (
    ENABLE_METRICS,
    METRICS_PORT_DATA_PROVIDER,
    KAFKA_BROKERS,
    KAFKA_BROKERS_PWAVE,
    KAFKA_TOPIC_TRACE,
    KAFKA_TOPIC_PWAVE
)
from utils.kafka_helper import create_topic_if_not_exists
from utils.logger import get_logger

logger = get_logger("DataProvider")

# =============================================================================
# Prometheus Multiprocess Setup
# =============================================================================
# Clean and prepare the multiprocess directory so child processes can
# write their metrics to shared files that the main HTTP server aggregates.
MULTIPROC_DIR = os.environ.get("PROMETHEUS_MULTIPROC_DIR", "/tmp/prometheus_multiproc")

if ENABLE_METRICS:
    # Clean stale files from previous runs
    if os.path.isdir(MULTIPROC_DIR):
        shutil.rmtree(MULTIPROC_DIR)
    os.makedirs(MULTIPROC_DIR, exist_ok=True)

    from prometheus_client import (
        Counter, Gauge,
        CollectorRegistry, multiprocess, generate_latest, CONTENT_TYPE_LATEST
    )
    from http.server import HTTPServer, BaseHTTPRequestHandler

    # Metrics — these will be automatically shared across child processes
    # because PROMETHEUS_MULTIPROC_DIR is set.
    TRACES_SENT = Counter(
        'data_provider_traces_sent',
        'Total number of trace messages sent to Kafka',
        ['topic']
    )
    PUBLISH_ERRORS = Counter(
        'data_provider_publish_errors',
        'Total number of Kafka publish errors'
    )
    ACTIVE_STREAMS = Gauge(
        'data_provider_active_streams',
        'Number of active SeedLink streams',
        multiprocess_mode='livesum'
    )

    class MetricsHandler(BaseHTTPRequestHandler):
        """Custom HTTP handler that aggregates metrics from all child processes."""
        def do_GET(self):
            registry = CollectorRegistry()
            multiprocess.MultiProcessCollector(registry)
            output = generate_latest(registry)
            self.send_response(200)
            self.send_header('Content-Type', CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(output)

        def log_message(self, format, *args):
            pass  # Suppress default access logs

else:
    TRACES_SENT = None
    PUBLISH_ERRORS = None
    ACTIVE_STREAMS = None


if __name__ == '__main__':
    logger.info("Starting Data Provider...")

    # Start Prometheus metrics server with multiprocess aggregation
    if ENABLE_METRICS:
        try:
            server = HTTPServer(('0.0.0.0', METRICS_PORT_DATA_PROVIDER), MetricsHandler)
            import threading
            metrics_thread = threading.Thread(target=server.serve_forever, daemon=True)
            metrics_thread.start()
            logger.info(f"Prometheus metrics server (multiprocess) started on port {METRICS_PORT_DATA_PROVIDER}")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")

    # Ensure required Kafka topics exist
    create_topic_if_not_exists(
        topic_name=KAFKA_TOPIC_TRACE,
        num_partitions=5,
        replication_factor=2,
        bootstrap_servers=KAFKA_BROKERS
    )
    
    create_topic_if_not_exists(
        topic_name=KAFKA_TOPIC_PWAVE,
        num_partitions=5,
        replication_factor=1,
        bootstrap_servers=KAFKA_BROKERS_PWAVE
    )

    num_processes = int(os.getenv("DATA_PROVIDER_NUM_PROCESSES", "30"))
    num_stations = int(os.getenv("DATA_PROVIDER_NUM_STATIONS", "6000"))

    logger.info(f"Launching multi_process with {num_processes} processes and {num_stations} stations")
    from multi_process import main
    main(station_path='./data/stations.json', num_processes=num_processes, num_station_configs=num_stations)