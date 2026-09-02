# BAB III
# METODE PENELITIAN

Bab ini membahas jenis dan pendekatan penelitian, tahap perancangan arsitektur sistem, implementasi sistem, hingga perancangan skenario pengujian. Bab ini menjelaskan bagaimana lapisan observabilitas Prometheus dan Grafana dirancang dan diintegrasikan ke dalam *pipeline* EEWS, serta metode yang digunakan untuk mengukur performanya.

**Gambar 3.1 Alur Metodologi Penelitian**
*Mulai → (3.1) Jenis & Pendekatan Penelitian dan Definisi Variabel → (3.2) Studi Literatur & Analisis Kebutuhan → (3.3) Perancangan Arsitektur Sistem → (3.4) Implementasi Sistem → (3.5) Perancangan Skenario Pengujian → (3.6) Pengumpulan dan Analisis Data → Selesai*

Gambar 3.1 menampilkan alur metodologi penelitian secara menyeluruh dalam bentuk diagram alir linear, mengikuti pola tahapan yang berurutan dari awal hingga akhir penelitian. Alur ini bersifat eksperimental dan tidak iteratif, karena setiap tahap pada dasarnya dikerjakan satu kali secara berurutan hingga seluruh skenario pengujian selesai dilaksanakan dan data dianalisis, berbeda dengan pola pengembangan bertahap-berulang seperti *Scrum* maupun pola bertingkat-milestone seperti ICONIX. Keenam tahap pada Gambar 3.1 selaras 1-ke-1 dengan struktur Sub Bab 3.1 hingga 3.6 pada bab ini; pelaksanaan pengujian aktual serta hasil dan pembahasan tiap skenario yang diperoleh dari tahap 3.6 akan diuraikan secara rinci pada Bab IV.

## 3.1 Jenis dan Pendekatan Penelitian

Penelitian ini tergolong penelitian eksperimental (*experimental research*) dengan pendekatan kuantitatif, yaitu penelitian yang mencari pengaruh perlakuan tertentu terhadap variabel lain dalam kondisi terkendali dan dianalisis menggunakan statistik. Perlakuan yang dimaksud pada penelitian ini berupa variasi konfigurasi sistem, seperti aktif/tidaknya instrumentasi Prometheus, jumlah *instance* suatu modul, maupun jenis implementasi komponen tertentu, yang diperkirakan memengaruhi performa sistem EEWS berupa latensi komunikasi, penggunaan CPU, penggunaan memori, dan *data delay end-to-end*. Hubungan sebab-akibat antara perlakuan dan performa inilah yang hendak diamati secara terkendali melalui rangkaian skenario pengujian pada Sub Bab 3.5.

Penelitian ini menegaskan prinsip satu variabel bebas per rangkaian pengujian, mengadopsi pola yang telah dibahas pada Sub Bab 2.2.9, yaitu memvariasikan satu variabel bebas pada satu rangkaian pengujian sementara variabel lain dijaga konstan sebagai variabel kontrol (Raptis dkk., 2024). Prinsip ini diterapkan secara konsisten pada keempat skenario S1–S4 yang dirancang pada Sub Bab 3.5, sehingga setiap skenario hanya memanipulasi satu variabel bebas tunggal. Dengan demikian, pengaruh masing-masing variabel bebas terhadap variabel terikat dapat diamati secara terisolasi tanpa tercampur oleh pengaruh variabel bebas lain.

Definisi variabel penelitian secara lengkap ditunjukkan pada Tabel 3.1.

**Tabel 3.1 Definisi Variabel Penelitian**

| Jenis Variabel | Rincian |
|---|---|
| Variabel bebas | Ada/tidaknya instrumentasi Prometheus pada seluruh modul (S1); jumlah *instance* P-Wave Detector/Data Archiver (S2); jenis implementasi WebSocket Server, Express.js/Socket.IO atau FastAPI (S3); konfigurasi *load balancing*, Kafka saja atau Kafka+NGINX (S4) — rincian tiap skenario ditunjukkan pada Tabel 3.3 Sub Bab 3.5 |
| Variabel terikat | Latensi komunikasi antar-layanan (ms), penggunaan CPU (%), penggunaan memori (MB), dan *data delay end-to-end* (s) |
| Variabel kontrol | Spesifikasi mesin *host*, dataset seismik (simulasi/historis melalui SeedLink), bobot model *deep learning* (tetap, tidak dilatih ulang), topologi jaringan Kafka, dan profil beban kerja pada tiap skenario (lihat Sub Bab 3.5) |
| Variabel diagnostik pelengkap | *Consumer lag* Kafka — bukan merupakan variabel terikat utama, melainkan dipantau sebagai sinyal tambahan untuk membantu menginterpretasikan penyebab perubahan pada variabel terikat utama, mengadopsi pemantauan tren *consumer lag* sebagaimana telah dibahas pada Sub Bab 2.2.10 (Henning & Hasselbring, 2024) |

