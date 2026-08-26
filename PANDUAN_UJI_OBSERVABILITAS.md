# Panduan Validasi dan Pengujian Sistem EEWS

Dokumen ini memandu pengoperasian, validasi, pengambilan screenshot, dan pengumpulan data untuk sistem EEWS berbasis Docker, Kafka, microservices, Prometheus, Grafana, MongoDB, dan InfluxDB.

---

## 1. Prasyarat

Windows membutuhkan Docker Desktop, Git, Python 3.10+, PowerShell, RAM minimal 8 GB, dan ruang kosong minimal 30 GB. VM Ubuntu membutuhkan Docker Engine, Docker Compose Plugin, Git, akses internet, minimal 4 vCPU, RAM 8 GB, dan ruang kosong 30 GB.

Periksa versi:

```bash
docker --version
docker compose version
git --version
python --version
```

Install library pengumpul metric pada host:

```bash
python -m pip install requests
```

---

## 2. Mengambil Source Code dan Environment

Clone pertama kali:

```bash
git clone https://github.com/mohamadsolkhannawawi/MDLBEEWS-V3.git
cd ~/MDLBEEWS-V3
```

Update berikutnya:

```bash
cd ~/MDLBEEWS-V3
git pull origin main
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
Copy-Item influxDB\.env.example influxDB\.env
```

Ubuntu VM:

```bash
cp .env.example .env
cp influxDB/.env.example influxDB/.env
```

Validasi:

```bash
ls -la .env influxDB/.env
docker compose config
```

Jangan commit `.env`. Jika muncul permission denied:

```bash
sudo chown -R $USER:$USER ~/MDLBEEWS-V3/influxDB
chmod 755 ~/MDLBEEWS-V3/influxDB
chmod 600 ~/MDLBEEWS-V3/influxDB/.env
```

---

## 3. Build dan Startup

Build dan start:

```bash
docker compose up -d --build
docker compose ps
```

Container utama harus `Up (healthy)`: `api_server`, `fast_api`, `data_provider`, `p_wave_detector`, `loc_mag_detector`, dan `data_archiver`. Kafka dan Zookeeper harus `Up`, bukan `Restarting` atau `Exited`.

Untuk rebuild satu service:

```bash
docker compose build --no-cache --progress=plain data_archiver
docker compose build --no-cache --progress=plain data_provider
docker compose build --no-cache --progress=plain p_wave_detector
docker compose build --no-cache --progress=plain loc_mag_detector
```

---

## 4. URL dan Login

Gunakan URL ini pada host Docker. Untuk komputer lain, ganti `localhost` dengan IP host atau VM.

| Komponen | URL |
|---|---|
| Express data table | `http://localhost:3333` |
| Express metrics | `http://localhost:8107/metrics` |
| FastAPI WebSocket | `http://localhost:3334` |
| FastAPI health | `http://localhost:3334/health` |
| Grafana | `http://localhost:4000` |
| Prometheus targets | `http://localhost:9090/targets` |
| Prometheus graph | `http://localhost:9090/graph` |
| InfluxDB | `http://localhost:8086` |
| Mongo Express | `http://localhost:8081` |

Port `3333` adalah Express API. Port `3334` pada host diteruskan ke port internal FastAPI `3333`.

Grafana login: `admin` / `12345678`.

InfluxDB login: username `admin`, password `12345678`, organization `owner`, bucket `eews`.

Mongo Express login: username `admin`, password `password`.

Tes endpoint:

```bash
curl http://localhost:3333
curl http://localhost:3334/health
curl http://localhost:8107/metrics
```

## 5. Validasi Prometheus dan Grafana

Di `http://localhost:9090/targets`, target aktif seperti `data_provider`, `p_wave_detector`, `loc_mag_detector`, `data_archiver`, `api_server`, dan `fast_api` harus UP. Target load balancer boleh gagal jika servicenya dikomentari di Compose.

Di Prometheus Graph, jalankan query berikut satu per satu:

```promql
up
```

```promql
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
```

```promql
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / 1024 / 1024
```

```promql
rate(data_provider_traces_sent_total[1m])
```

```promql
histogram_quantile(0.95, rate(pwave_inference_latency_seconds_bucket[1m]))
```

```promql
histogram_quantile(0.95, rate(locmag_inference_latency_seconds_bucket[1m]))
```

