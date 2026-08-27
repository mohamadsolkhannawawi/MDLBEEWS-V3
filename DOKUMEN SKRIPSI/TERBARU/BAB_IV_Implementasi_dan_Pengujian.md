# BAB IV
# IMPLEMENTASI DAN PENGUJIAN

Bab ini berisi hasil implementasi sistem sesuai rancangan pada Bab III beserta hasil pengujian dan pembahasannya, mencakup hasil pengujian performa sistem pada tiap skenario serta analisis *overhead* yang ditimbulkan oleh instrumentasi Prometheus.

> **Catatan verifikasi sumber data (wajib dibaca sebelum menyalin ke draf resmi):** Berbeda dengan sesi-sesi penulisan sebelumnya, pada sesi ini kode sumber sistem beserta hasil pengujian mentah (berkas CSV) telah tersedia secara nyata (lihat berkas `MDLBEEWS.zip`). Oleh karena itu, seluruh potongan kode pada Sub Bab 4.3 dikutip **langsung dari implementasi nyata**, bukan kerangka representatif karangan, dan seluruh angka pada Sub Bab 4.6 dihitung **langsung dari data CSV hasil pengujian nyata** (`tests/results/*.csv`) menggunakan metode statistik deskriptif yang sama dengan yang dipakai skrip `tests/analyze_s1.py` milik proyek (mean, median, standar deviasi, P95, dengan nilai kosong/`nan` diperlakukan sebagai *missing*, bukan nol). Meskipun demikian, beberapa keterbatasan penting ditemukan pada data hasil pengujian yang tersedia — terutama terkait jumlah *trial* dan kelengkapan variabel bebas tiap skenario — dan keterbatasan tersebut disampaikan secara eksplisit pada bagian pembahasan masing-masing skenario serta pada Sub Bab 4.7, alih-alih disembunyikan atau ditutupi dengan interpretasi yang berlebihan. Spesifikasi mesin fisik (CPU, RAM, penyimpanan) tidak tercatat secara presisi pada dokumentasi proyek sehingga tetap ditandai `[SPESIFIKASI PERANGKAT]`.

## 4.1 Lingkungan Implementasi

Implementasi sistem dilakukan pada satu mesin *host* yang menjalankan Docker Desktop di atas sistem operasi Windows, sebagaimana ditunjukkan oleh penggunaan *counter* performa khas Windows (`Get-Counter \Processor(_Total)\% Processor Time` dan `\Memory\Available MBytes`) pada skrip pengumpulan data dasar (Sub Bab 4.5). Seluruh modul dijalankan sebagai *container* Docker yang saling terhubung melalui jaringan Docker Compose tunggal, mengikuti prinsip modularitas dan skalabilitas horizontal yang telah ditetapkan pada Sub Bab 3.2. Persyaratan minimum yang didokumentasikan pada panduan pengujian internal proyek adalah 4 *vCPU*, RAM 8 GB, dan ruang penyimpanan kosong 30 GB, sedangkan spesifikasi presisi mesin yang benar-benar digunakan belum dicatat secara terpisah sehingga ditandai sebagai `[SPESIFIKASI PERANGKAT]` pada Tabel 4.1.

Tabel 4.1 merangkum lingkungan implementasi yang benar-benar digunakan, diambil langsung dari berkas konfigurasi `docker-compose.yml`, `Dockerfile`, dan `requirements.txt`/`package.json` proyek, sehingga nomor versi yang dicantumkan mencerminkan versi yang telah dikunci (*pinned*) pada implementasi, bukan versi yang masih berupa rencana sebagaimana dicatat pada dokumen kerja tahap perancangan.

**Tabel 4.1 Spesifikasi Lingkungan Implementasi**

| Kategori | Komponen | Spesifikasi |
|---|---|---|
| Perangkat keras *host* | CPU | `[SPESIFIKASI PERANGKAT]` |
| | RAM | `[SPESIFIKASI PERANGKAT]` (kebutuhan minimum terdokumentasi: 8 GB) |
| | Penyimpanan | `[SPESIFIKASI PERANGKAT]` (kebutuhan minimum terdokumentasi: 30 GB ruang kosong) |
| Sistem operasi *host* | — | Windows dengan Docker Desktop (versi build `[SPESIFIKASI PERANGKAT]`) |
| *Container runtime* | — | Docker Engine + Docker Compose Plugin |
| Bahasa pemrograman | Modul berbasis Python | Python 3.10 (*image* dasar `python:3.10-slim-bookworm`/`python:3.10.14-bullseye`) |
| | Modul berbasis Node.js | Node.js 20 (*image* dasar `node:20-slim`) |
| Pustaka inti Python | Pemrosesan seismik | `obspy==1.4.1`, `numpy==1.24.4` |
| | *Deep learning* | `tensorflow==2.10.0` |
| | Kafka *client* | `kafka-python-ng==2.2.3` |
| | Observabilitas | `prometheus_client==0.21.1` |
| | *Web framework* (WebSocket Server FastAPI) | `fastapi==0.115.8`, `uvicorn==0.34.0` |
| | *HTTP client* (Load Balancer) | `requests==2.32.3` |
| Pustaka inti Node.js | *Web framework* & WebSocket | `express ^4.21.2`, `socket.io ^4.8.1` |
| | Kafka *client* | `kafkajs ^2.2.4` |
| | Observabilitas | `prom-client ^15.1.3` |
| *Message broker* | Kafka + Zookeeper | `confluentinc/cp-kafka:7.7.1`, `confluentinc/cp-zookeeper:7.7.1` (3 *broker* Kafka) |
| Basis data | Arsip dokumen | `mongo:7` + `mongo-express:latest` |
| | *Time-series* arsip | `influxdb:2.7` |
| *Load balancer* HTTP | NGINX | `nginx:1.27` (hanya aktif pada varian pengujian S4 dengan NGINX) |
| Observabilitas (kontribusi utama) | Prometheus Server | `prom/prometheus:v2.54.1` |
| | Node Exporter | `prom/node-exporter:v1.8.2` |
| | Grafana Dashboard | `grafana/grafana:11.2.2` |