Tabel 3.1 menunjukkan bahwa variabel terikat penelitian ini dibatasi pada empat metrik sesuai Ruang Lingkup Bab I, sedangkan *consumer lag* Kafka diposisikan sebagai variabel diagnostik pelengkap agar tidak memperluas ruang lingkup yang telah ditetapkan. Variabel bebas berbeda-beda untuk tiap skenario pengujian, sehingga rincian keempatnya baru diuraikan secara lengkap pada Sub Bab 3.5 bersamaan dengan profil beban kerja yang menyertainya.

## 3.2 Studi Literatur dan Analisis Kebutuhan

Studi literatur pada tahap ini merupakan kelanjutan langsung dari studi literatur yang telah dijelaskan pada Sub Bab 2.1, bukan proses studi literatur yang terpisah. Penelusuran pustaka dilakukan melalui basis data jurnal terindeks Scopus dengan rentang tahun publikasi 2020–2026, sehingga hasil tinjauan pustaka pada Bab II sekaligus menjadi dasar analisis kebutuhan sistem pada tahap ini. Hasil tinjauan tersebut digunakan untuk mengidentifikasi kebutuhan fungsional dan non-fungsional sistem, serta menentukan titik kritis *pipeline* yang menjadi fokus instrumentasi observabilitas.

Kebutuhan fungsional sistem mengacu pada rancangan modul dan alur data yang telah ditetapkan pada dokumen konteks aplikasi, yaitu enam modul utama yang saling terhubung: Data Provider melakukan ingesti data seismik dan mempublikasikannya ke Kafka, P-Wave Detector mendeteksi onset gelombang-P baik melalui mode *consumer* langsung maupun mode *load-balanced* via HTTP, Load Balancer mendistribusikan beban permintaan ke *instance* P-Wave Detector, Location & Magnitude Detector mengestimasi hiposenter dan magnitudo, Data Archiver mengarsipkan data trace mentah, dan WebSocket Server menyebarluaskan data waveform mentah maupun hasil estimasi ke klien secara *real-time*. Keenam modul tersebut menjadi kebutuhan fungsional inti yang harus terpenuhi sebelum lapisan observabilitas ditambahkan di atasnya.

Kebutuhan non-fungsional sistem meliputi target latensi pada jalur kritis, granularitas metrik yang diinstrumentasikan, dan interval *scraping* Prometheus. Ketiga aspek tersebut belum dikunci pada tahap analisis kebutuhan ini dan direncanakan berada pada rentang nilai wajar untuk sistem *time-critical*, dengan nilai akhir baru ditentukan saat implementasi dan pengujian berlangsung [nilai final ditentukan saat implementasi]. Pendekatan ini diambil karena nilai target yang terlalu dini dikunci berisiko tidak realistis terhadap karakteristik beban kerja sesungguhnya yang baru dapat diamati setelah sistem berjalan.

Analisis kebutuhan turut mengidentifikasi jalur Load Balancer menuju P-Wave Detector sebagai titik kritis *pipeline* yang menjadi fokus utama instrumentasi. Jalur ini melibatkan pemanggilan HTTP yang bersifat sinkron di tengah alur *pipeline* yang secara umum bersifat asinkron berbasis Kafka, sehingga berpotensi menjadi sumber *bottleneck* apabila *instance* P-Wave Detector yang dituju mengalami keterlambatan respons. Karakteristik campuran sinkron-asinkron inilah yang menjadikan jalur tersebut prioritas instrumentasi metrik latensi pada Sub Bab 3.4.2, agar potensi *bottleneck* pada jalur tersebut dapat dipantau secara langsung melalui dashboard Grafana.

## 3.3 Perancangan Arsitektur Sistem

