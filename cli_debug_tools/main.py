import sys
import os
import json
from time import sleep

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import KAFKA_BROKERS, KAFKA_TOPIC_LOCMAG
from utils.kafka_helper import check_kafka_connection, topic_exists, get_consumer
from utils.logger import get_logger

logger = get_logger("DataConsumer")

class TraceConsumer:
    def __init__(self):
        self.consumer = None

    def connectConsumer(self):
        logger.info(f"Consuming from topic: {KAFKA_TOPIC_LOCMAG}")
        for msg in self.consumer:
            data = msg.value
            logger.info(f"Partition: {msg.partition} | Offset: {msg.offset} | Station: {data.get('station')} | Channel: {data.get('channel')}")

def initialize_system():
    while True:
        if check_kafka_connection(KAFKA_BROKERS) and topic_exists(KAFKA_TOPIC_LOCMAG, KAFKA_BROKERS):
            logger.info("System initialization successful.")
            break
        sleep(3)

if __name__ == '__main__':
    initialize_system()
    consumer = TraceConsumer()
    consumer.consumer = get_consumer(KAFKA_TOPIC_LOCMAG, 'data_consumer_group', KAFKA_BROKERS)
    consumer.connectConsumer()
