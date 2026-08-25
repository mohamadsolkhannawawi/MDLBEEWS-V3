# MDLBEEWS: Modular Deep Learning Based Earthquake Early Warning System (with Observability)

## Description

MDLBEEWS is a modular deep learning-based earthquake early warning system designed to provide real-time alerts and information about seismic activities. It leverages advanced machine learning techniques to analyze seismic data and predict potential earthquakes, enabling timely responses to mitigate risks and enhance safety. This software is designed to accelerate real-time seismic data processing to support earthquake early warning systems. Featuring a modular interface and containerization support, the system is easily deployable by geophysics researchers, disaster management agencies, and technology developers.

This repository features a significant enhancement: a **structured observability layer** based on **Prometheus and Grafana**. This layer enables real-time and reproducible monitoring of the system's performance, capturing metrics such as inter-service communication latency, CPU/memory usage, and end-to-end data delay across all microservices (Data Provider, P-Wave Detector, Load Balancer, Loc-Mag Detector, Data Archiver, and WebSocket Server).

MDLBEEWS is built on a foundation of modern technologies to deliver scalable, reliable, and high-performance earthquake early warning capabilities. The system leverages Docker for containerization, ensuring consistent deployment and simplified dependency management across platforms. Apache Kafka serves as the core message broker, enabling real-time, fault-tolerant streaming of seismic data between modules. For real-time, bidirectional communication, the system employs WebSocket protocols implemented with Express.js and FastAPI, supporting low-latency delivery of alerts and updates.

### Table of Contents
- [Installation](#installation)
- [How To Run](#how-to-run)
- [Observability Test Scenarios](#observability-test-scenarios)
- [License](#license)

## Installation
To install MDLBEEWS, follow these steps:
1. Install Docker and Docker Compose for your operating system.
2. Clone the repository:
   ```bash
   git clone https://github.com/ArjunaWahyu/MDLBEEWS.git
   cd MDLBEEWS
   ```

## Requirement 
All modules have been dockerized. The primary dependencies utilized inside the containers include `kafka-python-ng`, `tensorflow`, `obspy`, `fastapi`, `express.js`, `socket.io`, and `prometheus_client`.

## How To Run

1. You can run the entire system (including Prometheus and Grafana) using Docker Compose with the following command:
    ```bash
    docker compose up -d
    ```

2. Once running, you can access the observability tools at:
    - **Grafana Dashboard:** http://localhost:4000 (Login: `admin` / `12345678`)
    - **Prometheus UI:** http://localhost:9090
    - **Node Exporter Metrics:** http://localhost:9100

3. To shut down the system and clean up volumes:
    ```bash
    docker compose down -v
    ```

## Observability Test Scenarios

The system has been configured to support several reproducible test scenarios to evaluate its performance under different conditions. These tests focus on the impact of observability, multi-container scalability, load balancing, and WebSocket implementations.

You can run these tests automatically using the provided PowerShell script, which will tear down existing containers, spin up the specified scenario, wait for stabilization, and collect metrics into a CSV file via the Prometheus API.

```powershell
# Run all scenarios iteratively
./tests/run_all_tests.ps1 -Scenario all

# Run a specific scenario (e.g., s1b)
./tests/run_all_tests.ps1 -Scenario s1b
```

### S1: Prometheus Instrumentation Overhead

Evaluates the performance overhead introduced by the `prometheus_client` instrumentation across all modules.

| Scenario | File | Description |
|---|---|---|
| **S1a** | `docker-compose-5-1.yml` | Metrics disabled (`ENABLE_METRICS=false`), no Prometheus/Node Exporter |
| **S1b** | `docker-compose-5-2.yml` | Metrics enabled, full observability stack active |

### S2: Multi-Container Scalability

Evaluates the system's ability to scale data processing modules horizontally.

| Scenario | File | Description |
|---|---|---|
| **S2** | `docker-compose.yml` | Uses the default setup but can be scaled using Docker Compose replicas (e.g., `deploy: replicas: 3` for P-Wave Detector & Archiver) |

### S3: WebSocket Server Implementation Comparison

Compares the performance of different WebSocket server technologies for real-time client dissemination.

| Scenario | File | Description |
|---|---|---|
| **S3** | `docker-compose.yml` | Both Express.js (`api_server` on port 3333) and FastAPI (`fast_api` on port 3334) run simultaneously. Load testing can be directed to either port. |

### S4: Load Balancing (Kafka vs NGINX)

Evaluates load balancing strategies for HTTP-based components within the pipeline.

| Scenario | File | Description |
|---|---|---|
| **S4a** | `docker-compose-2-1.yml` | Kafka native load balancing (consumer groups) |
| **S4b** | `docker-compose-2-2.yml` | NGINX used as an active HTTP load balancer routing to P-Wave HTTP endpoints |

## LICENSE
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
