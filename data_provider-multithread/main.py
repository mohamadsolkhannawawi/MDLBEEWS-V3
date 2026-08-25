import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from multi_thread import main
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

logger = get_logger("dataprovidermultithread")

if ENABLE_METRICS:
    from prometheus_client import start_http_server, Counter, Gauge
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


if __name__ == '__main__':
    logger.info("Starting Data Provider (data_provider-multithread)...")

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

    logger.info("Launching main data provider loop...")
    main(station_path='./data_provider-multithread/data/stations.json', num_processes=30, num_station_configs=6000)
