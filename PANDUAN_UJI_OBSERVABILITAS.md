# Panduan Pengujian Observabilitas EEWS — Skenario S1 hingga S4

Dokumen ini adalah panduan langkah-demi-langkah untuk melaksanakan seluruh pengujian BAB IV, mulai dari persiapan awal hingga semua file CSV output berhasil dikumpulkan. Skenario S1–S4 sesuai dengan Tabel 3.3 pada BAB III.

---

## Daftar Isi

1. [Prasyarat dan Persiapan Awal](#1-prasyarat-dan-persiapan-awal)
2. [Mengambil Source Code](#2-mengambil-source-code)
3. [Pemasangan Dependensi Python](#3-pemasangan-dependensi-python)
4. [Validasi Sistem Sebelum Pengujian](#4-validasi-sistem-sebelum-pengujian)
5. [Panduan Pengambilan Screenshot](#5-panduan-pengambilan-screenshot)
6. [S1 — Overhead Instrumentasi Prometheus](#6-s1--overhead-instrumentasi-prometheus)
7. [S2 — Skalabilitas Multi-Container](#7-s2--skalabilitas-multi-container)
8. [S3 — Perbandingan WebSocket Server](#8-s3--perbandingan-websocket-server)
9. [S4 — Kafka vs Kafka+NGINX Load Balancer](#9-s4--kafka-vs-kafkanginx-load-balancer)
10. [Menjalankan Semua Skenario Sekaligus](#10-menjalankan-semua-skenario-sekaligus)
11. [Checklist Output yang Harus Dikumpulkan](#11-checklist-output-yang-harus-dikumpulkan)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Prasyarat dan Persiapan Awal

### Software yang Wajib Terinstal

| Software                 | Versi Minimum | Cara Cek                    |
| ------------------------ | ------------- | --------------------------- |
| Docker Desktop (Windows) | 4.x           | `docker --version`          |
| Docker Compose Plugin    | 2.x           | `docker compose version`    |
| Python                   | 3.10+         | `python --version`          |
| Git                      | 2.x           | `git --version`             |
| PowerShell               | 5.1+          | `$PSVersionTable.PSVersion` |

### Spesifikasi Mesin yang Direkomendasikan

- RAM: minimum **16 GB** (seluruh stack berjalan bersamaan bisa menggunakan 8–12 GB)
- Penyimpanan kosong: minimum **30 GB**
- CPU: minimum 4 core (8 core untuk skenario multi-container)

### Izin PowerShell (lakukan sekali saja)

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 2. Mengambil Source Code

### Clone pertama kali

```powershell
git clone https://github.com/mohamadsolkhannawawi/MDLBEEWS-V3.git
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS"
```

### Update jika sudah pernah clone

```powershell
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS"
git pull origin main
```

### Siapkan file environment

```powershell
Copy-Item .env.example .env
Copy-Item influxDB\.env.example influxDB\.env
```

> **Catatan:** Jangan pernah meng-commit file `.env`. File ini berisi credential yang bersifat rahasia.

### Validasi konfigurasi

```powershell
docker compose config
```

Perintah ini harus selesai tanpa error. Jika ada error, periksa apakah file `.env` dan `influxDB/.env` sudah tersedia.

---

## 3. Pemasangan Dependensi Python

Semua skrip pengumpul metrik membutuhkan library berikut. Pasang sekali saja:

```powershell
pip install requests websockets
```

### Verifikasi

```powershell
python -c "import requests, websockets; print('OK')"
```

---

## 4. Validasi Sistem Sebelum Pengujian

Sebelum menjalankan skenario apapun, pastikan sistem berjalan dengan benar menggunakan langkah berikut.

### Langkah 4.1 — Jalankan docker compose utama

```powershell
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS"
docker compose up -d --build
```

Tunggu **60 detik** agar Kafka selesai startup dan memilih leader.

### Langkah 4.2 — Periksa status container

```powershell
docker compose ps
```

Container berikut **wajib** berstatus `Up (healthy)` atau `Up`:

| Container                      | Status Wajib |
| ------------------------------ | ------------ |
| `zookeeper`                    | Up           |
| `kafka1`, `kafka2`, `kafka3`   | Up           |
| `data_provider`                | Up           |
| `p_wave_detector` (instance-1) | Up           |
| `loc_mag_detector`             | Up           |
| `data_archiver` (instance-1)   | Up           |
| `api_server`                   | Up           |
| `fast_api`                     | Up           |
| `prometheus`                   | Up           |
| `grafana`                      | Up           |

### Langkah 4.3 — Periksa Prometheus

```powershell
# Prometheus harus menjawab "Prometheus Server is Ready."
curl.exe http://localhost:9090/-/ready

# Semua target utama harus bernilai 1
curl.exe "http://localhost:9090/api/v1/query?query=up" |
    ConvertFrom-Json |
    ConvertTo-Json -Depth 100
```

Buka `http://localhost:9090/targets` di browser. Semua service EEWS harus berstatus **UP** (hijau).

### Langkah 4.4 — Periksa Grafana

Buka `http://localhost:4000`. Login dengan `admin` / `12345678`. Pastikan dashboard **EEWS Observability** muncul dan panelnya menampilkan data.

### Langkah 4.5 — Periksa endpoint WebSocket dan metrik

```powershell
curl.exe http://localhost:3333
curl.exe http://localhost:3334/health
curl.exe http://localhost:8107/metrics
```

### URL Lengkap untuk Validasi

| Komponen             | URL                             | Login                |
| -------------------- | ------------------------------- | -------------------- |
| Express WebSocket UI | `http://localhost:3333`         | —                    |
| FastAPI WebSocket UI | `http://localhost:3334`         | —                    |
| Express Metrics      | `http://localhost:8107/metrics` | —                    |
| FastAPI Metrics      | `http://localhost:8108/metrics` | —                    |
| Prometheus Targets   | `http://localhost:9090/targets` | —                    |
| Prometheus Graph     | `http://localhost:9090/graph`   | —                    |
| Grafana              | `http://localhost:4000`         | `admin` / `12345678` |
| InfluxDB             | `http://localhost:8086`         | `admin` / `12345678` |
| Mongo Express        | `http://localhost:8081`         | `admin` / `password` |

---

## 5. Panduan Pengambilan Screenshot

Screenshot berikut wajib diambil **satu kali** setelah validasi sistem berhasil (Langkah 4), dan dapat dipakai untuk semua skenario.

| No  | Yang Difoto                             | Cara Mengambil                                                            |
| --- | --------------------------------------- | ------------------------------------------------------------------------- |
| 1   | Hasil `docker compose ps`               | Buka PowerShell, jalankan perintah, screenshot terminal                   |
| 2   | Halaman `http://localhost:3333`         | Browser, tampilkan data trace                                             |
| 3   | Halaman `http://localhost:3334`         | Browser, tampilkan koneksi WebSocket                                      |
| 4   | Halaman `http://localhost:8107/metrics` | Browser, tampilkan teks metrik mentah Prometheus                          |
| 5   | Halaman `http://localhost:9090/targets` | Browser, semua target harus UP (hijau)                                    |
| 6   | Prometheus Graph dengan query `up`      | Ketik `up` di kotak query, klik Execute                                   |
| 7   | Prometheus Graph CPU                    | Query: `100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)` |
| 8   | Grafana dashboard EEWS                  | Pilih time range **Last 15 minutes**                                      |
| 9   | InfluxDB Data Explorer                  | Buka bucket `eews`                                                        |
| 10  | Mongo Express                           | Buka collection data                                                      |

> **Penting:** Jangan tampilkan password, token, atau isi file `.env` pada screenshot manapun.

---

## 6. S1 — Overhead Instrumentasi Prometheus

**Tujuan:** Mengukur selisih CPU (%), memori (MB), dan latensi (ms) antara sistem _tanpa_ instrumentasi Prometheus (S1a) dan sistem _dengan_ instrumentasi Prometheus (S1b).

**Compose file yang digunakan:** `docker-compose-5-1.yml` (S1a, tanpa metrik) dan `docker-compose-5-2.yml` (S1b, dengan metrik)

**Output yang dihasilkan:**

- `tests/results/s1_overhead_no_metrics_stats.csv` (S1a)
- `tests/results/s1_overhead_with_metrics_stats.csv` (S1b)

### Cara Menjalankan S1 (Otomatis)

```powershell
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\tests"
.\run_s1_overhead.ps1
```

Script ini akan otomatis:

1. Menurunkan compose yang berjalan sebelumnya
2. Menjalankan `docker-compose-5-1.yml` (S1a tanpa metrik)
3. Menunggu 60 detik stabilisasi
4. Mengumpulkan metrik selama 120 detik ke CSV S1a
5. Menurunkan S1a, menjalankan `docker-compose-5-2.yml` (S1b dengan metrik)
6. Menunggu 60 detik stabilisasi
7. Mengumpulkan metrik selama 120 detik ke CSV S1b
8. Menurunkan S1b

### Cara Menjalankan S1 (Manual, jika script gagal)

**Langkah S1a — Sistem Tanpa Prometheus:**

```powershell
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS"
docker compose down -v
docker compose -f docker-compose-5-1.yml up -d --build
# Tunggu 60 detik
Start-Sleep -Seconds 60
# Kumpulkan metrik
python tests/collect_docker_stats.py --duration 120 --output tests/results/s1_overhead_no_metrics_stats.csv --target-substring ""
docker compose -f docker-compose-5-1.yml down -v
```

**Langkah S1b — Sistem Dengan Prometheus:**

```powershell
docker compose -f docker-compose-5-2.yml up -d --build
Start-Sleep -Seconds 60
python tests/collect_docker_stats.py --duration 120 --output tests/results/s1_overhead_with_metrics_stats.csv --target-substring ""
docker compose -f docker-compose-5-2.yml down -v
```

### Analisis Perbandingan S1a vs S1b

Setelah kedua CSV tersedia:

```powershell
python tests/analyze_s1.py --s1a tests/results/s1_overhead_no_metrics_stats.csv --s1b tests/results/s1_overhead_with_metrics_stats.csv --output tests/results/s1_comparison.csv
```

### Verifikasi Hasil

```powershell
Get-Content tests/results/s1_overhead_no_metrics_stats.csv | Select-Object -First 5
Get-Content tests/results/s1_overhead_with_metrics_stats.csv | Select-Object -First 5
```

CSV harus memiliki kolom `timestamp`, `aggregate_cpu_percent`, `aggregate_mem_mb` dan minimal 20 baris data.

---

## 7. S2 — Skalabilitas Multi-Container

**Tujuan:** Mengukur pengaruh jumlah _instance_ (1 hingga 5 container) terhadap _data delay end-to-end_, CPU agregat, dan memori agregat pada modul **Data Archiver** dan **P-Wave Detector**.

**Compose file yang digunakan:**

- Data Archiver (1–5 container): `docker-compose-3-1.yml` hingga `docker-compose-3-5.yml`
- P-Wave Detector Kafka native (2–5 container): `docker-compose-3-6.yml` hingga `docker-compose-3-9.yml`
- P-Wave Detector FastAPI (2–5 container): `docker-compose-3-10.yml` hingga `docker-compose-3-13.yml`

**Output yang dihasilkan (per variasi):**

- `tests/results/table4_1_container_stats.csv` hingga `table4_5_container_stats.csv`
- `tests/results/table5_kafka_2c_stats.csv` hingga `table5_fastapi_5c_stats.csv`

### Cara Menjalankan S2 — Data Archiver (Otomatis)

```powershell
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\tests"
.\run_table4_archiver.ps1
```

### Cara Menjalankan S2 — P-Wave Detector (Otomatis)

```powershell
.\run_table5_pwavedetector.ps1
```

### Cara Menjalankan S2 (Manual, satu konfigurasi)

Contoh untuk Data Archiver 3 container:

```powershell
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS"
docker compose down -v
docker compose -f docker-compose-3-3.yml up -d --build
Start-Sleep -Seconds 60

# Jalankan kedua kolektor secara bersamaan
Start-Process python -ArgumentList "tests/collect_docker_stats.py --duration 120 --output tests/results/table4_3_container_stats.csv --target-substring data_archiver" -NoNewWindow
python tests/collect_metrics.py --duration 120 --output tests/results/table4_3_container_metrics.csv

docker compose -f docker-compose-3-3.yml down -v
```

### Verifikasi Hasil

```powershell
Get-ChildItem tests/results/table4_*.csv
Get-ChildItem tests/results/table5_*.csv
```

---

## 8. S3 — Perbandingan WebSocket Server

**Tujuan:** Membandingkan performa Express.js/Socket.IO versus FastAPI dalam menangani koneksi WebSocket pada 1 client dan 5 client konkuren, mengukur _data delay_, CPU (%), dan memori (MB).

**Compose file yang digunakan:**

- Express.js: `docker-compose-4-1.yml` (port `3333`)
- FastAPI: `docker-compose-4-2.yml` (port `3334`)

**Output yang dihasilkan:**

- `tests/results/table6_express_1c_stats.csv`
- `tests/results/table6_express_5c_stats.csv`
- `tests/results/table6_fastapi_1c_stats.csv`
- `tests/results/table6_fastapi_5c_stats.csv`

### Cara Menjalankan S3 (Otomatis)

```powershell
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\tests"
.\run_table6_websocket.ps1
```

Script ini secara otomatis akan menjalankan `ws_load_generator.py` untuk mensimulasikan 1 atau 5 client WebSocket yang terkoneksi selama durasi pengujian.

### Cara Menjalankan S3 (Manual)

Contoh untuk Express.js dengan 5 client:

```powershell
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS"
docker compose down -v
docker compose -f docker-compose-4-1.yml up -d --build
Start-Sleep -Seconds 60

# Jalankan load generator di background
Start-Process python -ArgumentList "tests/ws_load_generator.py --uri ws://localhost:3333 --clients 5 --duration 60" -NoNewWindow

# Kumpulkan metrik selama durasi yang sama
Start-Process python -ArgumentList "tests/collect_docker_stats.py --duration 60 --output tests/results/table6_express_5c_stats.csv --target-substring api" -NoNewWindow
python tests/collect_metrics.py --duration 60 --output tests/results/table6_express_5c_metrics.csv

docker compose -f docker-compose-4-1.yml down -v
```

### Verifikasi Hasil

```powershell
Get-ChildItem tests/results/table6_*.csv
```

---

## 9. S4 — Kafka vs Kafka+NGINX Load Balancer

**Tujuan:** Membandingkan konfigurasi _message broker_ Kafka native (3 broker) versus Kafka+NGINX sebagai _load balancer_ eksternal, mengukur _data delay_, CPU (%), dan memori (MB) pada kondisi beban normal.

**Compose file yang digunakan:**

- Kafka 3 Container: `docker-compose-2-1.yml`
- Kafka 3 Container + NGINX: `docker-compose-2-2.yml`

**Output yang dihasilkan:**

- `tests/results/table2_kafka_stats.csv`
- `tests/results/table2_kafka_metrics.csv`
- `tests/results/table2_nginx_stats.csv`
- `tests/results/table2_nginx_metrics.csv`

### Cara Menjalankan S4 (Otomatis)

```powershell
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\tests"
.\run_table2_broker.ps1
```

### Cara Menjalankan S4 (Manual)

Contoh untuk Kafka saja:

```powershell
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS"
docker compose down -v
docker compose -f docker-compose-2-1.yml up -d --build
Start-Sleep -Seconds 60

Start-Process python -ArgumentList "tests/collect_docker_stats.py --duration 120 --output tests/results/table2_kafka_stats.csv --target-substring kafka" -NoNewWindow
python tests/collect_metrics.py --duration 120 --output tests/results/table2_kafka_metrics.csv

docker compose -f docker-compose-2-1.yml down -v
```

Contoh untuk Kafka + NGINX:

```powershell
docker compose -f docker-compose-2-2.yml up -d --build
Start-Sleep -Seconds 60

Start-Process python -ArgumentList "tests/collect_docker_stats.py --duration 120 --output tests/results/table2_nginx_stats.csv --target-substring kafka" -NoNewWindow
python tests/collect_metrics.py --duration 120 --output tests/results/table2_nginx_metrics.csv

docker compose -f docker-compose-2-2.yml down -v
```

### Verifikasi Hasil

```powershell
Get-ChildItem tests/results/table2_*.csv
```

---

## 10. Menjalankan Semua Skenario Sekaligus

Jika Anda ingin menjalankan S1 hingga S4 secara berurutan tanpa intervensi manual, gunakan master runner:

```powershell
cd "e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\tests"
.\run_all_tests.ps1
```

> **Perhatian:** Proses ini membutuhkan estimasi **1,5 hingga 3 jam** tergantung spesifikasi mesin. Pastikan komputer tidak masuk mode tidur (_sleep_) selama eksekusi.

Untuk mencegah komputer tidur saat tes berjalan panjang:

```powershell
# Jalankan ini di terminal terpisah selama pengujian berlangsung
while ($true) { [System.Console]::Write("."); Start-Sleep -Seconds 60 }
```

---

## 11. Checklist Output yang Harus Dikumpulkan

Tandai setiap item setelah berhasil dikumpulkan.

### Screenshot (satu kali, dari sistem yang sudah tervalidasi)

- [ ] `docker compose ps` — semua container Up
- [ ] `http://localhost:3333` — data trace muncul
- [ ] `http://localhost:3334` — koneksi WebSocket aktif
- [ ] `http://localhost:8107/metrics` — teks metrik Prometheus muncul
- [ ] `http://localhost:9090/targets` — semua target UP (hijau)
- [ ] Prometheus Graph — query `up`
- [ ] Prometheus Graph — query CPU
- [ ] Grafana dashboard — panel berisi grafik terisi data
- [ ] InfluxDB Data Explorer — bucket `eews` berisi data
- [ ] Mongo Express — koleksi berisi dokumen

### File CSV per Skenario

**S1 — Overhead Instrumentasi:**

- [ ] `tests/results/s1_overhead_no_metrics_stats.csv`
- [ ] `tests/results/s1_overhead_with_metrics_stats.csv`
- [ ] `tests/results/s1_comparison.csv` (hasil analisis)

**S2 — Data Archiver (1–5 container):**

- [ ] `tests/results/table4_1_container_stats.csv`
- [ ] `tests/results/table4_2_container_stats.csv`
- [ ] `tests/results/table4_3_container_stats.csv`
- [ ] `tests/results/table4_4_container_stats.csv`
- [ ] `tests/results/table4_5_container_stats.csv`

**S2 — P-Wave Detector Kafka (2–5 container):**

- [ ] `tests/results/table5_kafka_2c_stats.csv`
- [ ] `tests/results/table5_kafka_3c_stats.csv`
- [ ] `tests/results/table5_kafka_4c_stats.csv`
- [ ] `tests/results/table5_kafka_5c_stats.csv`

**S2 — P-Wave Detector FastAPI (2–5 container):**

- [ ] `tests/results/table5_fastapi_2c_stats.csv`
- [ ] `tests/results/table5_fastapi_3c_stats.csv`
- [ ] `tests/results/table5_fastapi_4c_stats.csv`
- [ ] `tests/results/table5_fastapi_5c_stats.csv`

**S3 — WebSocket:**

- [ ] `tests/results/table6_express_1c_stats.csv`
- [ ] `tests/results/table6_express_5c_stats.csv`
- [ ] `tests/results/table6_fastapi_1c_stats.csv`
- [ ] `tests/results/table6_fastapi_5c_stats.csv`

**S4 — Broker:**

- [ ] `tests/results/table2_kafka_stats.csv`
- [ ] `tests/results/table2_kafka_metrics.csv`
- [ ] `tests/results/table2_nginx_stats.csv`
- [ ] `tests/results/table2_nginx_metrics.csv`

### Verifikasi Cepat Semua CSV

```powershell
Get-ChildItem "tests/results/*.csv" | ForEach-Object {
    $lines = (Get-Content $_.FullName).Count
    Write-Host "$($_.Name): $lines baris"
}
```

Setiap CSV harus memiliki **lebih dari 5 baris** (header + data). Jika kurang, pengujian mungkin terlalu singkat atau container belum stabil saat pengumpulan dimulai.

---

## 12. Troubleshooting

### Pengecekan Log Error per Modul

Untuk mendeteksi error pada seluruh modul atau modul tertentu secara menyeluruh:

**Filter Semua Error Terkini Sekaligus (5 Menit Terakhir):**
- PowerShell (Windows):
  ```powershell
  docker compose logs --since 5m | Select-String "ERROR", "Exception", "Traceback"
  ```
- Bash (Ubuntu / Linux):
  ```bash
  docker compose logs --since 5m | grep -iE "ERROR|Exception|Traceback"
  ```

**Pengecekan Error Terkini per Modul Spesifik:**
Jika ingin lebih detail, Anda bisa menjalankan perintah berikut untuk mengecek sisa bug terbaru pada setiap modul:

```powershell
# Data Provider
docker compose logs data_provider --since 5m | Select-String "ERROR", "Exception", "Traceback"

# AI Detectors
docker compose logs p_wave_detector --since 5m | Select-String "ERROR", "Exception", "Traceback"
docker compose logs loc_mag_detector --since 5m | Select-String "ERROR", "Exception", "Traceback"

# Backend & APIs
docker compose logs data_archiver --since 5m | Select-String "ERROR", "Exception", "Traceback"
docker compose logs api_server --since 5m | Select-String "ERROR", "Exception", "Traceback"
docker compose logs fast_api --since 5m | Select-String "ERROR", "Exception", "Traceback"

# Infrastruktur Inti (Kafka, Zookeeper, dll)
docker compose logs kafka1 --since 5m | Select-String "ERROR", "Exception", "Traceback"
docker compose logs zookeeper --since 5m | Select-String "ERROR", "Exception", "Traceback"
```

*(Tips: Jika Anda menggunakan Mac/Linux, cukup ganti `Select-String "..."` dengan `grep -iE "ERROR|Exception|Traceback"`).*

### Penanganan Resource Berlebihan (CPU > 100% / Memory Full / Laptop Lambat)

Jika Docker Desktop menggunakan resource berlebihan (misalnya CPU 1000%+ atau RAM penuh) saat pengujian lokal:

1. **Turunkan Beban Data Provider di `.env`:**
   Secara default konfigurasi produksi menggunakan 30 proses dan 6000 stasiun. Untuk pengujian skala lokal/laptop, sesuaikan nilai berikut di file `.env`:
   ```env
   DATA_PROVIDER_NUM_PROCESSES=2
   DATA_PROVIDER_NUM_STATIONS=50
   ```
2. **Restrukturisasi/Rebuild Container:**
   ```powershell
   docker compose down -v
   docker compose up -d --build
   ```
3. **Batasi Resource pada Docker Desktop (Windows):**
   Masuk ke Settings > Resources di Docker Desktop, batasi penggunaan CPU (misal max 4 core) dan RAM (misal max 8 GB).

### Container langsung Exiting atau Restarting

```powershell
docker compose logs --tail=50 data_provider
docker compose logs --tail=50 p_wave_detector
docker compose logs --tail=50 kafka1
```

Cari pesan `Error`, `Exception`, atau `ECONNREFUSED`. Untuk Kafka, tunggu minimal 60 detik karena Kafka membutuhkan waktu startup yang relatif lama.

### Error `model_p_wave.h5` atau `model_loc_mag.h5` tidak ditemukan

File model H5 harus tersedia di dalam folder masing-masing modul sebelum build:

- `p_wave_detector/model_p_wave.h5`
- `loc_mag_detector/model_p_wave.h5`

### Python: `ModuleNotFoundError: No module named 'requests'`

```powershell
pip install requests websockets
```

### CSV kosong atau hanya berisi header

Pastikan:

1. Container sudah berjalan selama minimal 60 detik sebelum kolektor dijalankan
2. Argumen `--target-substring` sesuai nama container (cek `docker compose ps`)

---

## 13. Verifikasi Penyimpanan Data ke Database

Selain metrik pada Grafana, Anda juga perlu memastikan bahwa seluruh data tersimpan dengan baik di database yang digunakan oleh sistem (InfluxDB, MongoDB, dan Prometheus). 

Berikut adalah cara memverifikasi data di masing-masing database:

### A. Verifikasi InfluxDB (Penyimpanan Data Gelombang & Metrik)
InfluxDB v2 menggunakan konsep **bucket** dan bahasa query **Flux**. Anda dapat memverifikasi data yang tersimpan secara langsung via terminal PowerShell menggunakan CLI InfluxDB v2 dengan token dan nama organisasi.

1. **Cek daftar bucket yang tersedia:**
   ```powershell
   docker compose exec influxdb influx bucket list --token "eFWu0UGcCzvGAX1w-z43heHjfDk8swujfryImhIsTrAkNJOgfMRSYsgYVki-QTiWHDwKLJtxsSnCmHhxisCN1w==" --org "owner"
   ```

2. **Cek data gelombang seismik terbaru (bucket `eews`):**
   Jalankan query Flux untuk menampilkan 10 sampel data dalam rentang 1 jam terakhir:
   ```powershell
   docker compose exec influxdb influx query 'from(bucket: \"eews\") |> range(start: -1h) |> limit(n: 10)' --token "eFWu0UGcCzvGAX1w-z43heHjfDk8swujfryImhIsTrAkNJOgfMRSYsgYVki-QTiWHDwKLJtxsSnCmHhxisCN1w==" --org "owner"
   ```

3. **Cek data Real-Time (Data mutakhir yang baru saja masuk):**
   - **Melihat data 1 menit terakhir (10 sampel paling akhir):**
     ```powershell
     docker compose exec influxdb influx query 'from(bucket: \"eews\") |> range(start: -1m) |> tail(n: 10)' --token "eFWu0UGcCzvGAX1w-z43heHjfDk8swujfryImhIsTrAkNJOgfMRSYsgYVki-QTiWHDwKLJtxsSnCmHhxisCN1w==" --org "owner"
     ```
   - **Melihat titik sampel paling mutakhir (`last()`) untuk tiap sensor/stasiun:**
     ```powershell
     docker compose exec influxdb influx query 'from(bucket: \"eews\") |> range(start: -5m) |> last()' --token "eFWu0UGcCzvGAX1w-z43heHjfDk8swujfryImhIsTrAkNJOgfMRSYsgYVki-QTiWHDwKLJtxsSnCmHhxisCN1w==" --org "owner"
     ```
   - **Melihat 10 data terbaru diurutkan dari timestamp paling baru (descending):**
     ```powershell
     docker compose exec influxdb influx query 'from(bucket: \"eews\") |> range(start: -5m) |> sort(columns: [\"_time\"], desc: true) |> limit(n: 10)' --token "eFWu0UGcCzvGAX1w-z43heHjfDk8swujfryImhIsTrAkNJOgfMRSYsgYVki-QTiWHDwKLJtxsSnCmHhxisCN1w==" --org "owner"
     ```

   > **Catatan PowerShell:** Pastikan menggunakan tanda petik tunggal (`'...'`) di luar query dan meng-escape nama bucket/kolom dengan backslash (`\"eews\"`, `\"_time\"`) agar tidak terpotong oleh parser PowerShell.

### B. Verifikasi MongoDB (Penyimpanan Hasil Deteksi AI)
MongoDB digunakan oleh modul `data_archiver` untuk menyimpan data timeseries dan hasil analisis dari modul AI.

1. **Masuk ke dalam container MongoDB (menggunakan `mongosh`):**
   *(Catatan: Nama service container di docker-compose adalah `mongo`)*
   ```powershell
   docker compose exec mongo mongosh
   ```
2. **Cek database yang tersedia dan pilih database `timeseries_db`:**
   ```javascript
   test> show dbs
   test> use timeseries_db
   ```
3. **Cek koleksi data yang tersedia:**
   ```javascript
   timeseries_db> show collections
   ```
4. **Cek jumlah dokumen / data yang sudah tersimpan:**
   ```javascript
   timeseries_db> db.timeseries_collection.countDocuments()
   ```
5. **Tampilkan data mutakhir/terbaru yang masuk:**
   ```javascript
   timeseries_db> db.timeseries_collection.find().sort({_id: -1}).limit(1)
   ```
*(Ketik `exit` untuk keluar dari shell MongoDB).*

### C. Verifikasi Prometheus (Penyimpanan Metrik Observabilitas)
Prometheus menarik (scrape) metrik dari seluruh layanan, termasuk Data Provider, Node Exporter, cAdvisor, dan Kafka.

1. Buka browser dan akses **Prometheus Web UI**:
   - `http://localhost:9090`
2. Di kolom pencarian (Expression), ketikkan query berikut dan klik **Execute** (pilih tab **Table** atau **Graph**):
   - Cek metrik dari Data Provider: `data_provider_traces_sent_total`
   - Cek penggunaan CPU container Kafka: `rate(container_cpu_usage_seconds_total{container_label_com_docker_compose_service=~"kafka.*"}[1m])`
   - Cek metrik API Server HTTP reqs: `http_requests_total`
3. Jika query mengembalikan tabel nilai (bukan "Empty query result"), artinya Prometheus berhasil menyimpan metrik.
3. Tidak ada error di terminal saat kolektor berjalan

### Permission Denied saat menulis CSV

Pastikan file CSV tidak sedang dibuka di Excel atau editor lain. Tutup semua aplikasi yang membuka file tersebut.

### Rebuild paksa setelah perubahan kode

```powershell
docker builder prune -af
docker compose -f docker-compose-5-2.yml build --no-cache --progress=plain
```

### Hapus semua data volume (reset total)

```powershell
docker compose down -v
docker volume prune -f
```

> **Perhatian:** Perintah di atas menghapus seluruh data MongoDB, InfluxDB, dan Grafana. Gunakan hanya jika memang ingin reset penuh.

---

## Referensi Mapping Skenario ke Compose File

| Kode Skenario (BAB III)     | Compose File              | Script Otomatis                |
| --------------------------- | ------------------------- | ------------------------------ |
| S1a — Tanpa Prometheus      | `docker-compose-5-1.yml`  | `run_s1_overhead.ps1`          |
| S1b — Dengan Prometheus     | `docker-compose-5-2.yml`  | `run_s1_overhead.ps1`          |
| S2 — Archiver 1 Container   | `docker-compose-3-1.yml`  | `run_table4_archiver.ps1`      |
| S2 — Archiver 2 Container   | `docker-compose-3-2.yml`  | `run_table4_archiver.ps1`      |
| S2 — Archiver 3 Container   | `docker-compose-3-3.yml`  | `run_table4_archiver.ps1`      |
| S2 — Archiver 4 Container   | `docker-compose-3-4.yml`  | `run_table4_archiver.ps1`      |
| S2 — Archiver 5 Container   | `docker-compose-3-5.yml`  | `run_table4_archiver.ps1`      |
| S2 — P-Wave Kafka 2C        | `docker-compose-3-6.yml`  | `run_table5_pwavedetector.ps1` |
| S2 — P-Wave Kafka 3C        | `docker-compose-3-7.yml`  | `run_table5_pwavedetector.ps1` |
| S2 — P-Wave Kafka 4C        | `docker-compose-3-8.yml`  | `run_table5_pwavedetector.ps1` |
| S2 — P-Wave Kafka 5C        | `docker-compose-3-9.yml`  | `run_table5_pwavedetector.ps1` |
| S2 — P-Wave FastAPI 2C      | `docker-compose-3-10.yml` | `run_table5_pwavedetector.ps1` |
| S2 — P-Wave FastAPI 3C      | `docker-compose-3-11.yml` | `run_table5_pwavedetector.ps1` |
| S2 — P-Wave FastAPI 4C      | `docker-compose-3-12.yml` | `run_table5_pwavedetector.ps1` |
| S2 — P-Wave FastAPI 5C      | `docker-compose-3-13.yml` | `run_table5_pwavedetector.ps1` |
| S3 — Express 1 Client       | `docker-compose-4-1.yml`  | `run_table6_websocket.ps1`     |
| S3 — Express 5 Client       | `docker-compose-4-1.yml`  | `run_table6_websocket.ps1`     |
| S3 — FastAPI 1 Client       | `docker-compose-4-2.yml`  | `run_table6_websocket.ps1`     |
| S3 — FastAPI 5 Client       | `docker-compose-4-2.yml`  | `run_table6_websocket.ps1`     |
| S4 — Kafka 3 Broker         | `docker-compose-2-1.yml`  | `run_table2_broker.ps1`        |
| S4 — Kafka 3 Broker + NGINX | `docker-compose-2-2.yml`  | `run_table2_broker.ps1`        |

---

## 16. Panduan Eksekusi dan Pengambilan Data Manual (Per Compose)

Jika Anda ingin mengontrol jalannya pengujian secara manual per-*compose* (satu per satu), menghidupkannya, mengekstrak datanya sendiri dengan perintah Python, lalu mematikannya, berikut adalah langkah-langkah presisinya:

### Langkah 1: Hidupkan Skenario Spesifik
Contoh kita gunakan `docker-compose-1-1.yml`:
```powershell
docker compose -f docker-compose-1-1.yml down -v
docker compose -f docker-compose-1-1.yml up -d --build
```
*(Tunggu sekitar 60 detik setelah `up -d` agar sistem Kafka dan Prometheus benar-benar stabil sebelum mulai mengambil data).*

### Langkah 2: Ambil Datanya
Buka terminal baru, atau jalankan perintah Python ini. Terdapat dua skrip utama yang bisa Anda gunakan sesuai kebutuhan:

**A. Mengambil Data CPU & Memori (Docker Stats)**
Gunakan skrip `collect_docker_stats.py`. Anda harus menentukan target nama container yang ingin difokuskan (misalnya `data_provider`).
```powershell
python tests/collect_docker_stats.py --duration 120 --output tests/results/data_1-1_stats.csv --target-substring data_provider
```
*(Ini akan merekam penggunaan CPU & RAM container yang mengandung nama `data_provider` selama 120 detik).*

**B. Mengambil Data Latency & Throughput (Prometheus)**
Gunakan skrip `collect_metrics.py` untuk mengambil data dari metrik sistem (seperti latensi pemrosesan atau pesan per detik).
```powershell
python tests/collect_metrics.py --duration 120 --output tests/results/data_1-1_metrics.csv
```

### Langkah 3: Matikan Setelah Selesai
Setelah file CSV selesai digenerate dan Anda sudah puas dengan datanya, bersihkan sistem:
```powershell
docker compose -f docker-compose-1-1.yml down -v
```

**Tips Tambahan untuk Parameter `--target-substring`:**
Saat Anda menguji *compose* lain, cukup ubah targetnya. Contoh:
- Untuk `docker-compose-3-x.yml` (Archiver), gunakan: `--target-substring data_archiver`
- Untuk `docker-compose-2-x.yml` (Kafka Broker), gunakan: `--target-substring kafka`
- Untuk `docker-compose-4-x.yml` (Backend/WebSocket), gunakan: `--target-substring fast_api` atau `api_server`

Dengan cara ini, Anda punya kontrol penuh untuk bereksperimen, mengganti durasi (misal `--duration 300` untuk 5 menit), atau mengubah nama file output sesuai kemauan Anda.

---

## 17. Daftar Lengkap Perintah Eksekusi Manual Seluruh Skenario

Berikut adalah kumpulan perintah lengkap (*copy-paste*) untuk menghidupkan lingkungan dan merekam data metrik maupun performa untuk **setiap skenario**. Anda cukup mengubah angka `--duration 120` (dalam detik) jika ingin mengambil data lebih lama.

> **PENTING:** Selalu beri jeda waktu tunggu (sekitar 60 detik) setelah Anda menekan *Enter* pada perintah `docker compose up -d` sebelum Anda menjalankan perintah pengambilan data `python`. Hal ini agar sistem Kafka dan sistem lainnya menyala dan stabil sepenuhnya.

### A. Skenario Kinerja Data Provider (docker-compose-1-x)
Fokus perekaman *resource* CPU & RAM pada layanan `data_provider`.

**Skenario 1.1: Sequence**
```powershell
docker compose -f docker-compose-1-1.yml down -v
docker compose -f docker-compose-1-1.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_1-1.csv --target-substring data_provider
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_1-1.csv
```

**Skenario 1.2: Multi-thread**
```powershell
docker compose -f docker-compose-1-2.yml down -v
docker compose -f docker-compose-1-2.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_1-2.csv --target-substring data_provider
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_1-2.csv
```

**Skenario 1.3: Multi-process**
```powershell
docker compose -f docker-compose-1-3.yml down -v
docker compose -f docker-compose-1-3.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_1-3.csv --target-substring data_provider
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_1-3.csv
```

**Skenario 1.4: Multi-process & Multi-thread**
```powershell
docker compose -f docker-compose-1-4.yml down -v
docker compose -f docker-compose-1-4.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_1-4.csv --target-substring data_provider
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_1-4.csv
```

**Skenario 1.5: Generator (FastAPI)**
```powershell
docker compose -f docker-compose-1-5.yml down -v
docker compose -f docker-compose-1-5.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_1-5.csv --target-substring data_provider
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_1-5.csv
```

### B. Skenario Arsitektur Message Broker Kafka (docker-compose-2-x)
Fokus perekaman *resource* CPU & RAM pada layanan `kafka`.

**Skenario 2.1: Kafka 3 Broker (Tanpa NGINX)**
```powershell
docker compose -f docker-compose-2-1.yml down -v
docker compose -f docker-compose-2-1.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_2-1.csv --target-substring kafka
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_2-1.csv
```

**Skenario 2.2: Kafka 3 Broker (Dengan NGINX Load Balancer)**
```powershell
docker compose -f docker-compose-2-2.yml down -v
docker compose -f docker-compose-2-2.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_2-2.csv --target-substring kafka
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_2-2.csv
```

### C. Skenario Scalability Worker Node (docker-compose-3-x)
Fokus pada container `data_archiver` atau `p_wave_detector`.

**Data Archiver (1 hingga 5 Container)**
```powershell
# 1 Container
docker compose -f docker-compose-3-1.yml down -v
docker compose -f docker-compose-3-1.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-1.csv --target-substring data_archiver
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-1.csv

# 2 Container
docker compose -f docker-compose-3-2.yml down -v
docker compose -f docker-compose-3-2.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-2.csv --target-substring data_archiver
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-2.csv

# 3 Container
docker compose -f docker-compose-3-3.yml down -v
docker compose -f docker-compose-3-3.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-3.csv --target-substring data_archiver
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-3.csv

# 4 Container
docker compose -f docker-compose-3-4.yml down -v
docker compose -f docker-compose-3-4.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-4.csv --target-substring data_archiver
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-4.csv

# 5 Container
docker compose -f docker-compose-3-5.yml down -v
docker compose -f docker-compose-3-5.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-5.csv --target-substring data_archiver
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-5.csv
```

**P-Wave Detector (Direct Kafka - 2 hingga 5 Container)**
```powershell
# 2 Container
docker compose -f docker-compose-3-6.yml down -v
docker compose -f docker-compose-3-6.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-6.csv --target-substring p_wave_detector
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-6.csv

# 3 Container
docker compose -f docker-compose-3-7.yml down -v
docker compose -f docker-compose-3-7.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-7.csv --target-substring p_wave_detector
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-7.csv

# 4 Container
docker compose -f docker-compose-3-8.yml down -v
docker compose -f docker-compose-3-8.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-8.csv --target-substring p_wave_detector
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-8.csv

# 5 Container
docker compose -f docker-compose-3-9.yml down -v
docker compose -f docker-compose-3-9.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-9.csv --target-substring p_wave_detector
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-9.csv
```

**P-Wave Detector (FastAPI HTTP + NGINX - 2 hingga 5 Container)**
```powershell
# 2 Container
docker compose -f docker-compose-3-10.yml down -v
docker compose -f docker-compose-3-10.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-10.csv --target-substring p_wave_detector_load_balance
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-10.csv

# 3 Container
docker compose -f docker-compose-3-11.yml down -v
docker compose -f docker-compose-3-11.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-11.csv --target-substring p_wave_detector_load_balance
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-11.csv

# 4 Container
docker compose -f docker-compose-3-12.yml down -v
docker compose -f docker-compose-3-12.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-12.csv --target-substring p_wave_detector_load_balance
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-12.csv

# 5 Container
docker compose -f docker-compose-3-13.yml down -v
docker compose -f docker-compose-3-13.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_3-13.csv --target-substring p_wave_detector_load_balance
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_3-13.csv
```

### D. Skenario WebSocket dan Backend (docker-compose-4-x)
Fokus pada container `api_server` (Express) atau `fast_api` (FastAPI).

**Skenario 4.1: Express API (1 atau 5 Klien)**
```powershell
docker compose -f docker-compose-4-1.yml down -v
docker compose -f docker-compose-4-1.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_4-1.csv --target-substring api_server
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_4-1.csv
```

**Skenario 4.2: FastAPI (1 atau 5 Klien)**
```powershell
docker compose -f docker-compose-4-2.yml down -v
docker compose -f docker-compose-4-2.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_4-2.csv --target-substring fast_api
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_4-2.csv
```

### E. Skenario Perbandingan Instrumentasi (docker-compose-5-x)
Fokus membandingkan `data_provider` tanpa dan dengan *library* Prometheus.

**Skenario 5.1: Tanpa Instrumentasi Prometheus**
```powershell
docker compose -f docker-compose-5-1.yml down -v
docker compose -f docker-compose-5-1.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_5-1.csv --target-substring data_provider
# (Skrip metrik tidak dipanggil karena fitur observabilitas dimatikan secara khusus pada skenario ini)
```

**Skenario 5.2: Dengan Instrumentasi Prometheus**
```powershell
docker compose -f docker-compose-5-2.yml down -v
docker compose -f docker-compose-5-2.yml up -d --build
python tests/collect_docker_stats.py --duration 120 --output tests/results/stats_5-2.csv --target-substring data_provider
python tests/collect_metrics.py --duration 120 --output tests/results/metrics_5-2.csv
```
