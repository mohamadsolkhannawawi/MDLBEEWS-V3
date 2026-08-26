# MDLBEEWS: Modular Deep Learning Based Earthquake Early Warning System

## Overview
MDLBEEWS is a high-performance, event-driven microservices architecture designed for real-time Earthquake Early Warning. By leveraging deep learning alongside robust data streaming technologies, the system is capable of analyzing continuous seismic waveforms, detecting P-Waves, computing earthquake location and magnitude, and disseminating real-time alerts with minimal latency.

The platform is fully containerized, horizontally scalable, and features a comprehensive observability stack to monitor system health, throughput, and end-to-end latency across all distributed components.

## Architecture & Microservices
The system follows an **Event-Driven Microservices** paradigm, decoupling data ingestion from processing and archival via Apache Kafka. 

### Core Components
1. **Data Provider**
   Connects to seismic sensors (via SeedLink protocol), parses multiplexed MiniSEED data into standardized JSON formats, and publishes raw waveform streams to the `eews-data` Kafka topic.
2. **P-Wave Detector**
   Consumes raw seismic data, preprocesses it, and utilizes a Deep Learning model to detect the arrival of Primary Waves (P-Waves). It publishes detection events to the `p-wave-picks` Kafka topic.
3. **Location & Magnitude (Loc-Mag) Detector**
   Listens to P-Wave detection events and estimates the hypocenter (location) and magnitude of the potential earthquake, issuing the final early warning alerts.
4. **Data Archiver**
   Acts as the system's sink, consuming all processed data and metadata. It archives continuous waveforms into standard MiniSEED files and stores event metadata into a MongoDB database for post-event analysis.
5. **Real-time API Servers (WebSockets)**
   Both Express.js and FastAPI implementations exist to broadcast real-time alerts to frontend dashboards and mobile clients via low-latency WebSockets.

### Infrastructure & Observability
- **Message Broker:** Apache Kafka & Zookeeper (handles high-throughput asynchronous communication).
- **Database:** MongoDB (for JSON metadata and processing logs).
- **Observability Stack:** Prometheus and Grafana are integrated to scrape and visualize metrics (CPU/Memory usage, Kafka lag, end-to-end processing delays, and system throughput).

## Prerequisites
- Docker Engine and Docker Compose (v2)
- At least 8GB of RAM allocated to Docker (16GB recommended for running the full observability and deep learning stack).

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-org/MDLBEEWS.git
   cd MDLBEEWS
   ```

2. **Environment Configuration**
   Copy the example environment variables file and modify it if necessary:
   ```bash
   cp .env.example .env
   ```

3. **Build and Run the System**
   Launch the entire microservices ecosystem, including Kafka, MongoDB, processing nodes, and the observability stack:
   ```bash
   docker compose up -d --build
   ```

## Monitoring & Observability
Once the system is operational, you can access the monitoring interfaces to observe the real-time performance of the deep learning pipeline:

- **Grafana Dashboard:** http://localhost:4000 (Default Login: `admin` / `12345678`)
- **Prometheus UI:** http://localhost:9090
- **Node Exporter:** http://localhost:9100

To gracefully shut down the environment and remove the created containers and networks:
```bash
docker compose down -v
```

## System Scalability
The architecture is designed to scale horizontally. If the volume of seismic stations increases, you can easily scale the consumer services. For example, to run multiple instances of the P-Wave Detector:
```bash
docker compose up -d --scale p_wave_detector=3
```
*(Note: Kafka partitions must be configured to match or exceed the number of consumer replicas for effective load distribution).*

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
