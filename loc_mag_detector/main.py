"""
Location & Magnitude Detector — Kafka Consumer → Producer
Consumes P-wave detection results from loc_mag_topic, estimates hypocenter and magnitude
using a pre-trained deep learning model, and publishes results to result_loc_mag_topic.

Instrumented with Prometheus metrics: Counter, Histogram.
"""

import sys
import os
import json
import threading
from time import sleep, time
from typing import Dict, Any

import numpy as np
import tensorflow as tf

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import (
    ENABLE_METRICS,
    METRICS_PORT_LOCMAG,
    KAFKA_BROKERS,
    KAFKA_TOPIC_LOCMAG,
    KAFKA_TOPIC_RESULT
)
from utils.kafka_helper import create_topic_if_not_exists, get_consumer, get_producer
from utils.logger import get_logger

logger = get_logger("LocMagDetector")

# =============================================================================
# Prometheus Metrics
# =============================================================================
if ENABLE_METRICS:
    from prometheus_client import start_http_server, Counter, Histogram

    LOCMAG_ESTIMATIONS = Counter(
        'locmag_estimations_total',
        'Total number of location-magnitude estimations produced'
    )
    LOCMAG_ERRORS = Counter(
        'locmag_errors_total',
        'Total number of inference errors in location-magnitude detection'
    )
    LOCMAG_INFERENCE_LATENCY = Histogram(
        'locmag_inference_latency_seconds',
        'Latency of location-magnitude model inference',
        buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
    )
    LOCMAG_E2E_LATENCY = Histogram(
        'locmag_end_to_end_latency_seconds',
        'End-to-end latency from data provider to loc-mag estimation',
        buckets=[0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0]
    )
else:
    LOCMAG_ESTIMATIONS = None
    LOCMAG_ERRORS = None
    LOCMAG_INFERENCE_LATENCY = None
    LOCMAG_E2E_LATENCY = None


class TraceConsumer:
    """Kafka consumer that estimates location and magnitude from P-wave detections."""

    def __init__(self):
        self.consumer = None
        self.producer = None
        self.model = tf.keras.models.load_model('./model_loc_mag.h5', compile=False)

    def preprocessingPWave(self, data: np.ndarray) -> np.ndarray:
        return data / np.max(np.abs(data), axis=0)

    def predict(self, data: Dict[str, Any]) -> None:
        """Run location-magnitude estimation on P-wave detection data."""
        try:
            converter_np_array = np.array([
                data['data'],
                data['data'],
                data['data']
            ]).T
            sliding_array = np.lib.stride_tricks.sliding_window_view(
                converter_np_array, (80, 3)).reshape(-1, 80, 3)
            preprocessed_array = np.apply_along_axis(
                self.preprocessingPWave, axis=1, arr=sliding_array)

            # Inference with latency measurement
            inference_start = time()
            predictions_loc_mag = self.model.predict(preprocessed_array, verbose=0)
            inference_duration = time() - inference_start

            if ENABLE_METRICS and LOCMAG_INFERENCE_LATENCY:
                LOCMAG_INFERENCE_LATENCY.observe(inference_duration)

            self.producer.send(
                KAFKA_TOPIC_RESULT,
                value={
                    'station': data['station'],
                    'channel': data['channel'],
                    'predictions_loc_mag': predictions_loc_mag.tolist(),
                    'data_provider_time': data.get('data_provider_time', 0),
                    'p_wave_detector_time': data.get('p_wave_detector_time', 0),
                    'loc_mag_detector_time': time(),
                }
            )
            self.producer.flush()

            if ENABLE_METRICS and LOCMAG_ESTIMATIONS:
                LOCMAG_ESTIMATIONS.inc()

            logger.info(f"Estimated for {data['station']}-{data['channel']}: {predictions_loc_mag.tolist()[0]}")

            del converter_np_array, sliding_array, preprocessed_array, predictions_loc_mag

        except Exception as e:
            logger.error(f"Error predicting {data['station']} {data['channel']}: {e}")
            if ENABLE_METRICS and LOCMAG_ERRORS:
                LOCMAG_ERRORS.inc()

    def process(self, data: Dict[str, Any]) -> None:
        start_time = time()
        self.predict(data)

        pwave_delay = start_time - data.get('p_wave_detector_time', start_time)
        all_delay = start_time - data.get('data_provider_time', start_time)
        process_time = time() - start_time

        if ENABLE_METRICS and LOCMAG_E2E_LATENCY:
            LOCMAG_E2E_LATENCY.observe(all_delay)

        logger.debug(f"PWave Delay: {pwave_delay:.4f}s | E2E Delay: {all_delay:.4f}s | Process: {process_time:.4f}s")

    def connectConsumer(self) -> None:
        """Main consumer loop."""
        logger.info(f"Starting consumer loop on topic {KAFKA_TOPIC_LOCMAG}...")
        for msg in self.consumer:
            data = msg.value
            threading.Thread(target=self.process, args=(data,)).start()


if __name__ == '__main__':
    if ENABLE_METRICS:
        try:
            start_http_server(METRICS_PORT_LOCMAG)
            logger.info(f"Prometheus metrics server started on port {METRICS_PORT_LOCMAG}")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")

    traceConsumer = TraceConsumer()
    
    create_topic_if_not_exists(
        topic_name=KAFKA_TOPIC_RESULT,
        num_partitions=3,
        replication_factor=1,
        bootstrap_servers=KAFKA_BROKERS
    )

    traceConsumer.consumer = get_consumer(KAFKA_TOPIC_LOCMAG, 'loc_mag_group', KAFKA_BROKERS)
    traceConsumer.producer = get_producer(KAFKA_BROKERS)
    
    traceConsumer.connectConsumer()