"""
WebSocket Server (FastAPI) — Kafka Consumer → Native WebSocket
Alternative WebSocket server using FastAPI's native WebSocket support.
Consumes trace data and location-magnitude results from Kafka,
broadcasts to connected WebSocket clients.

Instrumented with Prometheus metrics via prometheus_client.
"""

import sys
import os
import json
import asyncio
import time
from threading import Thread

from fastapi import FastAPI, WebSocket, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import (
    ENABLE_METRICS,
    METRICS_PORT_FASTAPI,
    KAFKA_BROKERS,
    KAFKA_TOPIC_TRACE,
    KAFKA_TOPIC_RESULT
)
from utils.kafka_helper import get_consumer, check_kafka_connection
from utils.logger import get_logger

logger = get_logger("FastAPI")

# =============================================================================
# Prometheus Metrics
# =============================================================================
if ENABLE_METRICS:
    from prometheus_client import (
        Counter, Gauge, Histogram,
        generate_latest, CONTENT_TYPE_LATEST
    )

    FASTAPI_WS_BROADCAST = Counter(
        'fastapi_ws_messages_broadcast_total',
        'Total number of messages broadcast to WebSocket clients',
        ['topic']
    )
    FASTAPI_WS_CONNECTIONS = Counter(
        'fastapi_ws_client_connections_total',
        'Total number of WebSocket client connections'
    )
    FASTAPI_WS_DISCONNECTIONS = Counter(
        'fastapi_ws_client_disconnections_total',
        'Total number of WebSocket client disconnections'
    )
    FASTAPI_WS_ACTIVE = Gauge(
        'fastapi_ws_active_clients',
        'Number of currently connected WebSocket clients'
    )
    FASTAPI_WS_BROADCAST_LATENCY = Histogram(
        'fastapi_ws_broadcast_latency_seconds',
        'Latency of broadcasting a message to all clients',
        buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0]
    )
else:
    FASTAPI_WS_BROADCAST = None
    FASTAPI_WS_CONNECTIONS = None
    FASTAPI_WS_DISCONNECTIONS = None
    FASTAPI_WS_ACTIVE = None
    FASTAPI_WS_BROADCAST_LATENCY = None


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients = set()
main_loop = None

@app.on_event("startup")
async def startup_event():
    global main_loop
    main_loop = asyncio.get_running_loop()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection handler."""
    await websocket.accept()
    connected_clients.add(websocket)

    if ENABLE_METRICS:
        if FASTAPI_WS_CONNECTIONS:
            FASTAPI_WS_CONNECTIONS.inc()
        if FASTAPI_WS_ACTIVE:
            FASTAPI_WS_ACTIVE.set(len(connected_clients))

    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        logger.info(f"Client disconnected: {e}")
    finally:
        connected_clients.discard(websocket)
        if ENABLE_METRICS:
            if FASTAPI_WS_DISCONNECTIONS:
                FASTAPI_WS_DISCONNECTIONS.inc()
            if FASTAPI_WS_ACTIVE:
                FASTAPI_WS_ACTIVE.set(len(connected_clients))


def consume_trace():
    """Kafka consumer thread for trace_topic."""
    consumer = get_consumer(KAFKA_TOPIC_TRACE, 'fast-api-group', KAFKA_BROKERS)
    logger.info(f"Started consuming {KAFKA_TOPIC_TRACE}")

    for message in consumer:
        data = message.value
        data['api_time'] = int(time.time() * 1000)
        
        endpoint = 'waves-data'
        message_data = {endpoint: data}

        broadcast_start = time.time()
        
        try:
            asyncio.run_coroutine_threadsafe(broadcast_message(message_data), main_loop)
        except Exception as e:
            logger.error(f"Error in broadcast loop: {e}")

        broadcast_duration = time.time() - broadcast_start

        if ENABLE_METRICS:
            if FASTAPI_WS_BROADCAST:
                FASTAPI_WS_BROADCAST.labels(topic=KAFKA_TOPIC_TRACE).inc()
            if FASTAPI_WS_BROADCAST_LATENCY:
                FASTAPI_WS_BROADCAST_LATENCY.observe(broadcast_duration)


def consume_loc_mag():
    """Kafka consumer thread for result_loc_mag_topic."""
    consumer = get_consumer(KAFKA_TOPIC_RESULT, 'fast-api-group2', KAFKA_BROKERS)
    logger.info(f"Started consuming {KAFKA_TOPIC_RESULT}")

    for message in consumer:
        data = message.value
        data['api_time'] = int(time.time() * 1000)
        
        logger.debug(f"Broadcasting Loc-Mag: {data.get('predictions_loc_mag', 'N/A')}")
        endpoint = 'loc-mag-data'
        message_data = {endpoint: data}

        broadcast_start = time.time()
        
        try:
            asyncio.run_coroutine_threadsafe(broadcast_message(message_data), main_loop)
        except Exception as e:
            logger.error(f"Error in broadcast loop: {e}")

        broadcast_duration = time.time() - broadcast_start

        if ENABLE_METRICS:
            if FASTAPI_WS_BROADCAST:
                FASTAPI_WS_BROADCAST.labels(topic=KAFKA_TOPIC_RESULT).inc()
            if FASTAPI_WS_BROADCAST_LATENCY:
                FASTAPI_WS_BROADCAST_LATENCY.observe(broadcast_duration)


async def broadcast_message(message: dict):
    """Broadcast message to all connected WebSocket clients."""
    if not connected_clients:
        return
        
    msg_str = json.dumps(message)
    clients_to_remove = []
    
    for client in connected_clients:
        try:
            await client.send_text(msg_str)
        except Exception as e:
            logger.warning(f"Error sending message to client: {e}")
            clients_to_remove.append(client)
            
    for client in clients_to_remove:
        connected_clients.discard(client)
        if ENABLE_METRICS and FASTAPI_WS_ACTIVE:
            FASTAPI_WS_ACTIVE.set(len(connected_clients))


@app.get("/")
async def get():
    return FileResponse("public/index.html")


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


def wait_for_kafka(brokers, max_retries=30, retry_interval=3):
    """Wait for Kafka brokers to become available before starting consumers."""
    for attempt in range(1, max_retries + 1):
        if check_kafka_connection(brokers):
            logger.info("Kafka brokers are available.")
            return True
        logger.warning(f"Kafka not ready (attempt {attempt}/{max_retries}), retrying in {retry_interval}s...")
        time.sleep(retry_interval)
    logger.error("Kafka brokers did not become available. Starting anyway...")
    return False


if __name__ == "__main__":
    logger.info("Starting FastAPI WebSocket Server")
    
    wait_for_kafka(KAFKA_BROKERS)
    
    consumer_thread = Thread(target=consume_trace, daemon=True)
    consumer_thread2 = Thread(target=consume_loc_mag, daemon=True)
    consumer_thread.start()
    consumer_thread2.start()
    
    uvicorn.run(app, host="0.0.0.0", port=3333)
