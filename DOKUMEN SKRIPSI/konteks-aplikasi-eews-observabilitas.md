# Konteks Aplikasi — EEWS Microservices dengan Observabilitas Prometheus & Grafana

> **Status dokumen:** Living document / dokumen kerja internal untuk memudahkan penulisan skripsi.
> **Pemilik:** Mohamad Solkhan Nawawi (24060123120020) — Informatika, FSM Undip.
> **Catatan penting:** Versi pustaka/environment (Python, Kafka image, Docker, dsb.) **belum fix** dan sengaja tidak dicantumkan di dokumen ini. Modul Prometheus & Grafana **belum diimplementasikan** di codebase saat ini — dokumen ini menjadi acuan rancangan sebelum implementasi dilakukan.

---

## 0. Posisi Proyek Ini

Sistem yang dibahas dalam dokumen ini **dirancang dan dibangun dari awal** sebagai proyek tugas akhir/skripsi, bukan replikasi atau kelanjutan dari karya ilmiah pihak lain. Seluruh keputusan arsitektur — pemilihan Kafka sebagai message broker, WebSocket sebagai mekanisme komunikasi real-time, NGINX sebagai load balancer, hingga penambahan Prometheus dan Grafana sebagai lapisan observabilitas — merupakan hasil rancangan sendiri untuk menjawab rumusan masalah penelitian ini.

Kode yang sudah ada saat ini (lihat Bagian 7 dan 8) adalah **implementasi awal/prototipe milik sendiri** yang sudah dibangun bertahap, dan menjadi dasar pengembangan lebih lanjut menuju versi final yang akan diuji dan dilaporkan dalam skripsi. Dokumen ini tidak merujuk ke publikasi, proposal, atau repositori pihak eksternal mana pun sebagai dasar arsitektur — semua penjelasan di bawah diposisikan sebagai rancangan sendiri, murni untuk kebutuhan penulisan Bab I–III skripsi secara konsisten.

---

## 1. Ringkasan Proyek

Penelitian ini merancang dan mengimplementasikan sebuah **Earthquake Early Warning System (EEWS)** berbasis arsitektur **microservices**, dengan setiap tahapan pemrosesan (ingesti data, deteksi gelombang-P, estimasi lokasi & magnitudo, pengarsipan, diseminasi) dipisah menjadi layanan independen yang dikontainerisasi menggunakan Docker. Komunikasi antar-layanan menggunakan **Apache Kafka** sebagai message broker, sedangkan diseminasi data real-time ke klien/frontend menggunakan **WebSocket** (bukan gRPC/RPC biner), agar implementasi tetap ringan dan mudah dipelihara.

Kontribusi utama penelitian ini adalah menambahkan **lapisan observabilitas terstruktur** berbasis **Prometheus** dan **Grafana** ke seluruh pipeline, karena tanpa mekanisme ini performa sistem (latensi, penggunaan CPU/memori, data delay end-to-end) sulit dipantau secara real-time maupun dianalisis secara reproducible — evaluasi hanya bisa dilakukan secara manual dan sesaat (snapshot testing), bukan pemantauan berkelanjutan.

**Poin rancangan kunci:**

| Aspek | Keputusan Desain |
|---|---|
| Arsitektur sistem | Microservices, tiap layanan berjalan sebagai container Docker independen |
| Protokol komunikasi antar-layanan kritis (Load Balancer ↔ P-Wave Detector) | HTTP biasa (bukan gRPC) |
| Mekanisme diseminasi real-time ke klien | **WebSocket** (Socket.IO/Express.js dan/atau FastAPI native WebSocket) |
| Message broker | Apache Kafka (multi-broker) |
| Load balancing | NGINX (untuk endpoint HTTP P-Wave Detector dan/atau broker Kafka) |
| Observabilitas | **Prometheus** (metrik) + **Grafana** (dashboard/visualisasi) — kontribusi utama penelitian |

---

## 2. Rumusan Masalah & Tujuan

### 2.1 Rumusan Masalah (draf)

