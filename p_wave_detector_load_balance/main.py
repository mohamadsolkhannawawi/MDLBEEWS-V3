"""
P-Wave Detector (Load-Balanced Mode) — FastAPI HTTP Endpoint
Exposes POST /trace endpoint for load-balanced P-wave detection.
Receives HTTP requests from Load Balancer, runs inference, publishes results to Kafka.

Instrumented with Prometheus metrics via prometheus_client.
"""

import sys
import os
import json
import asyncio
from time import time
from typing import Dict, Any

from fastapi import FastAPI, Response
import uvicorn
import obspy
import numpy as np
import tensorflow as tf
from cachetools import LRUCache

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import (
    ENABLE_METRICS,
    KAFKA_BROKERS,
    KAFKA_TOPIC_LOCMAG
)
from utils.kafka_helper import create_topic_if_not_exists, get_producer
from utils.logger import get_logger

logger = get_logger("PWaveDetectorLB")

# =============================================================================
# Prometheus Metrics
# =============================================================================
if ENABLE_METRICS:
    from prometheus_client import (
        Counter, Gauge, Histogram,
        generate_latest, CONTENT_TYPE_LATEST
    )

    PWAVE_LB_REQUESTS = Counter(
        'pwave_lb_requests_total',
        'Total number of HTTP trace requests received'
    )
    PWAVE_LB_DETECTIONS = Counter(
        'pwave_lb_detections_total',
        'Total number of positive P-wave detections (load-balanced)'
    )
    PWAVE_LB_ERRORS = Counter(
        'pwave_lb_inference_errors_total',
        'Total number of inference errors (load-balanced)'
    )
    PWAVE_LB_CACHE_SIZE = Gauge(
        'pwave_lb_waveform_cache_size',
        'Number of station-channel entries in waveform cache (load-balanced)'
    )
    PWAVE_LB_INFERENCE_LATENCY = Histogram(
        'pwave_lb_inference_latency_seconds',
        'Latency of P-wave model inference (load-balanced)',
        buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0, 600.0]
    )
    PWAVE_E2E_LATENCY = Histogram(
        'pwave_end_to_end_latency_seconds',
        'Total latency of processing a /trace HTTP request',
        buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0, 600.0]
    )
else:
    PWAVE_LB_REQUESTS = None
    PWAVE_LB_DETECTIONS = None
    PWAVE_LB_ERRORS = None
    PWAVE_LB_CACHE_SIZE = None
    PWAVE_LB_INFERENCE_LATENCY = None
    PWAVE_E2E_LATENCY = None


app = FastAPI()
last_waveform = LRUCache(maxsize=6000)
model = tf.keras.models.load_model('./model_p_wave.h5', compile=False)

create_topic_if_not_exists(
    topic_name=KAFKA_TOPIC_LOCMAG,
    num_partitions=1,
    replication_factor=1,
    bootstrap_servers=KAFKA_BROKERS
)

producer = get_producer(KAFKA_BROKERS)


def set_trace(data: Dict[str, Any]) -> obspy.Trace:
    trace = obspy.Trace(np.array(data['data']))
    trace.stats.update({
        'network': data['network'],
        'station': data['station'],
        'location': data['location'],
        'channel': data['channel'],
        'starttime': obspy.UTCDateTime(data['start_time']),
        'sampling_rate': data['sampling_rate'],
        'delta': data['delta'],
        'npts': data['npts'],
        'calib': data['calib'],
        'dataquality': data['data_quality'],
        'numsamples': data['num_samples'],
        'samplecnt': data['sample_cnt'],
        'sampletype': data['sample_type']
    })
    trace.interpolate(sampling_rate=20)
    return trace


def preprocessing_p_wave(data: np.ndarray) -> np.ndarray:
    return data / np.max(np.abs(data), axis=0)