Perancangan arsitektur sistem dimulai dengan menetapkan komponen-komponen yang menyusun keseluruhan sistem beserta teknologi dan protokol komunikasi yang digunakan, sebagaimana ditunjukkan pada Tabel 3.2.

**Tabel 3.2 Komponen Arsitektur Sistem**

| Modul | Teknologi | Protokol Komunikasi | Topik Kafka Terkait | Deskripsi Fungsi |
|---|---|---|---|---|
| Data Provider | Python, ObsPy, SeedLink, kafka-python | Kafka producer | `trace_topic` (produce, seluruh channel untuk arsip), `p_wave_topic` (produce, channel-Z untuk jalur deteksi) | Melakukan ingesti data seismik mentah dari sumber SeedLink dan mempublikasikannya ke Kafka, memisahkan trace lengkap untuk pengarsipan dan trace channel-Z untuk jalur deteksi gelombang-P. |
| P-Wave Detector (mode *consumer*) | Python, TensorFlow, kafka-python | Kafka consumer → producer | `p_wave_topic` (consume), `loc_mag_topic` (produce) | Mendeteksi onset gelombang-P dari trace mentah secara langsung sebagai konsumen Kafka. |
| P-Wave Detector (mode *load-balanced*) | Python, FastAPI, TensorFlow | HTTP endpoint (dipanggil Load Balancer) → Kafka producer | `loc_mag_topic` (produce) | Menyediakan fungsi deteksi gelombang-P yang sama melalui endpoint HTTP agar dapat diskalakan secara horizontal oleh Load Balancer. |
| Load Balancer | Python, kafka-python, requests | Kafka consumer → HTTP client | `p_wave_topic` (consume) | Mengonsumsi data terkait deteksi dari Kafka dan meneruskan payload melalui HTTP ke salah satu *instance* P-Wave Detector mode *load-balanced*. |
| Location & Magnitude Detector | Python, TensorFlow, kafka-python | Kafka consumer → producer | `loc_mag_topic` (consume), `result_loc_mag_topic` (produce) | Mengestimasi hiposenter dan magnitudo gempa berdasarkan hasil deteksi gelombang-P. |
| Data Archiver | Python, kafka-python, MongoDB, InfluxDB, ObsPy | Kafka consumer | `trace_topic` (consume) | Mengarsipkan data trace mentah ke basis data untuk kebutuhan penyimpanan jangka panjang. |
| WebSocket Server (Express.js/Socket.IO) | Node.js, Express, Socket.IO, kafkajs | Kafka consumer → WebSocket | `trace_topic` (consume), `result_loc_mag_topic` (consume) | Meneruskan data waveform mentah dan hasil estimasi lokasi-magnitudo ke klien secara *real-time* melalui dua jalur konsumsi Kafka yang berjalan paralel. |
| WebSocket Server (FastAPI) | Python, FastAPI, kafka-python | Kafka consumer → WebSocket | `trace_topic` (consume), `result_loc_mag_topic` (consume) | Menyediakan alternatif implementasi WebSocket Server berbasis *native* WebSocket sebagai pembanding performa terhadap varian Express.js/Socket.IO, dengan pola konsumsi topik yang sama. |
| NGINX | NGINX | HTTP proxy | — | Berperan sebagai *reverse proxy* untuk endpoint HTTP P-Wave Detector mode *load-balanced*, sebagai alternatif terhadap modul Load Balancer kustom berbasis Kafka *consumer*. |
| Kafka Cluster | Kafka multi-*broker* | — | `trace_topic`, `p_wave_topic`, `loc_mag_topic`, `result_loc_mag_topic` | Menjadi *message broker* terdistribusi yang menghubungkan seluruh modul *pipeline* EEWS. |
| Prometheus Server | Prometheus | HTTP *scraping* (`/metrics`) | — | Melakukan *scraping* metrik secara periodik dari endpoint `/metrics` tiap modul serta dari Node Exporter. |
| Node Exporter | Node Exporter | HTTP (diekspos ke Prometheus Server) | — | Mengekspos metrik level *host* (CPU, memori, disk, jaringan) agar dapat di-*scrape* Prometheus Server. |
| Grafana Dashboard | Grafana | HTTP (terhubung ke Prometheus Server) | — | Memvisualisasikan metrik yang dikumpulkan Prometheus Server dalam bentuk *dashboard* interaktif. |