Struktur direktori proyek pada tahap implementasi telah merealisasikan seluruh "rencana penambahan" yang sebelumnya masih berstatus rancangan pada dokumen konteks aplikasi, yaitu direktori `prometheus/` berisi `prometheus.yml` dan direktori `grafana/` berisi berkas provisioning *datasource*/*dashboard* beserta definisi *dashboard* JSON. Direktori inti pipeline EEWS (`data_provider/`, `p_wave_detector/`, `p_wave_detector_load_balance/`, `load_balancer/`, `loc_mag_detector/`, `data_archiver/`, `api_server/`, `fast_api/`, `nginx/`) tetap dipertahankan sesuai struktur rancangan awal, ditambah direktori `tests/` yang berisi skrip otomatisasi pengumpulan data (`collect_metrics.py`, `collect_host_metrics.ps1`, `run_all_tests.ps1`) dan skrip analisis (`analyze_s1.py`) yang digunakan pada Sub Bab 4.5 dan 4.6.

## 4.2 Implementasi Arsitektur Sistem

Realisasi arsitektur sistem secara umum konsisten dengan rancangan pada Tabel 3.2 Bab III, tanpa perbedaan mendasar pada topologi modul maupun protokol komunikasi antar-layanan. Seluruh sembilan modul inti (Data Provider, P-Wave Detector mode *consumer*, P-Wave Detector mode *load-balanced*, Load Balancer, Location & Magnitude Detector, Data Archiver, WebSocket Server Express.js/Socket.IO, WebSocket Server FastAPI, dan NGINX) berhasil diimplementasikan sebagai *container* Docker independen, ditambah tiga *container* lapisan observabilitas (Prometheus Server, Node Exporter, Grafana Dashboard) yang seluruhnya terhubung pada jaringan Docker Compose yang sama.

Satu detail realisasi yang perlu ditegaskan agar tidak menimbulkan kesalahpahaman saat membandingkan dengan rancangan Bab III adalah bahwa jalur *load-balanced* (P-Wave Detector mode *load-balanced*, Load Balancer, dan NGINX) tidak diaktifkan secara permanen bersamaan dengan jalur *consumer* pada konfigurasi `docker-compose.yml` utama yang dipakai sehari-hari. Ketiga komponen tersebut dikomentari (*commented out*) pada konfigurasi utama dan baru diaktifkan secara eksplisit melalui berkas konfigurasi Docker Compose terpisah yang khusus dipakai saat menjalankan skenario S4 (`docker-compose-2-1.yml` untuk konfigurasi Kafka saja dan `docker-compose-2-2.yml` untuk konfigurasi Kafka+NGINX). Pendekatan ini bukan penyimpangan dari rancangan Bab III, melainkan realisasi teknis dari prinsip satu variabel bebas per skenario pengujian (Sub Bab 3.1): setiap konfigurasi *load balancing* diisolasi ke dalam berkas Compose tersendiri agar dapat diaktifkan dan dinonaktifkan secara terkendali saat prosedur *reset* antar-skenario pada Sub Bab 3.5 dijalankan.

Pemetaan modul ke komponen Docker yang benar-benar berjalan ditunjukkan pada Tabel 4.2, diambil langsung dari definisi *service* pada `docker-compose.yml` beserta varian S4-nya.

**Tabel 4.2 Pemetaan Modul ke Komponen Docker**

| Modul/Fungsi | Nama *Service* | *Image*/Base | Port (*host:container*) | *Dependency* Utama |
|---|---|---|---|---|
| Koordinasi Kafka | `zookeeper` | `confluentinc/cp-zookeeper:7.7.1` | `2182:2181` | — |
| *Message broker* (3 *broker*) | `kafka1`, `kafka2`, `kafka3` | `confluentinc/cp-kafka:7.7.1` | `9092:9092`, `9093:9093`, `9094:9094` | `zookeeper` |
| Arsip dokumen | `mongo`, `mongo-express` | `mongo:7`, `mongo-express:latest` | `27017:27017`, `8081:8081` | `mongo` |
| Arsip *time-series* | `influxdb` | `influxdb:2.7` | `8086:8086` | — |
| Ingesti data seismik | `data_provider` | *build* dari `data_provider/Dockerfile` | `8101` (`/metrics`) | Kafka, SeedLink (GEOFON) |
| Deteksi gelombang-P (*consumer*) | `p_wave_detector` | *build* dari `p_wave_detector/Dockerfile` | `8102` (`/metrics`) | Kafka |
| Deteksi gelombang-P (*load-balanced*, hanya aktif pada S4) | `p_wave_detector_load_balance` | *build* dari `p_wave_detector_load_balance/Dockerfile` | `8004` (HTTP + `/metrics`) | Kafka |
| Distribusi beban (hanya aktif pada S4) | `load_balancer` | *build* dari `load_balancer/Dockerfile` | `8104` (`/metrics`) | Kafka, `p_wave_detector_load_balance` |
| *Reverse proxy* (hanya aktif pada S4 varian NGINX) | `nginx_load_balancer` | `nginx:1.27` | `8004:80` | `p_wave_detector_load_balance` |
| Estimasi lokasi & magnitudo | `loc_mag_detector` | *build* dari `loc_mag_detector/Dockerfile` | `8105` (`/metrics`) | Kafka |
| Pengarsipan data | `data_archiver` | *build* dari `data_archiver/Dockerfile` | `8106` (`/metrics`) | Kafka, MongoDB, InfluxDB |
| WebSocket Server (Express.js/Socket.IO) | `api_server` | *build* dari `api_server/Dockerfile` | `3333:3333`, `8107:8107` (`/metrics`) | Kafka |
| WebSocket Server (FastAPI) | `fast_api` | *build* dari `fast_api/Dockerfile` | `3334:3333`, `8108:3333` (`/metrics`) | Kafka |
| Pengumpulan metrik | `prometheus` | `prom/prometheus:v2.54.1` | `9090:9090` | Seluruh modul di atas |
| Metrik level *host* | `node-exporter` | `prom/node-exporter:v1.8.2` | `9100:9100` | — |
| Visualisasi *dashboard* | `grafana` | `grafana/grafana:11.2.2` | `4000:3000` | `prometheus`, `influxdb` |