Screenshot harus menampilkan URL, query, rentang waktu, dan hasil tabel/grafik.

Di Grafana, login lalu buka dashboard EEWS, pilih **Last 15 minutes**, tunggu 1 sampai 5 menit, dan pastikan panel CPU, memory, request, latency, atau delay berisi data.

---

## 6. Screenshot yang Wajib Diambil

Ambil screenshot berikut:

1. `docker compose ps` dengan container aktif.
2. `http://localhost:3333` dengan record trace.
3. `http://localhost:3334` dengan WebSocket Client.
4. `http://localhost:8107/metrics` dengan metric mentah.
5. `http://localhost:9090/targets` dengan target UP.
6. Prometheus Graph query `up`.
7. Prometheus Graph CPU atau memory.
8. Grafana dashboard dengan grafik terisi.
9. InfluxDB Data Explorer.
10. Mongo Express bila bukti database diperlukan.

Jangan tampilkan password, token, isi `.env`, atau secret pada screenshot.

---

## 7. Mengumpulkan Data CSV

Jalankan dari root repository setelah Compose stabil:

```bash
python tests/collect_metrics.py --duration 120 --interval 5 --output tests/results/s2_scalability.csv
```

Ubuntu dapat memakai `python3` dan perlu `python3 -m pip install requests`. Periksa hasil:

```bash
head -5 tests/results/s2_scalability.csv
wc -l tests/results/s2_scalability.csv
```

CSV harus memiliki header dan banyak timestamp. Nilai 0 dapat normal untuk metric tanpa traffic.

## 8. Skenario Pengujian

Script `tests/run_all_tests.ps1` berjalan di Windows PowerShell. Jalankan:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
./tests/run_all_tests.ps1 -Scenario s1a
./tests/run_all_tests.ps1 -Scenario s1b
./tests/run_all_tests.ps1 -Scenario s2
./tests/run_all_tests.ps1 -Scenario s3
./tests/run_all_tests.ps1 -Scenario s4a
./tests/run_all_tests.ps1 -Scenario s4b
```

Untuk semua skenario: `./tests/run_all_tests.ps1 -Scenario all`.

Di Ubuntu, file `.ps1` tidak berjalan langsung di Bash. Jalankan Compose file secara manual, kumpulkan CSV dengan `tests/collect_metrics.py`, dan lakukan `docker compose down` sebelum berganti skenario.

## 9. Pemeriksaan Log dan Troubleshooting

```bash
docker compose logs --tail=100 data_provider
docker compose logs --tail=100 p_wave_detector
docker compose logs --tail=100 loc_mag_detector
docker compose logs --tail=100 data_archiver
docker compose logs --tail=100 api_server
docker compose logs --tail=100 fast_api
```

Error `ModuleNotFoundError: tensorflow` berarti detector perlu dibuild ulang. Error model `model_*.h5` berarti file model belum tersedia di image. Error `stations.json` berarti path data provider salah atau file tidak ikut image. Error `ECONNREFUSED` Kafka dapat terjadi selama startup; tunggu 30 sampai 60 detik dan cek broker.

Untuk masalah build:

```bash
docker builder prune -af
docker compose build --no-cache --progress=plain <service>
```

Gunakan `docker compose down -v` hanya jika memang ingin menghapus seluruh volume data.

## 10. Checklist Kelulusan

- [ ] `.env` dan `influxDB/.env` tersedia.
- [ ] `docker compose config` berhasil.
- [ ] Semua image berhasil dibangun.
- [ ] Container utama berstatus `Up (healthy)`.
- [ ] Kafka dan Zookeeper berstatus `Up`.
- [ ] Data Table menampilkan trace.
- [ ] WebSocket Client terbuka.
- [ ] Endpoint metrics menampilkan teks Prometheus.
- [ ] Target Prometheus utama berstatus UP.
- [ ] Grafana login dan dashboard berisi grafik.
- [ ] InfluxDB bucket `eews` tersedia.
- [ ] Tidak ada error model atau file data pada log.
- [ ] CSV memiliki header dan baris data.
- [ ] Screenshot tidak berisi credential atau token.

Catat untuk setiap skenario: nama skenario, waktu, mesin/VM, CPU/RAM, versi Docker, Compose file, durasi, jumlah replica, nama CSV, nama screenshot, status container, status target Prometheus, dan error yang ditemukan.
