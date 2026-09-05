"""
Load Balancer — Kafka Consumer → HTTP Forwarder
Consumes from p_wave_topic and forwards via HTTP to P-Wave Detector instances.

Instrumented with Prometheus metrics: Counter, Histogram.
"""

import sys
import os
import json
import time
from time import sleep
import requests
from typing import Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import (
    ENABLE_METRICS,
    METRICS_PORT_LOAD_BALANCER,
    KAFKA_BROKERS_PWAVE,
    KAFKA_TOPIC_PWAVE
)
from utils.kafka_helper import check_kafka_connection, topic_exists, get_consumer
from utils.logger import get_logger

logger = get_logger("LoadBalancer")

# =============================================================================
# Prometheus Metrics
# =============================================================================
if ENABLE_METRICS:
    from prometheus_client import start_http_server, Counter, Histogram

    LB_FORWARDED = Counter(
        'lb_messages_forwarded_total',
        'Total number of messages forwarded to P-Wave Detector'
    )
    LB_FORWARD_ERRORS = Counter(
        'lb_forward_errors_total',
        'Total number of failed forward attempts'
    )
    LB_FORWARD_LATENCY = Histogram(
        'lb_forward_latency_seconds',
        'Latency of HTTP forward to P-Wave Detector',
        buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0, 600.0]
    )
else:
    LB_FORWARDED = None
    LB_FORWARD_ERRORS = None
    LB_FORWARD_LATENCY = None


class TraceConsumer:
    """Kafka consumer that forwards trace data via HTTP to load-balanced P-Wave Detectors."""

    def __init__(self):
        self.consumer = None
        self.target_url = os.getenv(
            "LB_TARGET_URL",
            "http://p_wave_detector_load_balance:8004/trace"
        )

    def connectConsumer(self) -> None:
        """Main consumer loop: forward messages via HTTP with latency tracking."""
        logger.info(f"Starting to consume from {KAFKA_TOPIC_PWAVE} and forward to {self.target_url}")

        for msg in self.consumer:
            data = msg.value
            kafka_delay = time.time() - data['data_provider_time']

            logger.debug(
                f"Partition: {msg.partition} | Offset: {msg.offset} | "
                f"Station: {data['station']}-{data['channel']} | "
                f"Delay Kafka: {kafka_delay:.4f}s"
            )

            forward_start = time.time()
            try:
                response = requests.post(self.target_url, json=data, timeout=30)
                response.raise_for_status()
                forward_duration = time.time() - forward_start

                if ENABLE_METRICS:
                    if LB_FORWARDED:
                        LB_FORWARDED.inc()
                    if LB_FORWARD_LATENCY:
                        LB_FORWARD_LATENCY.observe(forward_duration)

            except Exception as e:
                logger.error(f"Error forwarding to {self.target_url}: {e}")
                if ENABLE_METRICS and LB_FORWARD_ERRORS:
                    LB_FORWARD_ERRORS.inc()


def initialize_system() -> None:
    while True:
        if check_kafka_connection(KAFKA_BROKERS_PWAVE) and topic_exists(KAFKA_TOPIC_PWAVE, KAFKA_BROKERS_PWAVE):
            logger.info("System initialization successful.")
            break
        sleep(3)


if __name__ == '__main__':
    if ENABLE_METRICS:
        try:
            start_http_server(METRICS_PORT_LOAD_BALANCER)
            logger.info(f"Prometheus metrics server started on port {METRICS_PORT_LOAD_BALANCER}")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")

    initialize_system()
    
    consumer = TraceConsumer()
    consumer.consumer = get_consumer(KAFKA_TOPIC_PWAVE, 'load_balancer_group', KAFKA_BROKERS_PWAVE)
    consumer.connectConsumer()