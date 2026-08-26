import sys
import os
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

logger = get_logger("DataProvider")

if ENABLE_METRICS:
    from prometheus_client import REGISTRY, start_http_server, Counter, Gauge

    def get_metric(metric_type, name, documentation, label_names=None):
        registry_name = name.removesuffix('_total')
        existing_metric = REGISTRY._names_to_collectors.get(registry_name)
        if existing_metric is not None:
            return existing_metric
        metric_kwargs = {'labelnames': label_names} if label_names else {}
        return metric_type(name, documentation, **metric_kwargs)

    TRACES_SENT = get_metric(
        Counter,
        'TRACES_SENT',
        'Total number of trace messages sent to Kafka',
        ['topic']
    )
    PUBLISH_ERRORS = get_metric(
        Counter,
        'PUBLISH_ERRORS',
        'Total number of Kafka publish errors'
    )
    ACTIVE_STREAMS = get_metric(
        Gauge,
        'ACTIVE_STREAMS',
        'Number of active SeedLink streams'
    )
else:
    TRACES_SENT = None
    PUBLISH_ERRORS = None
    ACTIVE_STREAMS = None


if __name__ == '__main__':
    logger.info("Starting Data Provider...")

    # Start Prometheus metrics server
    if ENABLE_METRICS:
        try:
            start_http_server(METRICS_PORT_DATA_PROVIDER)
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

    logger.info(f"Launching multi_process with {num_processes} processes and {num_stations} stations")
    main(station_path='./data/stations.json', num_processes=num_processes, num_station_configs=num_stations)