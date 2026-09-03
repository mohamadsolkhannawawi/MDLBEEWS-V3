# Verifikasi Konfigurasi Docker Compose (S1 - S5)

Dokumen ini menguraikan letak spesifik (ciri khas) dari masing-masing file konfigurasi `docker-compose*.yml` untuk membuktikan bahwa isi konfigurasinya sudah benar-benar sinkron dengan nama filenya dan tidak tertukar.

### [docker-compose-s1-mp_mt.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-mp_mt.yml)
- **Data Provider Dockerfile**: Menggunakan `data_provider-multiprocess-multithread/Dockerfile`

### [docker-compose-s1-multiprocess.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-multiprocess.yml)
- **Data Provider Dockerfile**: Menggunakan `data_provider-multiprocess/Dockerfile`

### [docker-compose-s1-multithread.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-multithread.yml)
- **Data Provider Dockerfile**: Menggunakan `data_provider-multithread/Dockerfile`

### [docker-compose-s1-sequential.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-sequential.yml)
- **Data Provider Dockerfile**: Menggunakan `data_provider-sequence/Dockerfile`

### [docker-compose-s2-no_metrics.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s2-no_metrics.yml)
- **Prometheus**: Tidak ada service prometheus / instrumentasi dimatikan.

### [docker-compose-s2-with_metrics.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s2-with_metrics.yml)
- **Prometheus**: Service `prometheus` dan `grafana` diaktifkan.

### [docker-compose-s3-archiver-1c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-archiver-1c.yml)
- **Replicas Data Archiver**: Diset sebanyak `1` container.

### [docker-compose-s3-archiver-2c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-archiver-2c.yml)
- **Replicas Data Archiver**: Diset sebanyak `2` container.

### [docker-compose-s3-archiver-3c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-archiver-3c.yml)
- **Replicas Data Archiver**: Diset sebanyak `3` container.

### [docker-compose-s3-archiver-4c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-archiver-4c.yml)
- **Replicas Data Archiver**: Diset sebanyak `4` container.

### [docker-compose-s3-archiver-5c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-archiver-5c.yml)
- **Replicas Data Archiver**: Diset sebanyak `5` container.

### [docker-compose-s3-pwave-kafka-nginx-2c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-pwave-kafka-nginx-2c.yml)
- **Tipe P-Wave**: Menggunakan FastAPI (`p_wave_detector_load_balance`).
- **Replicas**: Diset sebanyak `2` container.

### [docker-compose-s3-pwave-kafka-nginx-3c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-pwave-kafka-nginx-3c.yml)
- **Tipe P-Wave**: Menggunakan FastAPI (`p_wave_detector_load_balance`).
- **Replicas**: Diset sebanyak `3` container.

### [docker-compose-s3-pwave-kafka-nginx-4c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-pwave-kafka-nginx-4c.yml)
- **Tipe P-Wave**: Menggunakan FastAPI (`p_wave_detector_load_balance`).
- **Replicas**: Diset sebanyak `4` container.

### [docker-compose-s3-pwave-kafka-nginx-5c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-pwave-kafka-nginx-5c.yml)
- **Tipe P-Wave**: Menggunakan FastAPI (`p_wave_detector_load_balance`).
- **Replicas**: Diset sebanyak `5` container.

### [docker-compose-s3-pwave-kafka-2c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-pwave-kafka-2c.yml)
- **Tipe P-Wave**: Menggunakan Kafka Native (`p_wave_detector`).
- **Replicas**: Diset sebanyak `2` container.

### [docker-compose-s3-pwave-kafka-3c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-pwave-kafka-3c.yml)
- **Tipe P-Wave**: Menggunakan Kafka Native (`p_wave_detector`).
- **Replicas**: Diset sebanyak `3` container.

### [docker-compose-s3-pwave-kafka-4c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-pwave-kafka-4c.yml)
- **Tipe P-Wave**: Menggunakan Kafka Native (`p_wave_detector`).
- **Replicas**: Diset sebanyak `4` container.

### [docker-compose-s3-pwave-kafka-5c.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s3-pwave-kafka-5c.yml)
- **Tipe P-Wave**: Menggunakan Kafka Native (`p_wave_detector`).
- **Replicas**: Diset sebanyak `5` container.

### [docker-compose-s4-express.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s4-express.yml)
- **Backend**: Menjalankan service `api_server` (Express.js).

### [docker-compose-s4-fastapi.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s4-fastapi.yml)
- **Backend**: Menjalankan service `fast_api` (FastAPI).

### [docker-compose-s5-kafka.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s5-kafka.yml)
- **Load Balancer**: Tidak menggunakan NGINX, murni Kafka native.

### [docker-compose-s5-nginx.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s5-nginx.yml)
- **Load Balancer**: Menggunakan service `nginx` untuk load balancing Kafka.

### [docker-compose.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose.yml)
- **Master Compose**: Memuat seluruh service dari hulu ke hilir dengan konfigurasi default (produksi).
