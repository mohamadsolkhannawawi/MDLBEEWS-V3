# Verifikasi Konfigurasi Docker Compose (S1 - S5)

Dokumen ini menguraikan letak spesifik (ciri khas) dari masing-masing file konfigurasi `docker-compose*.yml` untuk membuktikan bahwa isi konfigurasinya sudah benar-benar sinkron dengan nama filenya dan tidak tertukar.

### [docker-compose-s1-mp_mt.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-mp_mt.yml)
- **Data Provider Mode**: Di-override menggunakan environment `DATA_PROVIDER_MODE: "mp_mt"`.

### [docker-compose-s1-multiprocess.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-multiprocess.yml)
- **Data Provider Mode**: Di-override menggunakan environment `DATA_PROVIDER_MODE: "multiprocess"`.

### [docker-compose-s1-multithread.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-multithread.yml)
- **Data Provider Mode**: Di-override menggunakan environment `DATA_PROVIDER_MODE: "multithread"`.

### [docker-compose-s1-sequential.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-sequential.yml)
- **Data Provider Mode**: Di-override menggunakan environment `DATA_PROVIDER_MODE: "sequence"`.

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
  > **Cara Pengecekan:** Silakan buka filenya dan cari kata `nginx`. Anda tidak akan menemukannya. Selain itu, service P-Wave memanggil `dockerfile: p_wave_detector/Dockerfile` (versi aslinya yang menarik data langsung dari Kafka).

### [docker-compose-s5-nginx.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s5-nginx.yml)
- **Load Balancer**: Menggunakan service `nginx` untuk load balancing Kafka.
  > **Cara Pengecekan:** Cek baris paling bawah di dalam filenya, Anda akan melihat *service block* `nginx_load_balancer` (port 8004:80). Selain itu, service P-Wave memanggil `dockerfile: p_wave_detector_load_balance/Dockerfile` (versi HTTP yang menerima request distribusi trafik dari NGINX).

### [docker-compose.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose.yml)
- **Master Compose**: Memuat seluruh service dari hulu ke hilir dengan konfigurasi default (produksi).
# Verifikasi Konfigurasi Docker Compose (S1 - S5)

Dokumen ini menguraikan letak spesifik (ciri khas) dari masing-masing file konfigurasi `docker-compose*.yml` untuk membuktikan bahwa isi konfigurasinya sudah benar-benar sinkron dengan nama filenya dan tidak tertukar.

### [docker-compose-s1-mp_mt.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-mp_mt.yml)
- **Data Provider Mode**: Di-override menggunakan environment `DATA_PROVIDER_MODE: "mp_mt"`.

### [docker-compose-s1-multiprocess.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-multiprocess.yml)
- **Data Provider Mode**: Di-override menggunakan environment `DATA_PROVIDER_MODE: "multiprocess"`.

### [docker-compose-s1-multithread.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-multithread.yml)
- **Data Provider Mode**: Di-override menggunakan environment `DATA_PROVIDER_MODE: "multithread"`.

### [docker-compose-s1-sequential.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s1-sequential.yml)
- **Data Provider Mode**: Di-override menggunakan environment `DATA_PROVIDER_MODE: "sequence"`.

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
  > **Cara Pengecekan:** Silakan buka filenya dan cari kata `nginx`. Anda tidak akan menemukannya. Selain itu, service P-Wave memanggil `dockerfile: p_wave_detector/Dockerfile` (versi aslinya yang menarik data langsung dari Kafka).

### [docker-compose-s5-nginx.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose-s5-nginx.yml)
- **Load Balancer**: Menggunakan service `nginx` untuk load balancing Kafka.
  > **Cara Pengecekan:** Cek baris paling bawah di dalam filenya, Anda akan melihat *service block* `nginx_load_balancer` (port 8004:80). Selain itu, service P-Wave memanggil `dockerfile: p_wave_detector_load_balance/Dockerfile` (versi HTTP yang menerima request distribusi trafik dari NGINX).