Tabel 3.2 menunjukkan bahwa Data Provider memproduksi dua topik Kafka sekaligus, yaitu `trace_topic` yang memuat trace seismik lengkap untuk keperluan pengarsipan oleh Data Archiver, dan `p_wave_topic` yang memuat trace channel-Z terpilih untuk jalur deteksi gelombang-P oleh P-Wave Detector maupun Load Balancer — pemisahan ini menjadikan `p_wave_topic` selalu memiliki produsen yang jelas sebelum dikonsumsi oleh kedua jalur deteksi tersebut. Tabel 3.2 juga menunjukkan bahwa lapisan observabilitas (Prometheus Server, Node Exporter, Grafana Dashboard) tidak memiliki topik Kafka terkait karena keduanya berkomunikasi melalui mekanisme *scraping* HTTP, berbeda dengan modul inti EEWS yang saling terhubung melalui Kafka. Perbedaan pola komunikasi ini menjadi pertimbangan penting saat menggambarkan topologi arsitektur secara visual pada Gambar 3.2.

**Gambar 3.2 Diagram *Container* C4 Model**

Gambar 3.2 digambarkan menggunakan notasi *Container diagram* C4 *Model* sebagaimana telah dijelaskan pada Sub Bab 2.2.8.3, bukan diagram blok atau diagram komponen generik. Diagram ini menampilkan enam modul EEWS (Data Provider, P-Wave Detector, Load Balancer, Location & Magnitude Detector, Data Archiver, WebSocket Server) beserta tiga *container* lapisan observabilitas (Prometheus Server, Node Exporter, Grafana Dashboard), dengan masing-masing modul digambarkan sebagai satu *container* independen lengkap dengan label teknologi yang digunakan. Panah antar-*container* diberi label protokol komunikasi sesuai Tabel 3.2, yaitu Kafka, HTTP, atau WebSocket, sedangkan titik instrumentasi `/metrics` pada tiap modul EEWS ditandai secara eksplisit sebagai elemen visual utama untuk menegaskan bahwa observabilitas dirancang sebagai bagian melekat dari arsitektur, bukan tempelan yang ditambahkan belakangan.

**Gambar 3.3 Data Flow Diagram (DFD) Level Konteks dan Level 0**

Gambar 3.3 menggunakan notasi DFD yang telah dijelaskan pada Sub Bab 2.2.8.4, digambarkan secara berjenjang mulai dari diagram konteks yang menampilkan sistem EEWS sebagai satu proses tunggal beserta entitas eksternal di sekitarnya, kemudian diturunkan menjadi Diagram 0 yang memperlihatkan alur data seismik secara logis dari Data Provider hingga WebSocket Server. Diagram ini sengaja tidak menampilkan detail protokol komunikasi seperti Kafka atau HTTP, karena DFD menekankan pergerakan data secara abstrak, berbeda dengan Gambar 3.2 yang bersifat arsitektural maupun Gambar 3.4 yang bersifat prosedural-temporal. Dengan demikian, Gambar 3.3 berperan sebagai jembatan pemahaman antara topologi *container* pada Gambar 3.2 dan urutan interaksi antar-layanan pada Gambar 3.4.

**Gambar 3.4 Sequence Diagram Alur Data Seismik**

Gambar 3.4 menggambarkan interaksi antar-layanan berdasarkan urutan waktu, mulai dari Data Provider melakukan ingesti data seismik dan mempublikasikannya secara paralel ke `trace_topic` (trace lengkap) dan `p_wave_topic` (trace channel-Z), dilanjutkan proses deteksi gelombang-P melalui `p_wave_topic`, estimasi lokasi dan magnitudo melalui `loc_mag_topic`, hingga diseminasi hasil ke klien melalui `result_loc_mag_topic` dan WebSocket. WebSocket Server turut digambarkan mengonsumsi `trace_topic` secara langsung untuk meneruskan data waveform mentah ke klien, berjalan paralel terhadap jalur konsumsi `result_loc_mag_topic` untuk hasil estimasi. Titik *scraping* metrik oleh Prometheus Server turut disertakan pada diagram ini sebagai interaksi tambahan yang berjalan paralel terhadap alur data utama, untuk menegaskan bahwa proses pemantauan berlangsung bersamaan dengan pemrosesan data seismik, bukan sebagai proses terpisah yang dijalankan setelahnya.