1. Bagaimana merancang arsitektur microservices untuk EEWS yang menggunakan Kafka sebagai message broker dan WebSocket sebagai mekanisme komunikasi real-time, sehingga setiap modul dapat diskalakan dan dipelihara secara independen?
2. Metrik apa saja (latensi, penggunaan CPU, penggunaan memori, throughput/data delay) yang perlu diinstrumentasi pada tiap modul (Data Provider, P-Wave Detector, Load Balancer, Location-Magnitude Detector, Data Archiver, WebSocket Server) agar performa sistem EEWS dapat diamati secara real-time dan reproducible?
3. Bagaimana sistem pemantauan berbasis Prometheus dan Grafana dapat dirancang dan diintegrasikan ke dalam pipeline EEWS berbasis Docker, sehingga menghasilkan dashboard yang informatif serta metrik performa yang terstruktur dan dapat direproduksi?
4. Seberapa besar overhead yang ditimbulkan oleh instrumentasi Prometheus terhadap performa sistem EEWS itu sendiri?

### 2.2 Tujuan (draf)

1. Merancang dan mengimplementasikan arsitektur microservices EEWS yang terdiri atas modul ingesti data, deteksi gelombang-P, estimasi lokasi & magnitudo, pengarsipan data, dan diseminasi real-time berbasis WebSocket.
2. Mengimplementasikan endpoint `/metrics` (Counter, Gauge, Histogram) menggunakan pustaka `prometheus_client` (dan padanannya untuk layanan Node.js) pada seluruh modul dalam pipeline EEWS.
3. Mengonfigurasi Prometheus Server untuk melakukan scraping metrik secara periodik dari seluruh modul, ditambah Node Exporter untuk metrik level host.
4. Merancang dashboard Grafana yang menampilkan metrik latensi, CPU, memori, dan data delay end-to-end secara real-time, sekaligus mengukur overhead instrumentasi terhadap sistem.

> Catatan: rumusan masalah/tujuan final tetap mengikuti arahan pembimbing; bagian ini adalah draf kerja yang bisa disesuaikan saat integrasi ke Bab I skripsi.

### 2.3 Ruang Lingkup (draf)

- Sistem dibangun menggunakan Python (untuk modul pemrosesan data & deteksi) dan Node.js (untuk salah satu varian WebSocket server), diorkestrasi menggunakan Docker dan Docker Compose pada lingkungan pengembangan lokal.
- Komunikasi antar-layanan kritis menggunakan HTTP biasa; diseminasi ke klien menggunakan WebSocket. **Tidak ada penggunaan gRPC/Protocol Buffers** di sistem ini.
- Evaluasi performa difokuskan pada metrik: latensi komunikasi antar-layanan (ms), penggunaan CPU (%), penggunaan memori (MB), dan data delay end-to-end (s), seluruhnya diambil melalui Prometheus/Grafana.
- Model deep learning untuk deteksi gelombang-P dan estimasi lokasi-magnitudo menggunakan model yang sudah tersedia (bukan fokus pengembangan model baru); fokus penelitian ada pada arsitektur sistem dan lapisan observabilitasnya.
- Penelitian ini tidak mencakup deployment ke infrastruktur cloud skala produksi maupun pengujian pada jaringan sensor seismik fisik sesungguhnya.

---

## 3. Arsitektur Sistem (Rancangan)

### 3.1 Modul-Modul Sistem

