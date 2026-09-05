# Rekapitulasi Hasil Pengujian Observabilitas EEWS (S1 – S5)

Dokumen ini berisi rangkuman seluruh tabel hasil pengujian dari skenario **S1 hingga S5** yang telah diolah dari file-file CSV di direktori `tests/results/`. Hasil pengujian ini siap digunakan untuk penyusunan **BAB IV (Hasil dan Pembahasan)**.

---

## 1. Skenario S1 — Evaluasi Strategi Konkurensi Data Provider

* **Tujuan:** Mengevaluasi efisiensi dan performa strategi konkurensi (`Sequential`, `Multithread`, `Multiprocess`, `MP_MT`) pada tahap ingesti data di hulu.
* **Sumber Data:** `summary_s1_concurrency.csv`

| Arsitektur | Throughput (Trace/s) | CPU Mean (%) | CPU Max (%) | RAM Mean (MB) |
|---|---|---|---|---|
| **SEQUENTIAL** | N/A* | 1,24 | 12,99 | 39,92 |
| **MULTITHREAD** | 138,27 | 57,19 | 88,76 | 75,71 |
| **MULTIPROCESS** | 138,23 | 52,74 | 92,84 | 328,56 |
| **MP_MT** | 117,77 | 34,12 | 52,42 | 211,56 |

> **Catatan:** Pada strategi *SEQUENTIAL*, throughput menghasilkan `N/A` akibat *head-of-line blocking* (tersendat) ketika memproses 6.000 stasiun secara sekuensial dalam 1 thread tunggal.

---

## 2. Skenario S2 — Overhead Instrumentasi Prometheus

* **Tujuan:** Mengukur besarnya beban (*overhead*) sumber daya (CPU dan RAM) yang ditimbulkan oleh aktifnya lapisan observabilitas Prometheus di seluruh modul.
* **Sumber Data:** `summary_s2_overhead.csv`

| Kondisi | CPU Mean (%) | CPU P95 (%) | RAM Mean (MB) | RAM Max (MB) |
|---|---|---|---|---|
| **Tanpa Metrics** | 859,92 | 1.286,62 | 12.071,53 | 21.250,48 |
| **Dengan Metrics** | 895,54 | 1.387,89 | 14.176,89 | 24.788,21 |

---

## 3. Skenario S3 — Skalabilitas Multi-Container Worker Node

### 3.1 Sub-Skenario S3a: Skalabilitas Data Archiver
* **Tujuan:** Mengukur konsumsi sumber daya pada penambahan jumlah replika *container* Data Archiver (1 hingga 5 *instance*).
* **Sumber Data:** `summary_s3a_archiver.csv`

| Replika | CPU Mean (%) | CPU Max (%) | RAM Mean (MB) |
|---|---|---|---|
| **1 Container** | 77,18 | 118,97 | 150,81 |
| **2 Container** | 130,81 | 199,92 | 247,51 |
| **3 Container** | 159,65 | 227,01 | 318,78 |
| **4 Container** | 168,38 | 259,74 | 384,60 |
| **5 Container** | 169,87 | 238,20 | 453,30 |

### 3.2 Sub-Skenario S3b: Skalabilitas P-Wave Detector
* **Tujuan:** Membandingkan skalabilitas latensi *end-to-end* deteksi gelombang-P dan penggunaan *resource* antara mode **Native Kafka** (pemrosesan *consumer* langsung) vs **Kafka+NGINX** (pemrosesan HTTP *load balanced*).
* **Sumber Data:** `summary_s3b_pwave.csv`

| Arsitektur | Replika | E2E P-Wave P95 (ms) | CPU Mean (%) | RAM Mean (MB) |
|---|---|---|---|---|
| **Native Kafka** | 2c | 113.030,80 | 365,21 | 8.573,09 |
| **Native Kafka** | 3c | 57.833,30 | 447,94 | 10.903,74 |
| **Native Kafka** | 4c | 57.031,20 | 521,33 | 10.888,37 |
| **Native Kafka** | 5c | 56.407,00 | 517,86 | 10.440,32 |
| **Kafka+NGINX** | 2c | 10.000,00 | 330,19 | 3.561,79 |
| **Kafka+NGINX** | 3c | 10.000,00 | 458,37 | 4.867,12 |
| **Kafka+NGINX** | 4c | 10.000,00 | 548,61 | 5.921,04 |
| **Kafka+NGINX** | 5c | 8.854,40 | 557,00 | 6.906,47 |

---

## 4. Skenario S4 — Perbandingan WebSocket Server

* **Tujuan:** Membandingkan performa latensi *broadcast* dan penggunaan *resource* antara **FastAPI Native WebSocket** dan **Express.js / Socket.IO** pada beban 1 klien dan 5 klien aktif.
* **Sumber Data:** `summary_s4_websocket.csv`

| Server | Klien Aktif | Broadcast P95 (ms) | CPU Mean (%) | RAM Mean (MB) |
|---|---|---|---|---|
| **FastAPI** | 1 Klien | 1,00 | 29,52 | 42,04 |
| **FastAPI** | 5 Klien | 1,00 | 46,57 | 39,35 |
| **Express.js** | 1 Klien | 1,00 | 19,62 | 48,98 |
| **Express.js** | 5 Klien | 1,00 | 23,03 | 49,42 |

---

## 5. Skenario S5 — Observabilitas Load Balancer Message Broker (Profil Bursty)

* **Tujuan:** Mengevaluasi ketahanan dan latensi pemrosesan P-Wave pada konfigurasi **Kafka Native** (3 broker) dibandingkan **Kafka + NGINX Load Balancer** saat menghadapi lonjakan beban mendadak (*bursty load*).
* **Sumber Data:** `summary_s5_broker.csv`

| Broker | E2E P-Wave Mean (ms) | E2E P-Wave P95 (ms) | CPU Mean (%) | RAM Mean (MB) |
|---|---|---|---|---|
| **Kafka Native** | 11.145,20 | 28.484,80 | 77,40 | 1.585,12 |
| **Kafka + NGINX** | 6.847,31 | 10.000,00 | 63,44 | 1.442,54 |

---

## 📍 Kesimpulan Ringkas

1. **Strategi Konkurensi Ingesti (S1):** `Multithread` dan `Multiprocess` terbukti paling efisien (mencapai ~138 trace/detik), sementara `Sequential` gagal mengatasi skala 6.000 stasiun.
2. **Overhead Observabilitas (S2):** Instrumentasi Prometheus hanya menambah *overhead* CPU ~4,1% dan RAM ~17,4%, aman untuk lingkungan produksi *cloud-native*.
3. **Skalabilitas & Load Balancing (S3 & S5):** Penggunaan **NGINX Load Balancer** menurunkan latensi *end-to-end* P-Wave secara drastis dibanding *consumer* Kafka murni (dari >56 detik menjadi <10 detik pada S3b, dan dari 28,4s menjadi 10s pada S5).
4. **WebSocket Diseminasi (S4):** Baik `Express.js` maupun `FastAPI` mampu menjaga latensi *broadcast* tetap ultra-rendah (1 ms), dengan Express.js konsumsi CPU sedikit lebih hemat.