Skema topik Kafka yang dirancang terdiri atas empat topik utama, yaitu `trace_topic` untuk data trace seismik lengkap dari Data Provider yang dikonsumsi Data Archiver untuk keperluan arsip sekaligus WebSocket Server untuk diseminasi waveform mentah ke klien, `p_wave_topic` untuk data trace channel-Z dari Data Provider yang dikonsumsi jalur deteksi gelombang-P (baik mode *consumer* maupun mode *load-balanced* melalui Load Balancer), `loc_mag_topic` untuk metadata hasil deteksi gelombang-P yang menjadi masukan Location & Magnitude Detector, dan `result_loc_mag_topic` untuk hasil estimasi lokasi dan magnitudo yang dikonsumsi WebSocket Server. Keempat topik tersebut menjadi tulang punggung komunikasi asinkron antar-modul, sebagaimana ditunjukkan pada Tabel 3.2 dan divisualisasikan pada Gambar 3.2 hingga Gambar 3.4.

## 3.4 Implementasi Sistem

### 3.4.1 Implementasi Pipeline Inti EEWS

Implementasi Data Provider mencakup proses ingesti data seismik dari sumber SeedLink menggunakan pustaka ObsPy, dengan data yang digunakan berupa data simulasi atau data historis sesuai Ruang Lingkup Bab I. Data Provider menyediakan beberapa varian strategi eksekusi, yaitu sekuensial, *multithread*, *multiprocess*, dan kombinasi keduanya, untuk mengakomodasi kebutuhan pengujian skalabilitas pada Sub Bab 3.5. Data yang telah diingesti kemudian dipublikasikan ke `trace_topic` agar dapat dikonsumsi oleh modul-modul berikutnya dalam *pipeline*.

Implementasi P-Wave Detector disediakan dalam dua mode sesuai Tabel 3.2, yaitu mode *consumer* langsung yang mengonsumsi `p_wave_topic` dan langsung memproses deteksi gelombang-P menggunakan model *deep learning* yang telah tersedia, serta mode *load-balanced* yang mengekspos fungsi deteksi yang sama melalui endpoint HTTP `POST /trace` agar dapat diskalakan secara horizontal. Kedua mode P-Wave Detector diimplementasikan sebagai konfigurasi *deployment* yang terpisah dan tidak pernah diaktifkan bersamaan dalam satu *environment* yang sama: mode *consumer* dipakai pada konfigurasi Kafka murni tanpa komponen *load balancing* tambahan, sedangkan mode *load-balanced* selalu di-*deploy* bersama Load Balancer dan NGINX sekaligus di depan sekumpulan replika P-Wave Detector yang sama, dengan NGINX bertindak sebagai *reverse proxy* HTTP tambahan yang meneruskan permintaan ke pool replika tersebut. Load Balancer bertugas mengonsumsi data terkait deteksi dari Kafka dan meneruskannya melalui HTTP ke salah satu *instance* P-Wave Detector mode *load-balanced* menggunakan strategi distribusi beban tertentu, sehingga beban permintaan dapat dibagi merata antar-*instance* yang tersedia.

Location & Magnitude Detector mengonsumsi hasil deteksi gelombang-P dari `loc_mag_topic` untuk mengestimasi hiposenter dan magnitudo gempa menggunakan model *deep learning* yang telah tersedia sebelumnya, kemudian mempublikasikan hasil estimasi ke `result_loc_mag_topic`. Data Archiver secara paralel mengonsumsi `trace_topic` untuk mengarsipkan data trace mentah ke basis data, guna memenuhi kebutuhan penyimpanan jangka panjang yang terpisah dari kebutuhan pemrosesan *real-time*.

Implementasi WebSocket Server disediakan dalam dua varian, yaitu Express.js/Socket.IO dan FastAPI *native* WebSocket, yang keduanya mengonsumsi dua topik Kafka secara paralel — `trace_topic` untuk meneruskan data waveform mentah ke klien secara *real-time*, dan `result_loc_mag_topic` untuk meneruskan hasil estimasi lokasi-magnitudo begitu tersedia. Penyediaan lebih dari satu implementasi WebSocket Server dilakukan agar performa kedua varian dapat dibandingkan secara langsung pada skenario pengujian S3, mengingat keduanya dapat memiliki karakteristik performa yang berbeda meskipun menjalankan fungsi yang sama.