| Modul | Teknologi | Peran | Komunikasi |
|---|---|---|---|
| Data Provider (+ varian strategi eksekusi: sequential/multithread/multiprocess/hybrid, dan generator data sintetis untuk uji beban) | Python, ObsPy, SeedLink, kafka-python | Ingesti data seismik mentah dari sumber SeedLink, publish ke Kafka | Kafka producer |
| P-Wave Detector (mode consumer langsung) | Python, TensorFlow, kafka-python | Deteksi onset gelombang-P dari trace mentah | Kafka consumer → producer |
| P-Wave Detector (mode load-balanced) | Python, FastAPI, TensorFlow | Versi P-Wave Detector yang diekspos sebagai endpoint HTTP (`POST /trace`) agar dapat di-*load balance* multi-instance | HTTP endpoint (dipanggil Load Balancer) → Kafka producer |
| Load Balancer | Python, kafka-python, requests | Consume topik trace/deteksi dari Kafka, meneruskan payload via HTTP ke instance P-Wave Detector | Kafka consumer → HTTP client |
| Location & Magnitude Detector | Python, TensorFlow, kafka-python | Estimasi hiposenter & magnitudo dari hasil deteksi gelombang-P | Kafka consumer → producer |
| Data Archiver | Python, kafka-python, MongoDB, InfluxDB, ObsPy | Mengarsipkan data trace mentah untuk keperluan penyimpanan jangka panjang | Kafka consumer |
| WebSocket Server (varian Express.js/Socket.IO) | Node.js, Express, Socket.IO, kafkajs | Meneruskan data waveform & hasil estimasi ke klien secara real-time | Kafka consumer → WebSocket |
| WebSocket Server (varian FastAPI) | Python, FastAPI, kafka-python | Alternatif WebSocket server (native WebSocket) untuk perbandingan performa | Kafka consumer → WebSocket |
| Dashboard klien (desktop) | Python, PyQt, klien WebSocket | Visualisasi waveform real-time untuk keperluan monitoring/demo | Klien WebSocket |
| NGINX | NGINX | Reverse proxy/load balancer untuk endpoint HTTP P-Wave Detector dan/atau broker Kafka | HTTP/WS proxy |
| Kafka Cluster | Kafka multi-broker + Zookeeper | Message broker terdistribusi untuk seluruh pipeline | — |
| MongoDB, InfluxDB | — | Penyimpanan data arsip & time-series | — |

**Topik Kafka yang dirancang:**

- `trace_topic` — data trace seismik mentah dari Data Provider.
- `p_wave_topic` — data trace channel-Z yang dikonsumsi jalur deteksi gelombang-P.
- `loc_mag_topic` — metadata hasil deteksi gelombang-P (input bagi Location & Magnitude Detector).
- `result_topic` / `result_loc_mag_topic` — hasil estimasi lokasi & magnitudo, dikonsumsi WebSocket Server untuk diseminasi ke klien.

### 3.2 Prinsip Desain yang Dipegang

- **Tanpa gRPC/RPC biner** — seluruh komunikasi antar-layanan kritis memakai HTTP biasa, dan diseminasi ke klien memakai WebSocket standar. Ini dipilih agar kompleksitas implementasi (definisi `.proto`, code generation stub, dsb.) tidak perlu ditanggung, sementara performa tetap memadai untuk skala sistem saat ini.
- **Observabilitas sebagai warga kelas satu (first-class citizen)** — setiap modul dirancang agar dapat diinstrumentasi metriknya sejak awal (endpoint `/metrics`), bukan ditambahkan belakangan sebagai tempelan.
- **Modularitas & skalabilitas horizontal** — tiap modul dapat diskalakan (multi-instance) secara independen, terutama P-Wave Detector dan Data Archiver, dengan bantuan load balancer.

### 3.3 Komponen yang Sudah Diimplementasikan vs. yang Masih Dirancang

| Komponen | Status |
|---|---|
| Pipeline inti (Data Provider → Kafka → P-Wave Detector → Loc-Mag Detector → Data Archiver → WebSocket Server) | ✅ Sudah diimplementasikan sebagai prototipe |
| Kafka multi-broker + opsi NGINX load balancer | ✅ Sudah diimplementasikan (beberapa konfigurasi pengujian tersedia) |
| Varian strategi paralelisasi Data Provider | ✅ Sudah diimplementasikan dan diuji secara awal |
| WebSocket Server ganda (Express.js/Socket.IO dan FastAPI native) | ✅ Sudah diimplementasikan |
| Grafana | ⚠️ Sudah berjalan, namun saat ini datasource-nya masih InfluxDB (untuk data arsip seismik) — **belum** menampilkan metrik observabilitas sistem |
| Prometheus Server | ❌ Belum ada, perlu ditambahkan |
| Node Exporter | ❌ Belum ada, perlu ditambahkan |
| Instrumentasi `prometheus_client` di seluruh modul Python | ❌ Belum ada, endpoint `/metrics` belum diimplementasikan di modul mana pun |
| Instrumentasi metrik di WebSocket Server berbasis Node.js | ❌ Belum ada |
| Dashboard Grafana khusus metrik Prometheus (CPU/memori/latensi sistem) | ❌ Belum dirancang, perlu dipisahkan dari dashboard InfluxDB yang sudah ada |
| Konfigurasi Docker Compose untuk skenario pengujian observabilitas | ❌ Belum dibuat, perlu diturunkan dari konfigurasi skenario yang sudah ada |