Tabel 4.2 menunjukkan bahwa setiap modul EEWS mengekspos endpoint `/metrics` pada port unik (rentang 8101–8108), konsisten dengan rancangan Sub Bab 3.4.2 yang menegaskan tidak boleh terjadi tumpang tindih antar-*scrape target*. Konfigurasi *health check* juga diterapkan pada tiap `Dockerfile` modul Python maupun Node.js, sehingga Prometheus Server hanya mulai melakukan *scraping* setelah *container* target berstatus siap, sesuai prinsip yang telah dijelaskan pada Sub Bab 3.4.4.

## 4.3 Implementasi Source Code Kunci

Sub bab ini menyajikan potongan kode representatif dari implementasi nyata untuk lima aspek instrumentasi kunci sesuai rancangan Sub Bab 3.4.2. Format penyajian mengikuti aturan template Source Code (tabel dua baris satu kolom, font Courier New 10 pt, tanpa caption/nomor daftar); karena keterbatasan format Markdown pada draf kerja ini, potongan kode disajikan sebagai blok kode yang perlu dipindahkan ke format tabel Source Code resmi saat penyusunan naskah akhir.

Potongan kode pertama menunjukkan inisialisasi metrik Prometheus (`Counter`, `Gauge`, `Histogram`) pada modul P-Wave Detector mode *consumer*. Inisialisasi ini dilakukan secara kondisional terhadap *flag* `ENABLE_METRICS`, sehingga instrumentasi dapat dinonaktifkan sepenuhnya tanpa mengubah logika inti modul — mekanisme inilah yang memungkinkan skenario S1 (Sub Bab 4.6.1) membandingkan kondisi dengan dan tanpa instrumentasi menggunakan basis kode yang identik.

```python
if ENABLE_METRICS:
    from prometheus_client import start_http_server, Counter, Gauge, Histogram

    PWAVE_REQUESTS = Counter(
        'pwave_requests_total',
        'Total number of trace messages received for P-wave detection'
    )
    PWAVE_DETECTIONS = Counter(
        'pwave_detections_total',
        'Total number of positive P-wave detections'
    )
    PWAVE_ERRORS = Counter(
        'pwave_inference_errors_total',
        'Total number of inference errors'
    )
    PWAVE_CACHE_SIZE = Gauge(
        'pwave_waveform_cache_size',
        'Number of station-channel entries in waveform cache'
    )
    PWAVE_INFERENCE_LATENCY = Histogram(
        'pwave_inference_latency_seconds',
        'Latency of P-wave model inference',
        buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
    )
    PWAVE_E2E_LATENCY = Histogram(
        'pwave_end_to_end_latency_seconds',
        'End-to-end latency from data provider to P-wave detection',
        buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0]
    )
```

Empat jenis metrik pada potongan kode di atas mewakili pola instrumentasi yang diterapkan secara konsisten di seluruh modul: `Counter` untuk kuantitas kumulatif (permintaan, deteksi positif, *error*), `Gauge` untuk kondisi terkini (ukuran *cache*), dan `Histogram` untuk distribusi latensi dengan *bucket* yang disesuaikan skala waktu tiap proses — *bucket* inferensi model berada pada rentang mili-detik hingga beberapa detik, sedangkan *bucket* latensi *end-to-end* diperluas hingga puluhan detik karena mencakup keseluruhan jalur Kafka.

Potongan kode kedua menunjukkan penyediaan endpoint `/metrics` pada modul yang berbasis *web framework* (bukan `start_http_server` terpisah), diambil dari implementasi P-Wave Detector mode *load-balanced* berbasis FastAPI.

```python
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    if ENABLE_METRICS:
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
    return Response(content="Metrics disabled", status_code=404)
```

Modul yang tidak berbasis *web framework*, seperti P-Wave Detector mode *consumer* dan Load Balancer, sebaliknya menggunakan `start_http_server` dari `prometheus_client` yang dipanggil satu kali pada blok `if __name__ == '__main__':` untuk membuka *server* HTTP metrik pada *thread* terpisah, sebagaimana ditunjukkan pada potongan berikut dari modul Load Balancer.

```python
if __name__ == '__main__':
    if ENABLE_METRICS:
        try:
            start_http_server(METRICS_PORT_LOAD_BALANCER)
            logger.info(f"Prometheus metrics server started on port {METRICS_PORT_LOAD_BALANCER}")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")
```

Potongan kode ketiga menunjukkan logika inti pada jalur kritis yang telah diidentifikasi pada analisis kebutuhan Sub Bab 3.2, yaitu handler `POST /trace` pada P-Wave Detector mode *load-balanced* yang dipanggil oleh Load Balancer.

```python
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
```

Sebagai pasangan sisi pengirim pada jalur kritis yang sama, potongan kode berikut menunjukkan logika distribusi pada Load Balancer yang meneruskan pesan dari Kafka ke endpoint di atas melalui HTTP sekaligus mencatat latensi *forward*-nya.

```python
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
```

Potongan kode keempat menunjukkan konfigurasi `prometheus.yml`, khususnya *scrape target* untuk modul P-Wave Detector mode *consumer* yang menggunakan `dns_sd_configs` (DNS *service discovery*) agar dapat men-*scrape* seluruh replika modul secara otomatis tanpa perlu mencantumkan alamat IP setiap replika secara manual — mekanisme ini menjadi prasyarat teknis bagi skenario S2 (Sub Bab 4.6.2) yang memvariasikan jumlah *instance*.

```yaml
global:
  scrape_interval: 5s
  evaluation_interval: 5s
  scrape_timeout: 4s

scrape_configs:
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
        labels:
          instance: 'docker-host'

  - job_name: 'p_wave_detector'
    dns_sd_configs:
      - names: ['p_wave_detector']
        type: 'A'
        port: 8102
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
```

Potongan kode kelima menunjukkan definisi *service* Prometheus, Node Exporter, dan Grafana pada `docker-compose.yml`, termasuk *volume* untuk retensi data metrik dan *provisioning dashboard* Grafana secara otomatis.