### 3.4.2 Implementasi Instrumentasi Prometheus

Instrumentasi Prometheus diimplementasikan menggunakan pustaka `prometheus_client` pada modul-modul berbasis Python, serta pustaka padanan untuk modul WebSocket Server berbasis Node.js, sehingga seluruh modul dalam Tabel 3.2 memiliki mekanisme ekspos metrik yang konsisten. Jenis metrik yang diinstrumentasikan pada tiap modul mengikuti pola Counter, Gauge, dan Histogram, diturunkan dari rancangan rencana metrik pada dokumen konteks aplikasi, misalnya Counter untuk jumlah total pesan yang diproses atau *error* yang terjadi, Gauge untuk kondisi terkini seperti jumlah klien WebSocket aktif, dan Histogram untuk distribusi latensi seperti latensi inferensi model maupun latensi *forward* pada Load Balancer.

Setiap modul mengekspos endpoint `/metrics` pada port unik agar tidak terjadi tumpang tindih saat *scraping* dilakukan oleh Prometheus Server. Konfigurasi `prometheus.yml` menetapkan seluruh endpoint tersebut sebagai *scrape target*, ditambah target Node Exporter untuk metrik level *host*, dengan interval *scraping* yang berada pada rentang nilai wajar untuk sistem *time-critical* dan belum dikunci nilainya pada tahap perancangan ini [nilai final ditentukan saat implementasi].

### 3.4.3 Implementasi Dashboard Grafana

Implementasi dashboard Grafana pada penelitian ini menambahkan *datasource* Prometheus yang secara eksplisit dipisahkan dari *datasource* InfluxDB yang sudah lebih dahulu digunakan untuk menampilkan data arsip seismik pada sistem yang telah berjalan. Pemisahan ini ditegaskan agar dashboard observabilitas yang dirancang pada penelitian ini tidak dipahami sebagai perluasan dari dashboard arsip yang sudah ada, melainkan sebagai lapisan pemantauan performa sistem yang berdiri sendiri dan menjadi kontribusi utama penelitian ini.

Rancangan panel dashboard mencakup empat kelompok metrik utama, yaitu latensi per modul, penggunaan CPU dan memori, *data delay end-to-end*, serta jumlah klien WebSocket aktif. Jenis visualisasi dipilih menyesuaikan karakteristik masing-masing metrik: grafik *time-series* digunakan untuk metrik yang berubah terhadap waktu seperti latensi dan penggunaan CPU/memori, *gauge* digunakan untuk metrik berupa nilai terkini seperti jumlah klien aktif, sedangkan *heatmap* digunakan untuk memvisualisasikan distribusi latensi pada rentang waktu tertentu secara lebih rinci.

### 3.4.4 Konfigurasi Docker Compose

Seluruh komponen sistem, termasuk Prometheus Server, Node Exporter, dan Grafana Dashboard, didefinisikan sebagai *service* pada konfigurasi Docker Compose, lengkap dengan definisi jaringan dan *volume* yang dibutuhkan masing-masing *service*. Konfigurasi jaringan dirancang agar seluruh modul dapat saling berkomunikasi melalui Kafka maupun HTTP dalam satu jaringan Docker yang sama, sedangkan *volume* digunakan terutama untuk menyimpan data persisten seperti hasil arsip dan konfigurasi *dashboard* Grafana.

Konfigurasi *health check* ditambahkan pada tiap *service* agar Prometheus Server hanya mulai melakukan *scraping* setelah target yang dituju benar-benar siap menerima permintaan. Mekanisme ini penting untuk mencegah kegagalan *scraping* pada tahap awal *startup* sistem, terutama ketika beberapa modul memiliki waktu inisialisasi yang berbeda-beda, seperti modul yang perlu memuat model *deep learning* terlebih dahulu sebelum siap melayani permintaan.

## 3.5 Perancangan Skenario Pengujian

Skenario pengujian dirancang agar setiap baris memenuhi prinsip satu variabel bebas per skenario yang telah ditegaskan pada Sub Bab 3.1, dengan kolom profil beban kerja disertakan secara eksplisit sebagai bagian dari rancangan skenario. Rincian kelima skenario ditunjukkan pada Tabel 3.3.

**Tabel 3.3 Skenario Pengujian**