---

## 4. Rencana Instrumentasi Metrik per Modul

Rancangan awal jenis metrik (mengikuti pola `Counter`/`Gauge`/`Histogram` dari `prometheus_client`):

| Modul | Counter | Gauge | Histogram |
|---|---|---|---|
| Data Provider | total trace terkirim, total error publish Kafka | jumlah stream aktif per stasiun | — |
| P-Wave Detector | total request diterima, total deteksi gelombang-P positif, total error inferensi | ukuran antrean/cache waveform | latensi inferensi model (ms), latensi end-to-end sejak data diterima |
| Load Balancer | total pesan diteruskan, total gagal forward | — | latensi forward ke detector |
| Location & Magnitude Detector | total estimasi dihasilkan, total error | — | latensi inferensi model lokasi-magnitudo |
| Data Archiver | total record disimpan, total gagal simpan | — | latensi penulisan ke storage |
| WebSocket Server | total pesan di-broadcast, total klien connect/disconnect | jumlah klien WebSocket aktif | latensi broadcast per pesan |
| Node Exporter (level host) | — | CPU %, memori, disk, jaringan (bawaan) | — |

**Interval scraping** direncanakan pada kisaran beberapa detik (nilai final ditentukan saat implementasi/pengujian, tidak dikunci di dokumen ini).

---

## 5. Skenario Pengujian (Rancangan)

| Kode | Skenario | Deskripsi | Variabel Diukur |
|---|---|---|---|
| S1 | Overhead Instrumentasi Prometheus | Bandingkan performa sistem dengan dan tanpa `prometheus_client` aktif di seluruh modul | Selisih CPU (%), selisih memori (MB), selisih latensi (ms) |
| S2 | Skalabilitas Multi-Container | Variasi jumlah instance P-Wave Detector dan/atau Data Archiver, metrik diambil dari Prometheus | Data delay end-to-end (s), throughput (request/s), CPU/memori agregat |
| S3 | Perbandingan WebSocket Server (Express.js vs FastAPI) | Bandingkan dua implementasi WebSocket Server pada beban klien bertingkat, diukur via Prometheus/Grafana | Data delay (s), CPU (%), memori (MB), jumlah klien aktif |
| S4 | Observabilitas Kafka + NGINX Load Balancer | Bandingkan Kafka sebagai broker & load balancer vs. Kafka + NGINX sebagai load balancer terpisah | Data delay (s), CPU (%), memori (MB) |

Prinsip metodologis yang dipegang: pengujian dijalankan dengan jumlah trial yang memadai per skenario untuk stabilitas statistik, sistem di-restart antar-skenario untuk menjaga kondisi awal konsisten, dan analisis menggunakan statistik deskriptif (mean, median, P95) serta visualisasi time-series melalui Grafana.

---

## 6. Struktur Direktori Proyek (Referensi Implementasi Saat Ini)

