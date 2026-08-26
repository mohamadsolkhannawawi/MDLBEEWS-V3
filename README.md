# MDLBEEWS: Modular Deep Learning Based Earthquake Early Warning System

## Deskripsi Sistem

MDLBEEWS (*Modular Deep Learning Based Earthquake Early Warning System*) adalah sebuah sistem peringatan dini gempa bumi berbasis *deep learning* yang dirancang dengan arsitektur *microservices* modern. Sistem ini bertujuan untuk memproses data seismik secara *real-time* dan memprediksi potensi gempa dengan latensi seminimal mungkin, guna mendukung respons cepat mitigasi bencana. 

Fokus utama dari repositori ini adalah pada **pengembangan arsitektur backend yang scalable dan observable**. Sistem ini mengimplementasikan konsep *Event-Driven Architecture* (EDA) untuk memastikan aliran data berkecepatan tinggi antar layanan tidak terhambat (*bottleneck*).

## Arsitektur & Teknologi Utama

Pengembangan aplikasi ini bertumpu pada teknologi-teknologi standar industri untuk *streaming* dan *monitoring*:

- **Containerization (Docker & Docker Compose):** Seluruh modul diisolasi ke dalam container masing-masing untuk memudahkan deployment dan skalabilitas horizontal.
- **Message Broker (Apache Kafka):** Berfungsi sebagai tulang punggung (backbone) sistem untuk mendistribusikan data *waveform* seismik antar layanan (*decoupled services*) secara *real-time* dengan toleransi kesalahan (*fault-tolerant*).
- **WebSockets (FastAPI & Express.js):** Menangani pengiriman peringatan dan *update* data ke *client/frontend* secara dua arah (bidirectional) dengan latensi rendah.
- **Observability Stack (Prometheus & Grafana):** Sistem pemantauan komprehensif terintegrasi untuk melacak metrik krusial seperti penggunaan CPU, memori, latensi komunikasi antar-layanan (*inter-service latency*), dan *end-to-end data delay*.
- **Machine Learning (TensorFlow):** Model *deep learning* ditempatkan pada modul khusus untuk memproses inferensi P-Wave secara efisien tanpa membebani layanan pengumpul data.

## Struktur Microservices

Sistem ini terbagi ke dalam beberapa *service* terpisah yang memiliki tanggung jawab tunggal (*Single Responsibility Principle*):

1. **Data Provider:** Mengambil data seismik mentah (contoh: via SeedLink) dan mempublikasikannya ke topik Kafka.
2. **P-Wave Detector:** Mengkonsumsi data dari Kafka, melakukan *preprocessing*, menjalankan inferensi *deep learning*, dan mempublikasikan peringatan dini jika anomali terdeteksi.
3. **Loc-Mag Detector:** Memperkirakan lokasi episentrum dan magnitudo gempa lanjutan berdasarkan data peringatan.
4. **Data Archiver:** Menyimpan *log* metadata ke dalam MongoDB dan arsip data seismik (MiniSEED) ke sistem penyimpanan lokal.
5. **WebSocket Servers:** Bertugas sebagai *Gateway* antara sistem Kafka internal dengan klien eksternal.

## Panduan Instalasi & Pengembangan

### Prasyarat
- Docker dan Docker Compose.
- Environment yang memadai (RAM minimal 8GB direkomendasikan untuk menjalankan seluruh *stack* ML dan Observability).

### Instalasi
1. Clone repositori pengembangan ini:
   ```bash
   git clone https://github.com/developer/MDLBEEWS.git
   cd MDLBEEWS
   ```
2. Salin *environment variables* (opsional jika ingin kustomisasi):
   ```bash
   cp .env.example .env
   ```
3. Bangun dan jalankan seluruh container:
   ```bash
   docker compose up -d --build
   ```

## Akses Layanan & Monitoring

Setelah sistem berjalan, Anda dapat memonitor kinerjanya melalui:
- **Grafana Dashboard:** `http://localhost:4000` (Login: `admin` / `12345678`)
- **Prometheus UI:** `http://localhost:9090`
- **Node Exporter:** `http://localhost:9100`

Untuk menghentikan *environment* pengembangan:
```bash
docker compose down -v
```

## Pengujian Observabilitas

Sebagai bagian dari pengembangan sistem, terdapat skrip otomatis untuk menguji beban kerja aplikasi (overhead observabilitas, *load balancing*, dan perbandingan latensi):

```powershell
# Menjalankan seluruh tes performa secara berurutan
./tests/run_all_tests.ps1 -Scenario all
```

## Lisensi
Proyek ini dilisensikan di bawah lisensi MIT.