| Kode | Skenario | Variabel Bebas | Profil Beban Kerja | Variabel Terikat yang Diukur |
|---|---|---|---|---|
| S1 | Evaluasi Strategi Konkurensi Ingesti (Data Provider) | Jenis strategi konkurensi (Sequential, MT, MP, MP_MT) | Beban konstan (*smooth*) pada ingesti data awal | Waktu eksekusi, CPU/memori agregat |
| S2 | Overhead Instrumentasi Prometheus | Aktif/tidaknya `prometheus_client` di seluruh modul | Beban konstan (*smooth*) pada laju data seismik tetap | Selisih CPU (%), memori (MB), latensi (ms) |
| S3 | Skalabilitas Multi-Container (P-Wave Detector & Data Archiver) | Jumlah *instance* P-Wave Detector dan Data Archiver | Beban konstan (*smooth*), dinaikkan bertahap mengikuti jumlah *instance* | *Data delay end-to-end* (s), penggunaan CPU/memori agregat |
| S4 | Perbandingan Implementasi WebSocket Server | Jenis implementasi (Express.js/Socket.IO vs FastAPI) | Beban klien bertingkat (*smooth* naik bertahap) | *Data delay* (s), CPU (%), memori (MB), jumlah klien aktif |
| S5 | Observabilitas Kafka + NGINX Load Balancer | Konfigurasi *load balancing* (Kafka saja vs Kafka+NGINX) | Beban *bursty* (lonjakan permintaan mendadak) | *Data delay* (s), CPU (%), memori (MB) |

Alur pengujian pada Tabel 3.3 dirancang saling berkesinambungan, dengan skenario S1 berfungsi sebagai landasan bagi skenario-skenario berikutnya. Skenario S1 bertujuan untuk mengevaluasi strategi konkurensi (sekuensial, *multi-thread*, *multi-process*, atau gabungan) pada tahap ingesti data di hulu. Strategi yang nantinya terbukti memberikan performa terbaik pada pengujian S1 akan diadaptasi secara permanen sebagai konfigurasi dasar (*baseline*) untuk menjalankan skenario S2 hingga S5. Pendekatan ini dirancang untuk memastikan bahwa pengujian komponen hilir—seperti *overhead* metrik, skalabilitas layanan, dan *load balancing*—selalu dilakukan di atas mekanisme suplai data yang paling efisien, sehingga setiap tahapan evaluasi memiliki dasar argumen teknis yang kuat.

Kontras profil beban kerja antara S1–S4 yang memakai beban *smooth* dan S5 yang memakai beban *bursty* diadaptasi langsung dari pola pengujian yang telah dibahas pada Sub Bab 2.2.9/2.2.10 (Tzanettis dkk., 2022). Beban *smooth* pada S1–S4 dipilih agar pengaruh variabel bebas pada tiap skenario dapat diamati pada kondisi laju permintaan yang stabil, sedangkan beban *bursty* pada S5 sengaja digunakan sebagai pembanding untuk menguji ketahanan konfigurasi *load balancing* saat menghadapi lonjakan permintaan mendadak, bukan sekadar variasi acak tanpa dasar rujukan.

