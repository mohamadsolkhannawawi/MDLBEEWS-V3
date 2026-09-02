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
    from prometheus_client import start_http_server



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

    num_processes = int(os.getenv("DATA_PROVIDER_NUM_PROCESSES", "32"))
    num_stations = int(os.getenv("DATA_PROVIDER_NUM_STATIONS", "1200"))

    logger.info(f"Launching main data provider loop with {num_processes} processes and {num_stations} stations...")
    main(server='geofon.gfz-potsdam.de:18000', station_path='./data/stations.json', num_processes=num_processes, num_station_configs=num_stations)