async def predict(trace: obspy.Trace, data_provider_time: float) -> None:
    try:
        converter_np_array = np.stack([trace.data] * 3, axis=-1)
        sliding_array = np.lib.stride_tricks.sliding_window_view(
            converter_np_array, (160, 3)).reshape(-1, 160, 3)
        preprocessed_array = preprocessing_p_wave(sliding_array)

        # Inference with latency measurement
        inference_start = time()
        predictions_p_wave = await asyncio.get_event_loop().run_in_executor(
            None, lambda: model(preprocessed_array, training=False).numpy()
        )
        inference_duration = time() - inference_start

        if ENABLE_METRICS and PWAVE_LB_INFERENCE_LATENCY:
            PWAVE_LB_INFERENCE_LATENCY.observe(inference_duration)

        idx, max_value = max(
            ((i, np.max(predictions_p_wave[i:i + 20])) for i in range(len(predictions_p_wave) - 19)),
            key=lambda x: x[1],
            default=(0, 0)
        )

        if max_value == 0 or max_value < 0.95:
            return

        # P-wave detected!
        if ENABLE_METRICS and PWAVE_LB_DETECTIONS:
            PWAVE_LB_DETECTIONS.inc()

        p_wave_time = trace.stats.starttime.timestamp + idx * trace.stats.delta
        p_wave_waveform = trace.data[idx + 40:idx + 120].tolist()

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

        await asyncio.get_event_loop().run_in_executor(
            None, lambda: producer.send(KAFKA_TOPIC_LOCMAG, data, key=f"{data['station']}-{data['channel']}")
        )
        producer.flush()

        logger.info(f"P-Wave detected for {trace.stats.station}-{trace.stats.channel}")

    except Exception as e:
        logger.error(f"Error predict {trace.stats.station} {trace.stats.channel}: {e}")
        if ENABLE_METRICS and PWAVE_LB_ERRORS:
            PWAVE_LB_ERRORS.inc()


async def process(data: Dict[str, Any], data_delay: float) -> None:
    start_time = time()
    key = f"{data['station']}-{data['channel']}"

    if key in last_waveform:
        data['data'] = last_waveform[key] + data['data']
        data['start_time'] -= 4
        data['npts'] = len(data['data'])
        data['sample_cnt'] = len(data['data'])
        data['num_samples'] = len(data['data'])

    sampling_rate = data['sampling_rate']
    ratio = sampling_rate / 20
    new_length = int(len(data['data']) / ratio)
    if new_length >= 160:
        trace = set_trace(data)
        await predict(trace, data['data_provider_time'])
        last_waveform[key] = []

    process_duration = time() - start_time
    if ENABLE_METRICS and PWAVE_E2E_LATENCY:
        PWAVE_E2E_LATENCY.observe(process_duration)

    logger.debug(f"Delay Kafka: {data_delay:.4f}s | Process Time: {process_duration:.4f}s")


@app.post("/trace")
async def trace_endpoint(data: dict):
    """HTTP endpoint for receiving trace data from Load Balancer."""
    if ENABLE_METRICS and PWAVE_LB_REQUESTS:
        PWAVE_LB_REQUESTS.inc()

    data_delay = time() - data['data_provider_time']

    asyncio.create_task(process(data, data_delay))

    key = f"{data['station']}-{data['channel']}"
    if key in last_waveform:
        last_waveform[key] += data['data']
    else:
        last_waveform[key] = data['data']

    cut_length = int(4 * data['sampling_rate'])
    if len(last_waveform[key]) > cut_length:
        last_waveform[key] = last_waveform[key][-cut_length:]

    if ENABLE_METRICS and PWAVE_LB_CACHE_SIZE:
        PWAVE_LB_CACHE_SIZE.set(len(last_waveform))


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    if ENABLE_METRICS:
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
    return Response(content="Metrics disabled", status_code=404)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == '__main__':
    logger.info("Starting P-Wave Detector (Load Balanced Mode)")
    uvicorn.run(app, host="0.0.0.0", port=8004)