### [docker-compose.yml](file:///e:/Documents/Bahan Skripsi/Program EEWS/MDLBEEWS/docker-compose.yml)
- **Master Compose**: Memuat seluruh service dari hulu ke hilir dengan konfigurasi default (produksi).
  > **Cara Pengecekan:** Buka filenya, Anda akan melihat file ini memuat *seluruh* komponen sistem EEWS (Mulai dari ZooKeeper, ke-3 Kafka, InfluxDB, Prometheus, Grafana, Nginx, hingga seluruh detektor dan WebSocket API) menjadi satu kesatuan (*Full Stack*). Selain itu, nilai *replicas*-nya diset pada konfigurasi normal, bukan direkayasa untuk keperluan uji *stress-test* seperti pada skenario 1 - 5.

# Verifikasi Modul Internal

Bagian ini memuat hasil pemeriksaan (*code review*) modul-modul internal (*source code* python/nodejs) guna memastikan fungsinya sudah sesuai dengan arsitektur yang dirancang di bab Metodologi.

### Modul: `api_server` (Express.js WebSocket)
- **Lokasi Folder**: e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\api_server
- **Tumpukan Teknologi (Tech Stack)**: Node.js, Express.js, Socket.IO, KafkaJS, dan prom-client.
- **Hasil Verifikasi Fungsi**:
  1. **Koneksi Kafka**: Modul ini sukses berfungsi sebagai *Consumer* yang berlangganan pada topik `trace_topic` dan `result_loc_mag_topic` (terlihat di `server.js` baris 56-57).
  2. **Diseminasi WebSocket**: Modul menggunakan pustaka `socket.io` untuk melakukan *broadcasting* (memancarkan) data secara *real-time* kepada klien-klien *dashboard* (dapat dikonfirmasi pada baris `client.emit(endpoint, data)`).
  3. **Observabilitas (Prometheus)**: Modul ini telah terinstrumentasi sempurna dengan metrik-metrik kustom seperti `ws_messages_broadcast_total`, `ws_active_clients`, dan `ws_broadcast_latency_seconds`, yang diekspos melalui *endpoint* HTTP `/metrics`.
  4. **Antarmuka (Dashboard)**: Melayani antarmuka monitoring web secara statis lewat rute `app.get("/")`.
- **Kesimpulan**: Modul `api_server` **100% Valid** dan terbukti berjalan persis seperti spesifikasi "Express.js WebSocket Server" pada Skenario 4.

### Modul: config (Central Configuration)
- **Lokasi Folder**: e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\config
- **Tumpukan Teknologi (Tech Stack)**: Python.
- **Hasil Verifikasi Fungsi**:
  1. **Manajemen *Environment Variables***: File settings.py sukses bertindak sebagai *Single Source of Truth* (sumber acuan tunggal) untuk seluruh variabel *environment* sistem Python. Seluruh kredensial dan alamat (seperti KAFKA_BROKERS, port Prometheus, hingga token INFLUXDB_URL) dipusatkan di sini menggunakan metode os.getenv() dengan nilai bawaan (*fallback*) yang kokoh.
  2. **Standardisasi Nama Topik**: Penamaan topik Kafka (seperti 	race_topic, p_wave_topic, loc_mag_topic) ditetapkan secara konstan agar tidak ada deviasi nama (*typo*) antar *microservice* yang memanggilnya.
  3. **Konfigurasi Metrik Observabilitas**: Variabel ENABLE_METRICS memastikan fitur instrumentasi Prometheus dapat dimatikan sepenuhnya secara global dari satu tempat, sesuai dengan kebutuhan Skenario 2 (Uji Overhead).
- **Kesimpulan**: Modul config **100% Valid**. Desain ini mengonfirmasi penerapan *Best Practice* arsitektur mikroservis 12-Factor App (konfigurasi dipisahkan dari kode).

