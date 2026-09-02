import sys
import os

# MUST set PROMETHEUS_MULTIPROC_DIR before ANY prometheus_client imports
MULTIPROC_DIR = "/tmp/prometheus_multiproc"
os.environ["PROMETHEUS_MULTIPROC_DIR"] = MULTIPROC_DIR

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from multi_process import main
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

logger = get_logger("dataprovidermultiprocess")

if ENABLE_METRICS:
    import shutil
    from prometheus_client import CollectorRegistry, multiprocess, generate_latest, CONTENT_TYPE_LATEST
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    # Clean stale files from previous runs
    if os.path.isdir(MULTIPROC_DIR):
        shutil.rmtree(MULTIPROC_DIR)
    os.makedirs(MULTIPROC_DIR, exist_ok=True)

    class MetricsHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            registry = CollectorRegistry()
            multiprocess.MultiProcessCollector(registry)
            data = generate_latest(registry)
            self.send_response(200)
            self.send_header('Content-Type', CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(data)


if __name__ == '__main__':
    logger.info("Starting Data Provider (data_provider-multiprocess)...")

    # Start Prometheus metrics server
    if ENABLE_METRICS:
        try:
            server = HTTPServer(('0.0.0.0', METRICS_PORT_DATA_PROVIDER), MetricsHandler)
            import threading
            metrics_thread = threading.Thread(target=server.serve_forever, daemon=True)
            metrics_thread.start()
            logger.info(f"Prometheus metrics server started on port {METRICS_PORT_DATA_PROVIDER}")
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

    logger.info(f"Launching main data provider loop with {num_processes} processes and {num_stations} stations...")
    main(server='geofon.gfz-potsdam.de:18000', station_path='./data/stations.json', num_processes=num_processes, num_station_configs=num_stations)