```
project-root/
├── data_provider/                      # + varian: -sequence, -multithread, -multiprocess, -multiprocess-multithread, _generator
├── p_wave_detector/                    # mode Kafka consumer langsung
├── p_wave_detector_load_balance/       # mode HTTP endpoint (/trace) untuk load balancing
├── load_balancer/                      # Kafka consumer -> HTTP forwarder
├── loc_mag_detector/                   # estimasi hiposenter & magnitudo
├── data_archiver/                      # arsip ke MongoDB/InfluxDB/MiniSEED
├── api_server/                         # WebSocket server (Express.js + Socket.IO)
├── fast_api/                           # WebSocket server (FastAPI native WS)
├── seismic_app/                        # dashboard desktop PyQt (klien WebSocket)
├── nginx/nginx.conf                    # reverse proxy / load balancer
├── influxDB/.env                       # konfigurasi InfluxDB
├── docker-compose.yml                  # orkestrasi utama (default)
├── docker-compose-1-x.yml              # skenario strategi paralelisasi Data Provider
├── docker-compose-2-x.yml              # skenario Kafka vs Kafka+NGINX load balancer
├── docker-compose-3-x.yml              # skenario jumlah container Archiver/P-Wave Detector
├── docker-compose-4-x.yml              # skenario Express.js vs FastAPI WebSocket
├── cli_debug_tools/                      # utilitas debug/consume Kafka
├── data_provider_generator/            # generator data sintetis untuk uji beban
├── *.ps1                               # skrip pengumpulan metrik manual (sementara, sebelum ada Prometheus)
└── README.md / README_ID.md
```

**Rencana penambahan (belum ada secara fisik di repo):**

```
project-root/
├── prometheus/
│   └── prometheus.yml                  # konfigurasi scrape target
├── grafana/
│   └── provisioning/dashboards/...     # dashboard observabilitas (JSON), terpisah dari dashboard InfluxDB yang sudah ada
└── docker-compose-5-x.yml              # (usulan) skenario khusus overhead instrumentasi Prometheus (S1)
```

---

## 7. Catatan Penulisan untuk Skripsi

1. **Jangan mencantumkan versi pustaka/environment spesifik** (Python, Kafka, Docker, dsb.) di bagian mana pun draf skripsi sampai dikonfirmasi final — cukup sebut nama teknologi tanpa nomor versi, atau tandai sebagai `[versi menyusul]`.
2. Seluruh narasi Bab I–III ditulis sebagai **rancangan dan implementasi sendiri dari awal** — tidak perlu menyebut atau mengutip proyek/paper eksternal mana pun sebagai dasar arsitektur.
3. Landasan Teori terkait WebSocket sebaiknya membahas karakteristik komunikasi full-duplex, perbandingan singkat dengan HTTP polling/REST biasa, dan alasan pemilihannya (ringan, cukup untuk kebutuhan skala sistem saat ini) — tanpa perlu membandingkan dengan gRPC sebagai opsi yang dipertimbangkan lalu ditinggalkan, karena gRPC memang tidak pernah menjadi bagian dari rancangan sistem ini.
4. Gambar arsitektur sistem sebaiknya menekankan **titik-titik instrumentasi Prometheus (`/metrics`)** di setiap modul sebagai elemen visual utama, karena ini adalah kontribusi observabilitas yang menjadi fokus penelitian.
5. Bagian State of the Art dapat berisi kajian pustaka tentang microservices, Kafka, WebSocket, dan observabilitas (Prometheus/Grafana) secara umum, disusun sebagai pembanding dari sudut pandang eksternal — bukan sebagai narasi "melanjutkan sistem yang sudah ada".

---

## 8. Ringkasan Satu Paragraf (untuk Abstrak/Latar Belakang)

Penelitian ini merancang dan mengimplementasikan *Earthquake Early Warning System* (EEWS) berbasis arsitektur microservices yang menggunakan Apache Kafka sebagai message broker dan **WebSocket** sebagai mekanisme komunikasi real-time antar-layanan maupun ke klien, tanpa menggunakan protokol RPC biner seperti gRPC. Kontribusi utama penelitian adalah perancangan dan implementasi lapisan observabilitas berbasis **Prometheus** dan **Grafana**, mencakup instrumentasi metrik terstruktur (Counter, Gauge, Histogram) pada seluruh modul pipeline — Data Provider, P-Wave Detector, Load Balancer, Location & Magnitude Detector, Data Archiver, dan WebSocket Server — serta perancangan dashboard Grafana untuk memantau latensi, penggunaan CPU/memori, dan data delay end-to-end secara real-time dan reproducible, sekaligus mengukur overhead yang ditimbulkan oleh instrumentasi tersebut terhadap performa sistem secara keseluruhan.
