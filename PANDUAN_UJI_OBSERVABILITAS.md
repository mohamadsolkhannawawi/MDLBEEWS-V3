# Panduan Validasi dan Pengujian Sistem EEWS Observabilitas

Dokumen ini disusun sebagai panduan langkah demi langkah (checklist) bagi peneliti untuk memvalidasi apakah keseluruhan infrastruktur aplikasi (Microservices + Prometheus + Grafana) telah berjalan dengan baik, serta memandu cara pelaksanaan skenario pengujian yang dirancang pada **Bab III Skripsi**.

---

## 1. Persiapan dan Prasyarat (Pre-flight Check)

Sebelum memulai pengujian, pastikan *environment* lokal Anda sudah memenuhi syarat berikut:
- [ ] **Docker & Docker Compose** terinstal dan berjalan (*Docker Desktop* jika di Windows).
- [ ] **Python 3.10+** terinstal di OS lokal (host) untuk menjalankan script pengumpulan metrik.
- [ ] **PowerShell** tersedia (bawaan Windows) untuk mengeksekusi skrip otomatisasi.
- [ ] Install library Python yang dibutuhkan di host lokal (untuk script pengumpul data):
  ```bash
  pip install requests
  ```

---

## 2. Tahap 1: Validasi *Build* dan *Startup* Sistem Dasar

Tahap ini bertujuan untuk memastikan kode yang telah diperbarui tidak mengalami *crash* dan berhasil di-*build* menjadi container Docker.

**Langkah-langkah:**
1. Buka PowerShell atau Terminal di direktori *root* proyek (`MDLBEEWS`).
2. Bersihkan *environment* dari sisa percobaan sebelumnya (Opsional tapi disarankan):
   ```bash
   docker compose down -v
   ```
3. Jalankan sistem menggunakan konfigurasi *default* (setara dengan Skenario S2 / Skalabilitas Default):
   ```bash
   docker compose up -d --build
   ```
4. Tunggu beberapa menit (proses *build* awal membutuhkan waktu karena mengunduh *image* Python, Node.js, dan Kafka).
5. Validasi status container:
   ```bash
   docker compose ps
   ```
   *Ekspektasi: Seluruh container (kafka1-3, zookeeper, data_provider, p_wave_detector, loc_mag_detector, data_archiver, api_server, fast_api, prometheus, grafana, influxdb, dll) harus dalam status **Up (healthy)***.

---

## 3. Tahap 2: Validasi Lapisan Observabilitas

Tahap ini memvalidasi kontribusi utama penelitian, yaitu apakah metrik berhasil ditangkap oleh Prometheus dan divisualisasikan oleh Grafana.

**Langkah-langkah:**
1. **Validasi Endpoint Metrik Microservices:**
   Buka browser dan akses salah satu endpoint berikut:
   - `http://localhost:8101` (Metrik Data Provider)
   - `http://localhost:8107/metrics` (Metrik Express.js API)
   *Ekspektasi: Menampilkan teks mentah berformat Prometheus.*
2. **Validasi Prometheus Server:**
   Buka `http://localhost:9090/targets` di browser.
   *Ekspektasi: Seluruh endpoint (`data_provider`, `p_wave_detector`, dll) berstatus **UP** berwarna hijau.*
3. **Validasi Grafana Dashboard:**
   - Akses `http://localhost:4000` (Login: `admin` / `12345678`).
   - Masuk ke menu **Dashboards**. Anda akan melihat folder "EEWS" dengan dashboard bernama **"EEWS Observability Dashboard"**.
   - Buka dashboard tersebut.
   *Ekspektasi: Grafik mulai menampilkan data pergerakan CPU, Memori, Latency, Data Delay, dan jumlah Request (butuh waktu ~1 menit agar data terbentuk).*

---

## 4. Tahap 3: Pelaksanaan Eksekusi Skenario (Bab III)

Setelah sistem dasar dipastikan berjalan, Anda dapat mulai mengeksekusi skenario-skenario pengujian yang diwajibkan di Bab III. Kami telah menyediakan skrip otomatisasinya.

**Langkah-langkah:**
1. Buka PowerShell.
2. Navigasi ke *root* proyek.
3. Jalankan skrip tes berikut ini. Skrip ini akan menghapus container lama, menjalankan *build* baru khusus skenario tersebut, menunggu sistem stabil 60 detik, dan mengumpulkan metrik ke CSV selama 120 detik.

   **Menjalankan Seluruh Skenario (S1-S4) Secara Sekaligus (Ditinggal semalaman):**
   ```powershell
   ./tests/run_all_tests.ps1 -Scenario all
   ```

   **Menjalankan Skenario Tertentu Saja (Untuk Debug/Pengecekan):**
   ```powershell
   # Skenario S1a: Overhead (Tanpa Metrik)
   ./tests/run_all_tests.ps1 -Scenario s1a

   # Skenario S1b: Overhead (Dengan Metrik)
   ./tests/run_all_tests.ps1 -Scenario s1b

   # Skenario S2: Skalabilitas Default (Main Compose)
   ./tests/run_all_tests.ps1 -Scenario s2

   # Skenario S3: Perbandingan Express.js vs FastAPI
   ./tests/run_all_tests.ps1 -Scenario s3

   # Skenario S4a: Load Balancing via Kafka Native
   ./tests/run_all_tests.ps1 -Scenario s4a

   # Skenario S4b: Load Balancing via NGINX + HTTP
   ./tests/run_all_tests.ps1 -Scenario s4b
   ```
   *Catatan: Anda dapat menginterupsi eksekusi dengan `Ctrl+C` apabila dirasa cukup, namun untuk data yang solid biarkan skrip menyelesaikan durasinya.*

---

## 5. Tahap 4: Validasi Output Data (Pasca-Pengujian)

Tahap ini dilakukan untuk memastikan bahwa data empiris telah siap diolah untuk penulisan **Bab IV (Hasil & Analisis)** skripsi Anda.

**Langkah-langkah:**
1. Buka folder `tests/results/` di dalam direktori proyek.
2. Pastikan file-file `.csv` telah tercipta (misal: `s4b_nginx_lb.csv`).
3. Buka file `.csv` tersebut menggunakan Excel atau text editor.
   *Ekspektasi: File CSV berisi kolom-kolom metrik (Timestamp, CPU, RAM, Latency P95, dsb) dan baris-baris data angka yang tidak bernilai `0.0` (kecuali memang tidak ada trafik).*
4. Validasi InfluxDB (Opsional):
   - Buka `http://localhost:8086`.
   - Cek di *Data Explorer* apakah arsip data `trace` seismik telah tersimpan (memverifikasi bahwa pipeline tetap berjalan normal meskipun diobservasi).

---

## 6. Troubleshooting (Penyelesaian Masalah)

Jika Anda menemui kendala saat pengujian:
- **Container Exited / Crash:** Periksa log container spesifik dengan perintah `docker logs <nama_container>`. Contoh: `docker logs p_wave_detector_1`.
- **Script PowerShell Error (`UnauthorizedAccess`):** Jika skrip gagal berjalan di Windows karena aturan sekuriti, eksekusi perintah ini terlebih dahulu di PowerShell (sebagai Administrator): `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.
- **Metrik CSV berisi 0.0 semua:** Pastikan Anda menjalankan skenario yang memiliki metrics (S1b, S2, S3, S4a, S4b). Skenario S1a (*tanpa metrics*) memang mematikan endpoint prometheus. Jika terjadi di skenario lain, pastikan Data Provider memproduksi data dan Kafka tidak bermasalah (lihat log Kafka).