```yaml
prometheus:
  image: prom/prometheus:v2.54.1
  container_name: prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    - prometheus_data:/prometheus
  command:
    - '--config.file=/etc/prometheus/prometheus.yml'
    - '--storage.tsdb.path=/prometheus'
    - '--storage.tsdb.retention.time=30d'
  restart: always

node-exporter:
  image: prom/node-exporter:v1.8.2
  container_name: node-exporter
  ports:
    - "9100:9100"
  volumes:
    - /proc:/host/proc:ro
    - /sys:/host/sys:ro
    - /:/rootfs:ro
  restart: always

grafana:
  image: grafana/grafana:11.2.2
  container_name: grafana
  ports:
    - "4000:3000"
  volumes:
    - grafana_data:/var/lib/grafana
    - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources:ro
    - ./grafana/provisioning/dashboards:/etc/grafana/provisioning/dashboards:ro
    - ./grafana/dashboards:/var/lib/grafana/dashboards:ro
  restart: always
  depends_on:
    - prometheus
    - influxdb
```

## 4.4 Implementasi Dashboard Grafana

Dashboard Grafana yang diberi nama "EEWS Observability Dashboard" berhasil dibangun dan diprovisikan secara otomatis melalui berkas `grafana/provisioning/datasources/datasources.yml` dan `grafana/dashboards/eews-observability.json`, dengan *datasource* Prometheus yang terpisah secara eksplisit dari *datasource* InfluxDB yang telah lebih dahulu digunakan untuk data arsip seismik, sesuai penegasan pada Sub Bab 3.4.3. Tangkapan layar utuh dashboard ditandai sebagai `[LAMPIRAN GAMBAR DASHBOARD]` karena berkas gambar tangkapan layar dilampirkan secara terpisah dari sesi penulisan ini.

Dashboard tersusun atas lima kelompok panel, sesuai urutan baris (*row*) pada definisi JSON-nya, yang dipetakan ke kategori metrik sebagai berikut.

**Kelompok 1 — Ringkasan Pipeline.** Panel "Traces Sent (Data Provider)" menampilkan laju pengiriman *trace* melalui kueri `rate(data_provider_traces_sent_total[1m])`; panel "P-Wave Detections Rate" membandingkan laju deteksi mode *consumer* (`rate(pwave_detections_total[1m])`) dan mode *load-balanced* (`rate(pwave_lb_detections_total[1m])`) dalam satu grafik *time-series*; panel "Loc-Mag Estimations Rate" menampilkan `rate(locmag_estimations_total[1m])`.

**Kelompok 2 — Latensi.** Panel "P-Wave Inference Latency (P95)" memetakan `histogram_quantile(0.95, rate(pwave_inference_latency_seconds_bucket[5m]))` beserta P50-nya untuk mode *consumer*, ditambah P95 mode *load-balanced* dalam grafik yang sama. Panel "Load Balancer Forward Latency (P95)" memetakan `histogram_quantile(0.95, rate(lb_forward_latency_seconds_bucket[5m]))`. Panel "Loc-Mag Inference Latency (P95)" memetakan `histogram_quantile(0.95, rate(locmag_inference_latency_seconds_bucket[5m]))`. Panel "End-to-End Data Delay" memetakan P95 dari `pwave_end_to_end_latency_seconds_bucket` dan `locmag_end_to_end_latency_seconds_bucket` sekaligus, menjadi panel kunci untuk memantau variabel terikat *data delay end-to-end*. Panel "Data Archiver Write Latency" memetakan `histogram_quantile(0.95, rate(archiver_write_latency_seconds_bucket[5m]))` per jenis *storage*.

**Kelompok 3 — Penggunaan Sumber Daya (*Host*).** Panel "CPU Usage (%)" memetakan `100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)`, sedangkan panel "Memory Usage (MB)" memetakan `(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / 1024 / 1024` — kedua kueri inilah yang juga menjadi dasar pengumpulan data CPU/memori pada seluruh skenario S1–S4 Sub Bab 4.6.

**Kelompok 4 — WebSocket dan Error.** Panel "Active WebSocket Clients" bertipe *gauge*, memetakan `ws_active_clients` (Express.js) dan `fastapi_ws_active_clients` (FastAPI) berdampingan, sesuai rancangan visualisasi *gauge* untuk nilai terkini pada Sub Bab 3.4.3. Panel "WebSocket Broadcast Rate" memetakan laju *broadcast* kedua varian WebSocket Server. Panel "Error Rates (All Modules)" mengagregasi laju *error* dari kelima modul (`data_provider`, `p_wave_detector`, `load_balancer`, `loc_mag_detector`, `data_archiver`) dalam satu grafik untuk mempermudah deteksi anomali lintas-modul.

Seluruh panel di atas menggunakan jenis visualisasi *time-series* untuk metrik yang berubah terhadap waktu, kecuali panel "Active WebSocket Clients" yang menggunakan *gauge*, konsisten dengan rancangan Sub Bab 3.4.3. Visualisasi *heatmap* distribusi latensi yang sempat direncanakan pada tahap perancangan belum termasuk dalam definisi *dashboard* JSON yang berhasil diimplementasikan sampai sesi penulisan ini, sehingga disebutkan di sini sebagai catatan realisasi yang berbeda dari rancangan awal.

## 4.5 Lingkungan Pengujian