Setiap skenario pada Tabel 3.3 dijalankan melalui prosedur pengujian yang identik lintas skenario, mengadaptasi kerangka otomatisasi eksperimen *reusable* yang telah dibahas pada Sub Bab 2.2.10 (Raptis dkk., 2024). Prosedur tersebut mencakup empat tahap berurutan: (1) *reset*/*restart* seluruh *container* ke kondisi awal agar tidak ada pengaruh dari pengujian sebelumnya, (2) menjalankan pembangkit beban sesuai profil yang telah ditentukan pada Tabel 3.3, (3) mengumpulkan metrik melalui Prometheus API selama durasi pengujian yang tetap, dan (4) menyimpan hasil mentah. Setiap skenario dijalankan dengan durasi pengujian konstan selama 120 detik guna mengumpulkan sampel data *time-series* yang memadai untuk menjaga stabilitas statistik hasil pengukuran, mengacu pada prinsip *reproducibility* yang telah dibahas pada Sub Bab 2.2.10 (Henning & Hasselbring, 2024).

### 3.5.1 Pemetaan Skenario ke Implementasi

Untuk menjamin rekam jejak (*traceability*) antara rancangan skenario dengan implementasi teknis pada *codebase*, pemetaan skenario terhadap skrip pengujian utama dan konfigurasi Docker Compose dijabarkan pada Tabel 3.4.

**Tabel 3.4 Pemetaan Skenario Pengujian ke Implementasi Skrip dan Konfigurasi**

| Skenario | Skrip Uji Utama (`tests/`) | Konfigurasi Docker Compose |
|---|---|---|
| **S1** | `run_s1_dataprovider.ps1` | `1-1.yml` – `1-4.yml` (strategi eksekusi berbeda) |
| **S2** | `run_s2_overhead.ps1` | `5-1.yml` (tanpa metrik) vs `5-2.yml` (metrik aktif) |
| **S3** | `run_s3_scalability_pwave.ps1` & `run_s3_scalability_archiver.ps1` | `3-6.yml` – `3-13.yml` (P-Wave) & `3-1.yml` – `3-5.yml` (Archiver) |
| **S4** | `run_s4_websocket.ps1` | `4-1.yml` (Express) vs `4-2.yml` (FastAPI) |
| **S5** | `run_s5_loadbalancer.ps1` | `2-1.yml` (Kafka murni) vs `2-2.yml` (Kafka+NGINX) |

Tabel 3.4 menjabarkan secara konkret bagaimana kelima rancangan skenario pengujian (S1–S5) diterjemahkan ke dalam komponen *codebase* repositori. Skrip pengujian utama (*main test runner*) berbasis PowerShell (berekstensi `.ps1`) bertugas mengotomatisasi seluruh siklus pengujian, mulai dari inisialisasi lingkungan (*build/up*), injeksi beban (*load testing*), hingga perekaman data (ke format CSV). Masing-masing skrip tersebut akan secara dinamis menjalankan *file* konfigurasi Docker Compose (`.yml`) yang berbeda sesuai dengan arsitektur spesifik yang menjadi variabel bebas pada tiap skenario. Otomatisasi berlapis ini menjamin bahwa setiap tahapan eksperimen dapat dijalankan ulang (*reproducible*) secara konsisten tanpa intervensi manual yang rentan terhadap *human error*.

## 3.6 Pengumpulan dan Analisis Data

Pengumpulan data metrik *time-series* secara umum dilakukan melalui Prometheus API menggunakan PromQL. Pengecualian diterapkan pada Skenario S1 dan sebagian pengujian S2 (skenario tanpa metrik), di mana pengumpulan data profil *container* (seperti CPU dan memori) bersumber dari Docker API (`docker stats`) karena instrumentasi Prometheus belum/tidak diaktifkan. Sementara itu, *consumer lag* Kafka dipantau sebagai data diagnostik pelengkap sesuai definisi pada Tabel 3.1, bukan sebagai metrik hasil yang dilaporkan tersendiri. Hasil pengujian tiap skenario disimpan dalam format CSV agar dapat diproses lebih lanjut untuk keperluan analisis statistik maupun visualisasi tambahan di luar dashboard Grafana.

Metode analisis data menggunakan statistik deskriptif berupa *mean*, median, standar deviasi, dan persentil ke-95 (P95), dengan justifikasi penggunaan P95 mengikuti pembahasan yang telah diuraikan pada Sub Bab 2.2.10 dan tidak dijelaskan ulang pada bagian ini. Visualisasi data dilakukan melalui grafik *time-series* pada dashboard Grafana untuk pemantauan berkelanjutan, serta *box plot* untuk membandingkan distribusi hasil pengukuran antar-kondisi pengujian, misalnya distribusi pemakaian *resource* dengan dan tanpa instrumentasi Prometheus pada skenario S2.

Setiap hasil skenario pengujian pada akhirnya dipetakan kembali ke Rumusan Masalah tunggal pada Bab I, bukan ke beberapa rumusan masalah yang terpisah, mengingat penelitian ini menggunakan satu rumusan masalah payung sebagaimana telah ditetapkan pada Sub Bab 1.2. Skenario S2 secara khusus diarahkan untuk menjawab dimensi *overhead* instrumentasi Prometheus yang disebutkan pada Tujuan Penelitian. Adapun skenario S1 dan S3–S5 secara bersama-sama mengevaluasi performa fungsional maupun skalabilitas dari setiap lapisan arsitektur secara *end-to-end*, sekaligus menjawab dimensi pemantauan performa sistem secara *real-time* dan *reproducible* yang menjadi inti dari Rumusan Masalah penelitian ini.