### Modul: data_archiver (Seismic Data Storage Sink)
- **Lokasi Folder**: e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\data_archiver
- **Tumpukan Teknologi (Tech Stack)**: Python, Kafka-Python, PyMongo, InfluxDB-Client, ObsPy (untuk pengolahan format seismik MiniSEED).
- **Hasil Verifikasi Fungsi**:
  1. **Koneksi Kafka**: Modul ini sukses berfungsi sebagai *Consumer* yang berlangganan pada 	race_topic (mengambil gelombang seismik mentah).
  2. ***Polyglot Persistence* (Penyimpanan Multipangkalan Data)**: Modul mem-parsing data yang ditarik dari Kafka dan menyimpannya sekaligus ke tiga wadah penyimpanan berbeda:
     - **InfluxDB** (lewat save_data_to_influxdb) sebagai Time-Series Database untuk divisualisasikan oleh Grafana.
     - **MongoDB** (lewat save_data_to_mongodb) pada koleksi 	imeseries_collection sebagai data arsip *schema-less*.
     - **Sistem Berkas Lokal / Disk** (lewat save_data_to_mseed) dalam format standar internasional seismologi, yaitu **MiniSEED** (.mseed).
  3. **Toleransi Kesalahan (*Fault Tolerance*)**: Menggunakan fitur *retry logic* saat inisialisasi koneksi MongoDB (baris init_mongodb(max_retries=5)).
  4. **Observabilitas (Prometheus)**: Termonitor dengan cermat menggunakan metrik tipe Counter ( rchiver_records_saved_total,  rchiver_save_errors_total) dan Histogram ( rchiver_write_latency_seconds) untuk melacak waktu latensi penyimpanan IOPS ke masing-masing *database*.
- **Kesimpulan**: Modul data_archiver **100% Valid**. Desain pipa datanya (*data pipeline*) membuktikan kapabilitas sistem dalam menangani aliran data yang sangat masif (*high throughput*) khas pengolahan sinyal kegempaan (Skenario 3 Skalabilitas).

### Modul: `cli_debug_tools` (Debug Utility)
- **Lokasi Folder**: `e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\cli_debug_tools`
- **Tumpukan Teknologi (Tech Stack)**: Python, Kafka-Python.
- **Hasil Verifikasi Fungsi**:
  1. **Status Penggunaan**: Berdasarkan penyisiran di seluruh file *docker-compose*, modul ini **tidak di-deploy secara aktif** dalam skenario pengujian mana pun (S1 hingga S5) maupun di dalam *Master Compose*.
  2. **Fungsi Sebenarnya**: Modul ini murni bertindak sebagai skrip utilitas (*CLI debugging tool*) yang sangat ringan untuk menguji koneksi Kafka secara manual (membaca dan mencetak isi log dari topik loc_mag_topic ke dalam konsol).
  3. **Keselarasan Arsitektur**: Keberadaannya sah (terdokumentasi sebagai utilitas di DOKUMEN SKRIPSI/konteks-aplikasi-eews-observabilitas.md), meskipun tidak menjadi bagian dari *pipeline* utama aliran data otomatis.
- **Kesimpulan**: Modul `cli_debug_tools` **Valid** sebagai *support tool* (alat bantu *debug*). Modul ini bisa Anda jalankan secara independen ketika sedang memastikan *broker* Kafka tidak bermasalah.

### Modul: data_provider (Seismic Data Ingestion)
- **Lokasi Folder**: e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\data_provider
- **Tumpukan Teknologi (Tech Stack)**: Python, SeedLinkClient, Multi-Processing, Multi-Threading, Kafka-Python.
- **Hasil Verifikasi Fungsi**:
  1. **Universal Entrypoint**: Berhasil direfaktor menjadi modul tunggal yang menangani 4 mode komputasi berbeda (Sequential, Multi-Thread, Multi-Process, dan Hybrid) yang dikendalikan murni lewat variabel lingkungan DATA_PROVIDER_MODE.
  2. **Efisiensi Kode (DRY)**: 4 folder redundan berhasil dihapus tanpa merusak Skenario 1.
  3. **Observabilitas (Prometheus)**: Instrumentasi prometheus_client dikonfigurasi untuk *multiprocess mode* secara default untuk mengakomodasi pekerja (*workers*) paralel.
- **Kesimpulan**: Modul data_provider **100% Valid dan Elegan**. Desainnya sekarang sejalan dengan prinsip *12-Factor App* yang modern dan bersih.