Pengujian dilaksanakan pada mesin *host* yang sama dengan lingkungan implementasi pada Sub Bab 4.1 (`[SPESIFIKASI PERANGKAT]` untuk rincian CPU/RAM/penyimpanan), tanpa mesin khusus terpisah untuk *server* dan klien pengujian. Kondisi jaringan menggunakan jaringan *bridge* internal Docker Compose tanpa alat simulasi gangguan jaringan (seperti pembatasan *bandwidth* atau *latency injection*) yang diaktifkan secara eksplisit, sehingga hasil pengujian mencerminkan kondisi jaringan lokal ideal, bukan kondisi jaringan produksi yang lebih bervariasi. Dataset seismik yang digunakan bersumber dari data historis/*real-time* yang diakses melalui SeedLink server publik GEOFON (GFZ Potsdam, `geofon.gfz-potsdam.de:18000`) menggunakan pustaka ObsPy, sesuai Ruang Lingkup Bab I yang menyatakan penggunaan data simulasi/historis, bukan sensor fisik langsung.

Prosedur eksekusi pengujian diotomatisasi melalui skrip `tests/run_all_tests.ps1`, yang menjalankan empat tahap berurutan untuk tiap skenario: (1) menghentikan seluruh *container* dari kelima kemungkinan berkas Docker Compose (`docker compose -f <file> down -v`) agar kondisi awal bersih tanpa sisa *volume*, (2) menyalakan *container* sesuai berkas Compose skenario yang bersangkutan (`docker compose -f <file> up -d --build`), (3) menunggu 60 detik agar seluruh *service* stabil, dan (4) menjalankan pengumpulan metrik selama 120 detik dengan interval pengambilan sampel 5 detik menggunakan `tests/collect_metrics.py` (atau `collect_host_metrics.ps1` khusus untuk kondisi tanpa Prometheus pada S1a), sesuai kerangka otomatisasi eksperimen *reusable* yang dirujuk pada Sub Bab 3.5. Data metrik diambil melalui Prometheus API menggunakan sepuluh kueri PromQL tetap (mencakup CPU, memori, latensi inferensi tiap modul, *data delay end-to-end*, dan jumlah klien WebSocket aktif) yang didefinisikan secara terpusat pada skrip pengumpul, sehingga metodologi pengumpulan data identik lintas skenario S1b–S4.

**Catatan keterbatasan jumlah *trial*:** Berdasarkan `tests/run_all_tests.ps1`, setiap skenario (S1a, S1b, S2, S3, S4a, S4b) pada dataset yang tersedia baru dijalankan sebanyak **satu kali** (*single trial*), berbeda dengan prinsip "jumlah *trial* yang memadai untuk menjaga stabilitas statistik" yang ditetapkan pada Sub Bab 3.5. Nilai standar deviasi yang dilaporkan pada Sub Bab 4.6 karenanya dihitung dari variasi sampel *time-series* dalam satu *trial* (24 sampel per 120 detik pengujian), bukan dari variasi antar-*trial* yang berulang. Implikasi keterbatasan ini disampaikan lebih lanjut pada Sub Bab 4.7.

## 4.6 Hasil Pengujian per Skenario

### 4.6.1 Hasil Pengujian S1 — Overhead Instrumentasi Prometheus

Skenario S1 bertujuan mengukur selisih penggunaan CPU, memori, dan latensi antara kondisi tanpa dan dengan instrumentasi `prometheus_client` aktif di seluruh modul. Prosedur pelaksanaan mengikuti Tabel 3.3: variabel bebas berupa aktif/tidaknya `prometheus_client` (`ENABLE_METRICS=false` pada `docker-compose-5-1.yml` untuk kondisi S1a, `ENABLE_METRICS=true` pada `docker-compose-5-2.yml` untuk kondisi S1b), dengan beban data seismik konstan (*smooth*) dari `data_provider` sebagai variabel kontrol.

Tabel 4.3 menyajikan hasil perbandingan S1a (tanpa metrik) dan S1b (dengan metrik), dihitung dari `tests/results/s1a_no_metrics.csv` (18 sampel) dan `tests/results/s1b_with_metrics.csv` (24 sampel).

**Tabel 4.3 Hasil Pengujian S1 — Perbandingan CPU dan Memori**

| Metrik | S1a — Tanpa Metrik (*mean*) | S1b — Dengan Metrik (*mean*) | Perubahan Absolut | Perubahan (%) |
|---|---|---|---|---|
| CPU (%) | 55,8120 | 37,8533 | −17,9587 pp | −32,18% |
| Memori (MB) | 25.342,56 | 8.684,61 | −16.657,94 MB | −65,73% |

Tabel 4.4 melengkapi Tabel 4.3 dengan metrik latensi level-aplikasi yang hanya tersedia pada kondisi S1b, karena metrik tersebut berasal dari `prometheus_client` yang justru dinonaktifkan pada S1a — sehingga metrik ini berstatus `no_baseline` dan tidak dapat dihitung selisihnya terhadap S1a, hanya dilaporkan sebagai nilai deskriptif kondisi S1b.

**Tabel 4.4 Hasil Pengujian S1 — Latensi Level-Aplikasi (Hanya Tersedia pada S1b)**

| Metrik | *Mean* | Median | P95 | Data Valid/Total |
|---|---|---|---|---|
| Latensi inferensi P-Wave (s) | 1,2954 | 0,8030 | 0,975 (histogram) | 24/24 |
| Latensi inferensi Loc-Mag (s) | 0,7696 | 0,9375 | 0,975 (histogram) | 14/24 |
| *Data delay end-to-end* Loc-Mag (s) | 5,1875 | 4,8750 | 6,4062 | 14/24 |
| Klien WebSocket aktif (Express.js) | 1,0 | 1,0 | 1,0 | 24/24 |

Hasil pada Tabel 4.3 menunjukkan arah yang **berlawanan** dengan hipotesis *overhead* yang lazim ditemukan pada literatur: penggunaan CPU dan memori pada kondisi dengan instrumentasi (S1b) justru lebih rendah dibandingkan kondisi tanpa instrumentasi (S1a), bukan lebih tinggi. Faseeha dkk. (2025) melaporkan bahwa *overhead* CPU/memori kerangka kerja observabilitas modern secara umum berada pada kisaran di bawah 5% (misalnya 1,4–4,53% untuk kerangka berbasis eBPF maupun instrumentasi level-aplikasi), sehingga hasil selisih −32,18% pada S1 tidak sejalan dengan pola yang diharapkan dan perlu diinterpretasikan secara hati-hati, bukan disimpulkan begitu saja sebagai bukti bahwa instrumentasi Prometheus "menghemat" sumber daya sistem.

Interpretasi yang lebih beralasan mengarah pada kemungkinan perancu (*confounding factor*) metodologis, bukan efek nyata dari instrumentasi. Pertama, S1a dan S1b diukur menggunakan alat ukur yang berbeda — S1a menggunakan *counter* performa Windows (`Get-Counter`) yang berjalan di *host* dan diambil dengan interval serta durasi yang sedikit berbeda (18 sampel dibanding 24 sampel), sedangkan S1b menggunakan kueri PromQL terhadap Node Exporter, sehingga kedua rangkaian data tidak sepenuhnya *apple-to-apple*. Kedua, kedua kondisi dijalankan sebagai dua siklus *container* yang terpisah dan berurutan (bukan diacak/*counterbalanced*), sehingga kondisi awal sistem (proses *warm-up* pemuatan model *deep learning*, status *cache* Docker, maupun proses latar belakang lain pada *host*) berpotensi berbeda antara kedua *run* dan ikut memengaruhi angka CPU/memori yang teramati. Ketiga, dengan hanya satu *trial* per kondisi (Sub Bab 4.5), tidak dapat dipastikan apakah selisih besar ini konsisten atau hanya kebetulan pada *run* tersebut. Ketiga faktor ini menjadi dasar rekomendasi pada Sub Bab 4.7 agar S1 diulang dengan *trial* berganda dan alat ukur yang seragam sebelum kesimpulan mengenai arah *overhead* dapat ditarik secara meyakinkan.

Tabel 4.4 tetap memberikan informasi yang berguna secara independen dari perbandingan *overhead*: latensi inferensi P-Wave rata-rata di bawah 1,3 detik dan *data delay end-to-end* rata-rata sekitar 5,2 detik pada kondisi instrumentasi aktif menunjukkan bahwa penambahan instrumentasi tidak menghalangi jalur pemrosesan utama untuk tetap berjalan pada orde waktu yang wajar untuk sistem *time-critical* seperti EEWS, sekalipun besaran ini belum dibandingkan langsung terhadap ambang batas target yang dikunci (Sub Bab 3.2).

### 4.6.2 Hasil Pengujian S2 — Skalabilitas Multi-Container

Skenario S2 bertujuan mengamati *data delay end-to-end* serta penggunaan CPU/memori agregat saat jumlah *instance* P-Wave Detector/Data Archiver divariasikan, dengan beban data seismik konstan yang dinaikkan bertahap mengikuti jumlah *instance* sesuai Tabel 3.3. Konfigurasi multi-*instance* (`docker-compose-3-1.yml` hingga `docker-compose-3-13.yml`) yang memvariasikan jumlah replika P-Wave Detector *load-balanced* dan Data Archiver (antara 4–5 replika pada berkas-berkas yang diperiksa) telah tersedia di repositori proyek, namun `tests/run_all_tests.ps1` pada dataset yang tersedia hanya menjalankan pengumpulan data S2 menggunakan `docker-compose.yml` baku, yaitu konfigurasi *default* satu *instance* per modul.

Tabel 4.5 menyajikan hasil deskriptif dari `tests/results/s2_scalability.csv` (24 sampel, konfigurasi *default*).

**Tabel 4.5 Hasil Pengujian S2 — Konfigurasi Default (Satu *Instance* per Modul)**

| Metrik | *Mean* | Median | P95 | Data Valid/Total |
|---|---|---|---|---|
| CPU (%) | 39,3745 | 47,4971 | 52,8375 | 24/24 |
| Memori (MB) | 8.845,02 | 9.107,65 | 10.799,82 | 24/24 |
| Latensi inferensi P-Wave (s) | 1,5622 | 0,9210 | 4,9873 | 24/24 |
| Latensi inferensi Loc-Mag (s) | 0,6029 | 0,8500 | 0,975 | 18/24 |
| *Data delay end-to-end* P-Wave (s) | 12,8432 | 2,4250 | 58,5 | 11/24 |
| *Data delay end-to-end* Loc-Mag (s) | 35,1250 | 55,1250 | 56,25 | 18/24 |

Pembahasan hasil S2 pada dataset yang tersedia perlu dibatasi pada apa yang benar-benar dapat didukung oleh data: karena hanya satu konfigurasi jumlah *instance* yang terekam, Tabel 4.5 **belum dapat menjawab pertanyaan skalabilitas** sebagaimana dirumuskan pada Tabel 3.3 (yaitu bagaimana metrik berubah seiring bertambahnya jumlah *instance*), dan baru memberikan gambaran karakteristik satu titik data pada kondisi *default*. Meskipun demikian, pola temporal di dalam satu *run* tersebut tetap informatif: nilai *data delay end-to-end* Loc-Mag naik dari 4,875 detik pada awal jendela pengujian menjadi 55,5–56,25 detik menjelang akhir jendela 120 detik, mengindikasikan penumpukan antrean (*backlog*) pada jalur pemrosesan satu-*instance* saat beban data seismik terus mengalir tanpa jeda. Pola kenaikan progresif ini justru memperkuat motivasi teknis di balik penyediaan konfigurasi multi-*instance* pada `docker-compose-3-x.yml`: penambahan jumlah *instance* P-Wave Detector/Data Archiver secara konseptual diharapkan menahan laju kenaikan *backlog* tersebut, sebagaimana disinggung Al Qassem dkk. (2024) mengenai peran skalabilitas horizontal dalam arsitektur *microservices* yang menghadapi beban tinggi — namun klaim ini baru bersifat dugaan teoretis sampai konfigurasi multi-*instance* benar-benar diukur dan dibandingkan.

### 4.6.3 Hasil Pengujian S3 — Perbandingan Implementasi WebSocket Server

Skenario S3 bertujuan membandingkan *data delay*, CPU, memori, dan jumlah klien aktif antara implementasi WebSocket Server Express.js/Socket.IO dan FastAPI di bawah beban klien bertingkat, dengan konfigurasi `docker-compose.yml` baku yang menjalankan kedua varian WebSocket Server secara bersamaan.

Tabel 4.6 menyajikan hasil deskriptif dari `tests/results/s3_websocket.csv` (24 sampel).

**Tabel 4.6 Hasil Pengujian S3 — Perbandingan Express.js vs FastAPI**

| Metrik | *Mean* | Median | P95 | Data Valid/Total |
|---|---|---|---|---|
| CPU (%) | 39,9329 | 48,1293 | 52,2448 | 24/24 |
| Memori (MB) | 8.781,27 | 8.851,84 | 10.576,54 | 24/24 |
| Latensi inferensi P-Wave (s) | 3,5822 | 5,0000 | 5,0 | 24/24 |
| Latensi inferensi Loc-Mag (s) | 0,5169 | 0,4875 | 0,975 | 22/24 |
| *Data delay end-to-end* Loc-Mag (s) | 27,8489 | 39,0000 | 52,5 | 22/24 |
| Klien aktif — Express.js | 1,0 | 1,0 | 1,0 | 24/24 |
| Klien aktif — FastAPI | 0,0 | 0,0 | 0,0 | 24/24 |

Tabel 4.6 menunjukkan keterbatasan penting yang harus disampaikan secara jujur sesuai prinsip pelaporan pada Sub Bab 4.6: jumlah klien aktif pada varian FastAPI tercatat **konstan nol** di sepanjang jendela pengujian, sedangkan varian Express.js tercatat **konstan satu** klien. Kondisi ini menunjukkan bahwa perbandingan performa "di bawah beban klien bertingkat" sebagaimana dirancang pada Tabel 3.3 belum sepenuhnya terealisasi pada pengambilan data ini: hanya satu klien tunggal yang tersambung ke varian Express.js sepanjang pengujian, tanpa tahapan kenaikan jumlah klien secara bertahap, dan tidak ada klien yang tersambung sama sekali ke varian FastAPI. Akibatnya, Tabel 4.6 lebih tepat dibaca sebagai karakteristik satu klien tunggal pada varian Express.js dibandingkan sebagai perbandingan Express.js-vs-FastAPI yang valid, karena sisi FastAPI tidak memiliki data pembanding yang berarti untuk metrik yang bergantung pada aktivitas klien.

Nilai latensi inferensi P-Wave pada Tabel 4.6 juga menunjukkan saturasi yang mencolok, dengan median tepat berada di batas *bucket histogram* tertinggi (5,0 detik) yang tersedia pada definisi `Histogram` (lihat Sub Bab 4.3), mengindikasikan bahwa sebagian besar observasi latensi pada *window* pengukuran tersebut sesungguhnya melebihi 2,5 detik namun tidak dapat dibedakan presisinya lebih lanjut karena *bucket* histogram tidak menyediakan batas di atas 5,0 detik. Kenaikan progresif *data delay end-to-end* Loc-Mag dari 0,475 detik di awal jendela menjadi sekitar 52,5 detik menjelang akhir jendela menunjukkan pola penumpukan antrean yang serupa dengan temuan pada S2, memperkuat indikasi bahwa beban data seismik berkelanjutan pada konfigurasi satu-*instance* menjadi sumber utama kenaikan *delay*, terlepas dari varian WebSocket Server yang digunakan.

### 4.6.4 Hasil Pengujian S4 — Observabilitas Kafka + NGINX Load Balancer

Skenario S4 bertujuan membandingkan *data delay*, CPU, dan memori antara konfigurasi *load balancing* Kafka saja (S4a) dan konfigurasi Kafka+NGINX (S4b), di bawah profil beban *bursty* (lonjakan permintaan mendadak) sesuai Tabel 3.3. Prosedur pengujian menggunakan `docker-compose-2-1.yml` untuk S4a dan `docker-compose-2-2.yml` untuk S4b, dengan `nginx_load_balancer` (image `nginx:1.27`) hanya aktif pada S4b sesuai Tabel 4.2.

Tabel 4.7 menyajikan hasil deskriptif dari `tests/results/s4a_kafka_lb.csv` dan `tests/results/s4b_nginx_lb.csv` (masing-masing 24 sampel).

**Tabel 4.7 Hasil Pengujian S4 — Perbandingan Kafka Saja (S4a) vs Kafka+NGINX (S4b)**

| Metrik | S4a — Kafka Saja (*mean*) | S4b — Kafka+NGINX (*mean*) |
|---|---|---|
| CPU (%) | 41,5606 | 10,1035 |
| Memori (MB) | 10.000,30 | 5.085,85 |
| Latensi inferensi P-Wave (s) | 3,5854 (24/24 valid) | Tidak terekam (0/24 valid) |
| Latensi inferensi Loc-Mag (s) | 0,5870 (21/24 valid) | Tidak terekam (0/24 valid) |
| *Data delay end-to-end* Loc-Mag (s) | 2,7548 (21/24 valid) | Tidak terekam (0/24 valid) |
| Klien aktif — Express.js | 1,0 | 1,0 |

Tabel 4.7 menunjukkan selisih CPU dan memori yang besar antara S4a dan S4b, dengan S4b mencatat penggunaan sumber daya jauh lebih rendah. Namun, selisih ini **tidak dapat langsung diinterpretasikan sebagai keunggulan efisiensi konfigurasi Kafka+NGINX**, karena seluruh metrik latensi level-aplikasi pada S4b tercatat kosong sepanjang 24 sampel, menunjukkan bahwa modul-modul inti pipeline (P-Wave Detector, Location & Magnitude Detector) kemungkinan tidak sedang memproses lalu lintas data yang setara dengan S4a selama jendela pengujian S4b — dengan kata lain, CPU/memori yang lebih rendah pada S4b lebih mungkin mencerminkan beban kerja aktual yang lebih rendah atau kegagalan sebagian jalur pemrosesan untuk menerima data, bukan efisiensi arsitektural NGINX itu sendiri. Pola data mentah turut mendukung dugaan ini: CPU pada S4a naik progresif dari 13,9% menjadi sekitar 53% sepanjang jendela pengujian (mengindikasikan beban yang terus mengalir dan terproses), sedangkan CPU pada S4b relatif datar pada kisaran 9–18% sepanjang jendela, tanpa pola kenaikan yang sebanding.

Temuan ini menjadi salah satu keterbatasan paling signifikan pada dataset pengujian yang tersedia dan perlu ditindaklanjuti dengan pemeriksaan status *target* Prometheus (`/targets`) serta log modul terkait pada *run* S4b berikutnya, sebelum perbandingan Kafka-saja-vs-Kafka+NGINX dapat disimpulkan secara valid. Ma dan Kook (2022) menekankan bahwa evaluasi algoritma *load balancing* NGINX idealnya dilakukan dengan memastikan beban kerja yang setara pada kedua sisi pembanding; kondisi data S4b pada pengujian ini belum memenuhi prasyarat tersebut.

## 4.7 Analisis dan Pembahasan Keseluruhan

Sintesis lintas-skenario menunjukkan satu pola umum yang konsisten muncul pada S2, S3, dan S4a: *data delay end-to-end* cenderung meningkat secara progresif sepanjang jendela pengujian 120 detik pada konfigurasi satu-*instance*, mengindikasikan bahwa laju pemrosesan satu *instance* P-Wave Detector/Location & Magnitude Detector belum sepenuhnya mengimbangi laju masuknya data seismik pada beban yang diuji. Pola ini konsisten dengan pandangan Ranasinghe dkk. (2024) bahwa tantangan EEWS modern tidak hanya soal akurasi deteksi, melainkan juga ketahanan sistem terhadap gangguan operasional termasuk penumpukan beban — dan justru pola inilah yang menjadi salah satu nilai utama lapisan observabilitas yang dibangun penelitian ini: tanpa dashboard Grafana dan metrik *end-to-end delay* pada Sub Bab 4.4, kecenderungan penumpukan antrean semacam ini akan sulit terdeteksi lebih awal karena hanya tampak dari nilai agregat sesaat, bukan dari tren temporalnya.

Dikaitkan dengan Rumusan Masalah tunggal pada Sub Bab 1.2, hasil pengujian S1–S4 secara umum menunjukkan bahwa arsitektur observabilitas berbasis Prometheus dan Grafana yang dirancang berhasil diimplementasikan dan mampu mengumpulkan metrik latensi, CPU, memori, dan *data delay end-to-end* secara *real-time* melalui dashboard pada Sub Bab 4.4, sehingga dimensi "pemantauan performa secara *real-time*" pada Rumusan Masalah dapat dijawab secara afirmatif. Sebaliknya, dimensi "dianalisis secara *reproducible*" pada Rumusan Masalah yang sama **belum sepenuhnya terpenuhi** oleh dataset yang tersedia saat ini, mengingat setiap skenario baru dijalankan sebanyak satu *trial* (Sub Bab 4.5) sehingga stabilitas statistik lintas-*trial* belum dapat diverifikasi — sebuah kesenjangan yang secara langsung berkaitan dengan prinsip *reproducibility* Henning dan Hasselbring (2024) yang telah dirujuk pada Sub Bab 3.6. Terkait Tujuan Penelitian keempat mengenai besar *overhead* instrumentasi Prometheus, skenario S1 pada Sub Bab 4.6.1 memberikan angka kuantitatif (−32,18% CPU, −65,73% memori), namun arah hasil yang berlawanan dengan literatur pembanding (Faseeha dkk., 2025) membuat temuan ini belum dapat dijadikan simpulan akhir mengenai *overhead* Prometheus pada arsitektur EEWS, melainkan baru berupa temuan awal yang menuntut pengujian ulang dengan kontrol metodologis yang lebih ketat.

Keterbatasan yang ditemukan selama implementasi dan pengujian disampaikan secara eksplisit sebagai berikut, agar pembaca dapat menilai batas validitas temuan Bab IV secara proporsional.

1. Seluruh skenario S1–S4 baru dijalankan sebanyak satu *trial*, berbeda dengan prinsip jumlah *trial* memadai yang ditetapkan pada Sub Bab 3.5, sehingga nilai standar deviasi yang dilaporkan mencerminkan variasi intra-*trial* (antar-sampel dalam satu jendela 120 detik), bukan variasi antar-*trial* yang berulang.
2. Skenario S1 membandingkan dua kondisi menggunakan dua alat ukur CPU/memori yang berbeda (*counter* performa Windows untuk S1a, kueri Node Exporter untuk S1b) tanpa pengacakan urutan pengujian, sehingga selisih yang teramati berpotensi dipengaruhi perancu metodologis selain aktif/tidaknya instrumentasi itu sendiri.
3. Skenario S2 pada dataset yang tersedia baru mencakup satu konfigurasi jumlah *instance* (*default*, satu *instance* per modul), sehingga belum dapat menjawab pertanyaan skalabilitas multi-*instance* sebagaimana dirancang pada Tabel 3.3, meskipun konfigurasi multi-*instance* (`docker-compose-3-1.yml` hingga `docker-compose-3-13.yml`) telah tersedia di repositori proyek untuk pengujian lanjutan.
4. Skenario S3 belum merealisasikan profil "beban klien bertingkat" yang dirancang; jumlah klien WebSocket aktif tercatat konstan (satu klien pada Express.js, nol klien pada FastAPI) sepanjang jendela pengujian, sehingga perbandingan performa kedua varian WebSocket Server di bawah beban belum dapat disimpulkan dari data ini.
5. Skenario S4b (Kafka+NGINX) tidak berhasil merekam metrik latensi level-aplikasi sama sekali pada jendela pengujian yang tersedia, sehingga perbandingan efisiensi konfigurasi *load balancing* pada Sub Bab 4.6.4 terbatas pada metrik CPU/memori *host* dan berisiko dipengaruhi oleh perbedaan beban kerja aktual antara kedua *run*, bukan murni oleh perbedaan arsitektur *load balancing*.
6. Spesifikasi presisi mesin *host* implementasi dan pengujian belum didokumentasikan secara terpisah dari kebutuhan minimum sistem, sehingga ditandai sebagai `[SPESIFIKASI PERANGKAT]` pada Tabel 4.1 dan perlu dilengkapi sebelum naskah akhir disusun.

Keterbatasan-keterbatasan di atas tidak meniadakan kontribusi utama yang telah dicapai pada Bab IV ini, yaitu keberhasilan implementasi lapisan observabilitas Prometheus dan Grafana secara nyata di atas arsitektur *microservices* EEWS berbasis Kafka dan WebSocket, lengkap dengan instrumentasi metrik terstruktur pada seluruh modul dan dashboard yang informatif. Keterbatasan tersebut sebaliknya menjadi arahan konkret bagi putaran pengujian lanjutan — pengulangan *trial*, penyeragaman alat ukur, serta eksekusi konfigurasi multi-*instance* dan beban klien bertingkat yang sudah tersedia namun belum dijalankan — sebelum Bab IV versi final dan Bab V (Penutup) dapat menyusun simpulan yang sepenuhnya didukung data sesuai kaidah penelitian eksperimental kuantitatif pada Sub Bab 3.1.
