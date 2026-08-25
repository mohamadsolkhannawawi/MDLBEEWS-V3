# Rancangan Isi Laporan Skripsi — EEWS Microservices dengan Observabilitas Prometheus & Grafana

> **Fungsi dokumen:** Blueprint/kerangka isi laporan skripsi, disusun agar dapat diberikan ke AI lain (atau dipakai sendiri) sebagai acuan generate tulisan Bab I–V secara konsisten dan esensial — bukan draf final, melainkan peta "apa yang harus dibahas di tiap subbab dan kalimat kunci apa yang harus muncul".
> **Topik:** Perancangan dan implementasi sistem *Earthquake Early Warning System* (EEWS) berbasis arsitektur microservices, menggunakan Apache Kafka sebagai message broker dan WebSocket sebagai mekanisme komunikasi real-time, dengan kontribusi utama berupa lapisan observabilitas berbasis **Prometheus** dan **Grafana**.
> **Bidang:** Rekayasa Perangkat Lunak — Komputasi Tersebar Paralel (*distributed & parallel computing*).
> **Jenis penelitian:** Eksperimental — kuantitatif (perancangan sistem + pengujian performa terukur), **bukan** penelitian berbasis metodologi pengembangan aplikasi bisnis seperti ICONIX Process atau Scrum. Struktur bab mengikuti format baku skripsi Departemen Informatika FSM Undip, tetapi isi tiap bab disesuaikan dengan karakter penelitian eksperimental/benchmarking sistem terdistribusi.
> **Acuan format:** Template resmi *"Template dan Format Penulisan Skripsi"* Departemen Informatika FSM Undip (struktur BAB I–V, aturan penomoran sub-bab, aturan penyajian tabel/gambar/source code, gaya abstrak WHY–WHAT–HOW–CONCLUSION).
> **Acuan gaya penulisan:** Dua contoh skripsi terdahulu (topik chatbot berbasis ICONIX Process, dan topik administrasi berbasis Scrum) dipakai **hanya sebagai referensi gaya kalimat, kedalaman subbab, dan cara menyitasi/menyajikan tabel-gambar** — bukan sebagai acuan metodologi, karena topik penelitian ini bersifat eksperimental/pengukuran performa, bukan pengembangan aplikasi berbasis use case.
> **Acuan khusus Bab I (arahan pembimbing):** kerangka Latar Belakang mengikuti pola *inverted funnel* (Status Quo → What's Wrong → Why This is a Problem → How You Intend to Fix It → Objective); Rumusan Masalah ditentukan lebih dulu dalam bentuk kalimat tanya (satu paragraf jika fokus tunggal, poin bernomor jika fokus majemuk); Tujuan Penelitian ditulis berorientasi hasil/outcome, bukan aktivitas; dan paragraf pembuka tiap bab harus identik verbatim dengan deskripsi bab tersebut di Sub Bab 1.5 Sistematika Penulisan. Detail lengkap ada di Bagian 0 dan Bagian 2 dokumen ini.

---

## 0. Prinsip Penulisan yang Harus Dipatuhi di Seluruh Bab

Bagian ini bukan bab tersendiri, tetapi aturan lintas-bab yang wajib diikuti AI/penulis saat men-generate isi dari kerangka ini:

1. **Satu paragraf = satu gagasan utama, ditopang kalimat utama yang kuat.** Kalimat pertama paragraf harus mampu berdiri sendiri sebagai inti gagasan; kalimat-kalimat berikutnya hanya menjelaskan/mendukung kalimat utama tersebut, bukan menambah gagasan baru yang tidak tercakup oleh kalimat utama.
2. **Idealnya 1 paragraf terdiri atas 3–5 kalimat, tidak "gemuk".** Hindari paragraf bertele-tele atau memuat banyak anak kalimat bersarang. Jika sebuah gagasan butuh lebih dari 5 kalimat untuk dijelaskan tuntas, pecah menjadi dua paragraf — jangan memanjangkan satu paragraf.
3. **Setiap tabel, gambar, source code harus disitasi dalam teks** sebelum atau sesudah kemunculannya (contoh: "...ditunjukkan pada Tabel 3.1", "...seperti pada Gambar 3.2").
4. **Penomoran sub-bab maksimal 4 level** (Bab → Sub Bab → Sub Sub Bab → Sub Sub Sub Bab). Jangan membuat level ke-5.
5. **Bahasa formal ilmiah**, hindari kalimat afektif/berlebihan, hindari kata ganti orang pertama tunggal ("saya") — gunakan bentuk pasif atau "penulis"/"peneliti".
6. **Setiap klaim kuantitatif (angka performa, hasil pengujian) harus merujuk pada data hasil pengujian aktual**, bukan asumsi — bagian ini di kerangka ditandai `[DATA HASIL PENGUJIAN]` sebagai placeholder yang wajib diisi dari eksperimen nyata, tidak boleh dikarang.
7. **Konsisten dalam istilah**: gunakan istilah baku yang sama di seluruh bab, misalnya selalu "Data Provider", "P-Wave Detector", "Load Balancer", "Location & Magnitude Detector", "Data Archiver", "WebSocket Server", "Prometheus Server", "Node Exporter", "Grafana Dashboard" (huruf kapital di awal setiap kata, konsisten sebagai nama modul).
8. **Tidak menyebut versi pustaka/environment spesifik** (Python, Kafka, Docker, dsb.) di badan teks manapun sampai versi final ditentukan — cukup nama teknologi, atau tandai `[versi menyusul]` bila benar-benar diperlukan.
9. **Tidak merujuk ke proyek/paper eksternal sebagai dasar arsitektur** — seluruh sistem diposisikan sebagai rancangan dan implementasi orisinal untuk penelitian ini.
10. **Sitasi mengikuti gaya APA** (Nama dkk., Tahun) seperti pada kedua contoh skripsi acuan, dengan Daftar Pustaka disusun alfabetis.
11. **Paragraf pembuka tiap bab harus identik (verbatim) dengan paragraf deskripsi bab tersebut di Sub Bab 1.5 Sistematika Penulisan.** Kalimat yang dipakai untuk mendeskripsikan "BAB II ..." dsb. pada Sistematika Penulisan harus sama persis, kata per kata, dengan paragraf yang muncul langsung setelah judul bab tersebut di halaman babnya. Berlaku untuk BAB I sampai BAB V — lihat detail dan contoh di Sub Bab 1.5.

---

## 1. ABSTRAK & ABSTRACT

**Aturan format (dari template resmi):** satu paragraf, spasi 1, tanpa indentasi baris pertama, maksimal 300 kata, memuat 4 unsur wajib:

| Unsur | Isi yang harus dibahas untuk topik ini |
|---|---|
| **WHY** (urgensi/latar belakang) | Gempa bumi sebagai bencana yang butuh peringatan dini cepat; sistem EEWS berbasis microservices umumnya sulit dipantau performanya secara real-time dan reproducible karena tidak memiliki lapisan observabilitas terstruktur |
| **WHAT** (apa yang dihasilkan) | Sistem EEWS berbasis microservices (Data Provider, P-Wave Detector, Load Balancer, Location & Magnitude Detector, Data Archiver, WebSocket Server) yang diorkestrasi dengan Kafka dan Docker, dilengkapi lapisan observabilitas Prometheus + Grafana |
| **HOW** (proses implementasi) | Instrumentasi metrik (Counter, Gauge, Histogram) pada setiap modul via `prometheus_client`, scraping periodik oleh Prometheus Server, visualisasi via dashboard Grafana, diuji melalui beberapa skenario (skalabilitas multi-container, perbandingan WebSocket server, overhead instrumentasi, dsb.) |
| **CONCLUSION** (kesimpulan) | Ringkasan `[DATA HASIL PENGUJIAN]`: sistem berhasil diamati secara real-time dan reproducible, dengan overhead instrumentasi yang terukur dan dapat diterima; dashboard mampu memvisualisasikan performa sistem secara komprehensif |

**Kata kunci (draf):** *Earthquake Early Warning System, microservices, Apache Kafka, WebSocket, Prometheus, Grafana, observabilitas*

**Catatan:** ABSTRACT adalah terjemahan maknawi (bukan kata-per-kata) dari ABSTRAK ke bahasa Inggris, dengan aturan format identik.

---

## 2. BAB I — PENDAHULUAN

Kalimat pembuka bab (mengikuti pola template): satu paragraf singkat yang menyebutkan bahwa bab ini menguraikan latar belakang masalah, rumusan masalah, tujuan dan manfaat, ruang lingkup, dan sistematika penulisan dari penelitian mengenai **[Judul final skripsi — draf: "Perancangan dan Implementasi Observabilitas Berbasis Prometheus dan Grafana pada Arsitektur Microservices Earthquake Early Warning System"]**.

> **Penting (lihat Bagian 0 poin 11):** paragraf pembuka ini **harus sama persis, kata per kata**, dengan paragraf yang mendeskripsikan "BAB I PENDAHULUAN" di Sub Bab 1.5 Sistematika Penulisan. Susun kalimat ini sekali, lalu salin verbatim ke kedua tempat — jangan menulis dua versi berbeda yang maknanya sama tapi redaksinya berlainan.

### 1.1 Latar Belakang

**Kerangka wajib (arahan pembimbing):** Latar Belakang disusun dari pembahasan **umum ke khusus**, mengikuti pola *inverted funnel* lima lapis berikut. Setiap lapis idealnya menjadi **satu paragraf** (3–5 kalimat, kalimat utama kuat di awal paragraf) — bukan poin bebas seperti draf sebelumnya:

| Lapis Funnel | Fungsi | Isi untuk topik ini |
|---|---|---|
| **1. Status Quo** (kondisi saat ini) | Menjelaskan kondisi umum yang berlaku sekarang, sebagai pijakan awal pembaca | EEWS berbasis arsitektur microservices sudah menjadi pendekatan umum: setiap tahap pemrosesan (ingesti data seismik, deteksi gelombang-P, estimasi lokasi/magnitudo, diseminasi peringatan) dipisah menjadi layanan independen yang dikontainerisasi, berkomunikasi melalui message broker seperti Kafka dan mekanisme real-time seperti WebSocket. |
| **2. What's wrong with the status quo** | Menunjukkan celah pada kondisi tersebut, tanpa dulu menjelaskan dampaknya | Sistem microservices semacam ini pada umumnya **tidak dilengkapi mekanisme pemantauan operasional yang terstruktur** — performa tiap layanan (latensi, penggunaan CPU/memori, data delay) biasanya hanya diamati secara manual dan sesaat, bukan berkelanjutan dan real-time. |
| **3. Why this is a problem** | Menjelaskan **kenapa** celah tersebut penting/berbahaya, bukan hanya "belum ada" | Ketiadaan observabilitas terstruktur membuat evaluasi performa sistem EEWS sulit direproduksi secara ilmiah, sulit dipakai untuk mendeteksi bottleneck secara dini, dan berisiko pada sistem yang sifatnya *time-critical* seperti EEWS, di mana keterlambatan atau kegagalan layanan idealnya dapat dideteksi sebelum berdampak pada waktu peringatan. |
| **4. How you intend to fix it** | Menjelaskan solusi yang diusulkan penelitian, sebagai jembatan menuju rumusan masalah | Penelitian ini merancang dan mengimplementasikan lapisan observabilitas berbasis **Prometheus** (pengumpulan metrik terstruktur dari tiap modul) dan **Grafana** (visualisasi dashboard real-time) di atas arsitektur EEWS berbasis Kafka dan WebSocket, sehingga performa sistem dapat dipantau dan dianalisis secara berkelanjutan dan reproducible. |
| **5. Objective** (niat & harapan) | **Paragraf penutup** — bukan pernyataan kontribusi teknis lagi, melainkan ungkapan niat/harapan penelitian secara naratif | Melalui rancangan ini, diharapkan sistem EEWS yang dibangun tidak hanya mampu mendeteksi dan menyebarluaskan peringatan gempa, tetapi juga dapat diamati dan dievaluasi performanya secara transparan, sehingga menjadi acuan yang dapat diandalkan bagi pengembangan sistem peringatan dini serupa di masa mendatang. |

**Catatan penerapan:**
- Paragraf 1–4 bersifat argumentatif/teknis dan boleh disitasi dengan pustaka (mengikuti gaya APA, lihat Bagian 0 poin 10).
- Paragraf 5 (**Objective**) ditulis dengan nada **harapan**, bukan klaim capaian — hindari kalimat yang terdengar seperti kesimpulan hasil (itu tempatnya di Bab V), cukup niat/tujuan besar penelitian secara naratif.
- Total Latar Belakang idealnya **5 paragraf**, sesuai 5 lapis funnel di atas — jangan menambah paragraf lain di luar kerangka ini kecuali benar-benar diperlukan.

**Kalimat kunci yang wajib muncul:** "mekanisme pemantauan operasional yang terstruktur", "evaluasi performa secara ilmiah dan reproducible", "Prometheus dan Grafana sebagai lapisan observabilitas".

### 1.2 Rumusan Masalah

**Aturan format (arahan pembimbing):** Rumusan masalah **harus ditentukan lebih dulu**, dalam bentuk kalimat tanya, sebelum menyusun Tujuan Penelitian (Tujuan diturunkan langsung dari Rumusan Masalah, lihat Sub Bab 1.3.1).

- **Jika fokus penelitian hanya satu**, rumusan masalah ditulis sebagai **satu paragraf** berisi satu kalimat tanya utama (tidak dipecah jadi poin-poin).
- **Jika fokus penelitian lebih dari satu dimensi yang benar-benar berbeda**, baru ditulis sebagai **poin bernomor**, masing-masing satu kalimat tanya.

**Penerapan pada topik ini:** perlu ditentukan lebih dulu apakah fokus penelitian ini **tunggal** (observabilitas sebagai satu kesatuan masalah) atau **majemuk** (beberapa dimensi terpisah: arsitektur, metrik, dashboard, overhead).

**Rekomendasi:** gunakan **Opsi A (fokus tunggal)**. Alasannya:

1. **Keempat dimensi di Opsi B bukan empat masalah yang berdiri sendiri, melainkan komponen dari satu solusi yang sama.** Arsitektur (dimensi 1), instrumentasi metrik (dimensi 2), dan dashboard Prometheus/Grafana (dimensi 3) sebenarnya adalah tiga bagian yang bersama-sama membentuk "lapisan observabilitas" — bukan tiga masalah berbeda yang kebetulan diteliti bersamaan. Memecahnya jadi poin terpisah berisiko membuat pembaca (dan penguji sidang) melihat penelitian ini sebagai empat proyek kecil yang longgar keterkaitannya, padahal sebenarnya satu kontribusi yang koheren.
2. **Pengukuran overhead (dimensi 4) lebih tepat diposisikan sebagai bagian dari evaluasi solusi, bukan rumusan masalah yang setara.** Ia adalah pertanyaan validasi ("apakah solusi ini punya biaya?"), bukan masalah yang memicu penelitian ini dilakukan — tempatnya lebih pas di Bab III (metode pengujian) dan Bab IV (hasil), tetap dibahas tuntas tanpa perlu jadi rumusan masalah tersendiri.
3. **Fokus tunggal menghasilkan judul, tujuan, dan kontribusi yang lebih tajam** — memudahkan penyusunan Abstrak (WHY–WHAT–HOW–CONCLUSION harus mengerucut ke satu benang merah) dan memudahkan argumentasi saat sidang karena penguji hanya perlu menilai satu klaim utama, bukan menimbang empat klaim yang levelnya tidak sama.
4. **Selaras dengan pola yang ditunjukkan pembimbing sendiri** (contoh rumusan masalah satu poin karena fokus penelitiannya satu) — ini indikasi kuat gaya penulisan yang diharapkan pada program studi ini condong ke fokus tunggal untuk skripsi S1, bukan multi-rumusan-masalah seperti pada penelitian dengan cakupan lebih luas (tesis/disertasi).

**Cara menjaga keempat dimensi tetap terlihat tanpa memecah rumusan masalah:** keempat dimensi itu tidak hilang — cukup dipindah perannya dari "rumusan masalah" menjadi **struktur turunan** di bab-bab berikutnya: dimensi 1–3 menjadi sub-bab pada Bab III (Perancangan Arsitektur Sistem, Implementasi Instrumentasi Prometheus, Implementasi Dashboard Grafana — lihat Bagian 4 dokumen ini), dan dimensi 4 menjadi salah satu skenario pengujian (S1 — Overhead Instrumentasi Prometheus, lihat Bagian 4 Sub Bab 3.5). Dengan begitu keempatnya tetap dibahas rinci, tetapi payung masalahnya tetap satu.

Dua opsi berikut tetap disiapkan sebagai draf konkret — **gunakan Opsi A**, dan simpan Opsi B hanya sebagai cadangan bila pembimbing secara eksplisit meminta breakdown rumusan masalah menjadi beberapa poin:

**Opsi A — Fokus tunggal (1 paragraf) → ✅ Direkomendasikan:**

> Bagaimana merancang dan mengimplementasikan lapisan observabilitas berbasis Prometheus dan Grafana pada arsitektur microservices Earthquake Early Warning System yang menggunakan Kafka dan WebSocket, sehingga performa sistem — mencakup latensi, penggunaan sumber daya, dan data delay end-to-end — dapat dipantau secara real-time dan dianalisis secara reproducible?

**Opsi B — Fokus majemuk (poin bernomor) → cadangan, pakai hanya jika pembimbing meminta breakdown eksplisit:**

1. Bagaimana merancang arsitektur microservices untuk EEWS yang menggunakan Kafka sebagai message broker dan WebSocket sebagai mekanisme komunikasi real-time?
2. Metrik apa yang perlu diinstrumentasi pada tiap modul agar performa sistem dapat diamati secara real-time dan reproducible?
3. Bagaimana Prometheus dan Grafana dirancang dan diintegrasikan ke dalam pipeline EEWS berbasis Docker agar menghasilkan dashboard yang informatif?
4. Seberapa besar overhead yang ditimbulkan instrumentasi Prometheus terhadap performa sistem EEWS itu sendiri?

> **Penting:** Sub Bab 1.3.1 (Tujuan Penelitian) di bawah mengikuti opsi yang sama dengan yang dipilih di sini — karena Opsi A direkomendasikan, Tujuan Penelitian juga ditulis sebagai satu hasil tunggal (lihat draf Tujuan Opsi A). Opsi B pada Tujuan hanya dipakai jika Opsi B di Rumusan Masalah ini yang dipilih.

### 1.3 Tujuan dan Manfaat

#### 1.3.1 Tujuan Penelitian

**Aturan format (arahan pembimbing):** Tujuan Penelitian diturunkan langsung dari Rumusan Masalah (Sub Bab 1.2), dan **wajib ditulis sebagai HASIL/OUTCOME, bukan sebagai AKTIVITAS**. Artinya, hindari kata kerja proses seperti "merancang", "mengimplementasikan", "mengukur" sebagai kata kerja utama di awal kalimat tujuan (itu menjelaskan *apa yang dikerjakan*, bukan *apa yang dihasilkan*). Gunakan konstruksi yang menonjolkan **produk/keadaan akhir** yang dicapai, misalnya "dihasilkannya...", "diperolehnya...", "tersedianya...", "diketahuinya...".

- Kata kerja proses seperti "merancang", "mengimplementasikan" tetap boleh muncul, tetapi **sebagai penjelas di dalam kalimat**, bukan sebagai kata kerja utama yang membuka kalimat tujuan.
- Tujuan harus **selaras 1-ke-1 dengan Rumusan Masalah** — ikuti opsi yang sama (A atau B) yang dipilih di Sub Bab 1.2.

**Opsi A — Tujuan tunggal (selaras dengan Rumusan Masalah Opsi A) → ✅ Direkomendasikan:**

> Penelitian ini bertujuan untuk menghasilkan arsitektur microservices Earthquake Early Warning System berbasis Kafka dan WebSocket yang dilengkapi lapisan observabilitas Prometheus dan Grafana, sehingga performa sistem dapat dipantau secara real-time dan dianalisis secara reproducible.

**Opsi B — Tujuan majemuk, selaras 1-ke-1 dengan Rumusan Masalah Opsi B (cadangan)** *(perhatikan setiap poin dibuka dengan hasil, bukan aktivitas)*:

1. Dihasilkannya arsitektur microservices EEWS (Data Provider, P-Wave Detector, Load Balancer, Location & Magnitude Detector, Data Archiver, WebSocket Server) yang saling berkomunikasi melalui Kafka dan WebSocket.
2. Diperolehnya seperangkat metrik terstruktur (Counter, Gauge, Histogram) pada setiap modul pipeline yang mampu merepresentasikan kondisi performa sistem secara real-time.
3. Tersedianya dashboard Grafana yang terintegrasi dengan Prometheus Server dan Node Exporter untuk memvisualisasikan performa sistem EEWS secara komprehensif.
4. Diketahuinya besaran overhead yang ditimbulkan instrumentasi Prometheus terhadap performa sistem EEWS melalui pengujian terstruktur.

> **Contoh salah (dihindari) vs benar:** ~~"Merancang dan mengimplementasikan arsitektur microservices EEWS..."~~ (aktivitas) → **"Dihasilkannya arsitektur microservices EEWS..."** (hasil).

#### 1.3.2 Manfaat Penelitian

Dipisah **manfaat teoritis** dan **manfaat praktis** (mengikuti pola proposal eksperimental sebelumnya, lebih lengkap daripada contoh skripsi acuan yang hanya manfaat praktis):

- **Teoritis:** kontribusi pada bidang rekayasa sistem terdistribusi, khususnya kerangka evaluasi performa berbasis observabilitas untuk sistem EEWS; dapat menjadi rujukan metodologis penelitian observabilitas microservices selanjutnya.
- **Praktis:** menyediakan prototipe EEWS yang dilengkapi dashboard monitoring siap pakai bagi komunitas riset kebencanaan; memberi bukti empiris tentang overhead dan manfaat observabilitas pada sistem time-critical seperti EEWS.

### 1.4 Ruang Lingkup

Poin bernomor, harus eksplisit menyebut **batasan yang membedakan penelitian ini dari topik lain**:

1. Sistem dibangun dengan arsitektur microservices, dikontainerisasi menggunakan Docker/Docker Compose pada lingkungan pengembangan lokal.
2. Modul yang dikembangkan: Data Provider, P-Wave Detector, Load Balancer, Location & Magnitude Detector, Data Archiver, WebSocket Server, serta lapisan observabilitas Prometheus Server, Node Exporter, dan Grafana Dashboard.
3. Komunikasi antar-layanan kritis menggunakan HTTP biasa; diseminasi ke klien menggunakan WebSocket. **Tidak menggunakan gRPC/Protocol Buffers atau RPC biner lain.**
4. Data seismik yang digunakan adalah data simulasi/historis (via SeedLink/ObsPy), bukan data sensor fisik langsung.
5. Evaluasi performa difokuskan pada empat metrik: latensi komunikasi (ms), penggunaan CPU (%), penggunaan memori (MB), dan data delay end-to-end (s), seluruhnya diambil melalui Prometheus.
6. Model deep learning untuk deteksi gelombang-P dan estimasi lokasi-magnitudo menggunakan model yang **sudah tersedia/terlatih sebelumnya** — bukan fokus pengembangan model baru.
7. Tidak mencakup deployment ke infrastruktur cloud produksi maupun pengujian pada jaringan sensor seismik fisik sesungguhnya.

### 1.5 Sistematika Penulisan

**Aturan format (arahan pembimbing, lihat juga Bagian 0 poin 11):** Sub Bab ini berisi lima paragraf (satu per bab, BAB I–V). Untuk setiap bab, paragraf yang ditulis di sini **harus sama persis (verbatim)** dengan paragraf pembuka yang muncul langsung setelah judul bab tersebut di halaman babnya masing-masing — bukan dua kalimat berbeda yang kebetulan bermakna sama. Praktiknya: tulis paragraf pembuka satu bab **satu kali saja**, lalu salin-tempel apa adanya ke dua tempat (di halaman bab itu sendiri, dan di sini sebagai entri Sistematika Penulisan).

Setiap paragraf idealnya terdiri atas **dua bagian** (mengikuti pola pada dokumen arahan pembimbing):
1. Kalimat generik yang menyebutkan **apa saja isi bab** (mis. "Bab ini membahas latar belakang penelitian, rumusan masalah, tujuan dan manfaat penelitian, ruang lingkup penelitian, serta sistematika penulisan").
2. Kalimat spesifik yang menegaskan **inti permasalahan/fokus khusus** dari topik penelitian ini yang relevan dengan bab tersebut.

**Draf lima paragraf untuk topik ini** (masing-masing dipakai identik di dua tempat — halaman bab & Sistematika Penulisan):

- **BAB I PENDAHULUAN:** "Bab ini membahas latar belakang penelitian, rumusan masalah, tujuan dan manfaat penelitian, ruang lingkup penelitian, serta sistematika penulisan. Bab ini menjelaskan dasar permasalahan mengenai ketiadaan mekanisme pemantauan operasional yang terstruktur pada arsitektur microservices Earthquake Early Warning System, serta alasan diusulkannya integrasi Prometheus dan Grafana sebagai lapisan observabilitas untuk mengatasi permasalahan tersebut."
- **BAB II TINJAUAN PUSTAKA:** "Bab ini membahas penelitian terdahulu yang relevan serta dasar teori yang mendukung penelitian. Bab ini menguraikan teori mengenai Earthquake Early Warning System, arsitektur microservices, Apache Kafka, WebSocket, serta konsep observabilitas berbasis Prometheus dan Grafana yang menjadi landasan perancangan sistem."
- **BAB III METODE PENELITIAN:** "Bab ini membahas jenis dan pendekatan penelitian, tahap perancangan arsitektur sistem, implementasi sistem, hingga perancangan skenario pengujian. Bab ini menjelaskan bagaimana lapisan observabilitas Prometheus dan Grafana dirancang dan diintegrasikan ke dalam pipeline EEWS, serta metode yang digunakan untuk mengukur performanya."
- **BAB IV IMPLEMENTASI DAN PENGUJIAN:** "Bab ini membahas hasil implementasi sistem sesuai rancangan pada Bab III, beserta hasil pengujian dan pembahasannya. Bab ini menyajikan hasil pengujian performa sistem pada tiap skenario, termasuk analisis overhead yang ditimbulkan oleh instrumentasi Prometheus."
- **BAB V PENUTUP:** "Bab ini membahas kesimpulan dari keseluruhan penelitian serta saran untuk pengembangan lebih lanjut. Bab ini merangkum sejauh mana lapisan observabilitas Prometheus dan Grafana berhasil menjawab permasalahan pemantauan performa pada arsitektur microservices EEWS."

> **Catatan:** kalimat spesifik pada tiap paragraf di atas harus disesuaikan kembali begitu Rumusan Masalah final (Opsi A/B, Sub Bab 1.2) dan hasil pengujian nyata sudah tersedia — draf ini adalah kerangka awal, bukan versi final.

---

## 3. BAB II — TINJAUAN PUSTAKA

Kalimat pembuka bab: satu paragraf yang menyatakan bahwa bab ini membahas penelitian terdahulu yang relevan serta dasar teori yang mendukung perancangan dan implementasi sistem.

### 2.1 Penelitian Terdahulu

**Struktur yang harus diikuti** (kombinasi gaya narasi funneling dari proposal eksperimental sebelumnya + tabel ringkasan seperti kedua contoh skripsi acuan):

1. Narasi naratif berkelompok (2–3 klaster tematik), misalnya:
   - **Klaster 1 — EEWS berbasis deep learning & arsitektur terdistribusi**: penelitian tentang deteksi gelombang-P, estimasi hiposenter/magnitudo berbasis ML pada arsitektur cloud/terdistribusi.
   - **Klaster 2 — Microservices, message broker, dan komunikasi real-time**: penelitian tentang Kafka, kontainerisasi, WebSocket vs REST/gRPC pada sistem microservices.
   - **Klaster 3 — Observabilitas sistem terdistribusi**: penelitian tentang Prometheus, Grafana, taksonomi observabilitas (metrik/log/trace), benchmarking sistem stream processing.
2. Setiap penelitian dirujuk dengan pola: **penulis (tahun) melakukan/mengembangkan X, menghasilkan Y, dengan keterbatasan/gap Z.**
3. **Tabel 2.1 — Ringkasan Penelitian Terkait**: kolom [Penulis (Tahun) | Topik | Metode/Teknologi | Hasil/Kontribusi].
4. **Tabel 2.2 — Posisi Penelitian** (tabel checklist ✓/✗ seperti pada proposal eksperimental sebelumnya): baris = penelitian terdahulu + "Penelitian Ini", kolom = fitur kunci (mis. Microservices, Kafka, Docker, WebSocket, Prometheus, Grafana, Evaluasi Latensi/Reproducibility). Kolom "Penelitian Ini" harus mencentang **WebSocket, Prometheus, dan Grafana secara bersamaan** — inilah celah yang belum diisi penelitian lain, dan menjadi penegasan posisi kontribusi.
5. Paragraf penutup subbab: sintesis eksplisit gap penelitian — *"belum ada penelitian yang secara bersamaan mengintegrasikan arsitektur microservices berbasis WebSocket dengan lapisan observabilitas Prometheus dan Grafana pada konteks EEWS."*

### 2.2 Dasar Teori

Struktur sub-sub-bab berikut wajib ada (urut dari konsep umum ke spesifik, sesuai pola kedua contoh skripsi):

#### 2.2.1 Earthquake Early Warning System (EEWS)
- Definisi EEWS, prinsip kerja (deteksi onset gelombang-P → estimasi parameter gempa → diseminasi peringatan).
- Tantangan utama: kecepatan vs akurasi, keandalan pada kondisi kritis.

#### 2.2.2 Arsitektur Microservices dan Kontainerisasi Docker
- Definisi microservices, perbandingan dengan arsitektur monolitik.
- Docker & Docker Compose sebagai platform kontainerisasi dan orkestrasi lokal.

#### 2.2.3 Apache Kafka sebagai Message Broker
- Konsep topic, partition, consumer group, broker.
- Peran Kafka dalam pipeline data streaming EEWS (asinkron, fault-tolerant).

#### 2.2.4 WebSocket sebagai Protokol Komunikasi Real-Time
- Definisi WebSocket, karakteristik full-duplex, perbedaan dengan HTTP polling/REST biasa.
- Alasan pemilihan WebSocket untuk diseminasi data EEWS (ringan, cukup untuk kebutuhan skala sistem, mudah diimplementasikan di sisi klien berbasis browser).
- **Catatan penting:** subbab ini TIDAK membandingkan dengan gRPC sebagai opsi yang sempat dipertimbangkan lalu ditinggalkan — WebSocket dibahas sebagai pilihan desain langsung, bukan hasil migrasi/reduksi dari opsi lain.

#### 2.2.5 Load Balancing dengan NGINX
- Definisi load balancing, algoritma umum (round-robin, least connection).
- Peran NGINX sebagai reverse proxy/load balancer pada endpoint HTTP dan/atau broker Kafka.

#### 2.2.6 Observabilitas Sistem Terdistribusi
- Definisi observabilitas (bukan sekadar monitoring): tiga pilar (metrik, log, trace).
- **Prometheus**: model scraping, time-series database, PromQL, jenis metrik (Counter, Gauge, Histogram).
- **Node Exporter**: metrik level host (CPU, memori, disk, jaringan).
- **Grafana**: platform visualisasi, integrasi datasource Prometheus, dashboard interaktif.
- Pustaka `prometheus_client` (Python) dan padanan untuk Node.js sebagai mekanisme instrumentasi aplikasi.

#### 2.2.7 Benchmarking Sistem Terdistribusi
- Definisi benchmarking, metrik umum (latensi, throughput, resource usage).
- Prinsip reproducibility dalam pengujian (jumlah trial, kontrol variabel, statistik deskriptif — mean, median, P95).
- Justifikasi metodologis kenapa P95 lebih relevan daripada rata-rata untuk sistem time-critical seperti EEWS.

---

## 4. BAB III — METODE PENELITIAN

Kalimat pembuka bab: satu paragraf yang menyatakan bab ini menjelaskan pendekatan penelitian, tahapan perancangan sistem, implementasi, hingga pengujian yang dilakukan.

### 3.1 Jenis dan Pendekatan Penelitian
- Jenis: **penelitian eksperimental (experimental research)** dengan pendekatan **kuantitatif**.
- Justifikasi: tujuan penelitian menentukan hubungan sebab-akibat antara variabel independen (desain arsitektur/instrumentasi observabilitas) dan variabel dependen (latensi, CPU, memori, data delay).
- Definisi variabel penelitian:
  - **Variabel bebas:** konfigurasi sistem yang diuji (mis. ada/tidaknya instrumentasi Prometheus; jumlah instance container; jenis WebSocket server).
  - **Variabel terikat:** latensi (ms), penggunaan CPU (%), penggunaan memori (MB), data delay end-to-end (s).
  - **Variabel kontrol:** spesifikasi mesin host, dataset seismik yang digunakan, model deep learning (bobot tetap), topologi jaringan Kafka.

### 3.2 Studi Literatur dan Analisis Kebutuhan
- Sumber literatur: basis data jurnal terindeks (Scopus/IEEE/ScienceDirect/dsb.), rentang tahun tertentu.
- Kebutuhan fungsional: daftar modul dan alur data (mengacu Bagian 3 dokumen rancangan aplikasi sebelumnya).
- Kebutuhan non-fungsional: target latensi jalur kritis, granularitas metrik, interval scraping.
- Identifikasi titik kritis pipeline yang menjadi fokus instrumentasi (mis. jalur Load Balancer → P-Wave Detector).

### 3.3 Perancangan Arsitektur Sistem
- Deskripsi komponen sistem dalam bentuk **tabel arsitektur** (nama modul, teknologi, protokol komunikasi, topik Kafka terkait, deskripsi fungsi) — turunkan dari tabel modul pada dokumen rancangan aplikasi sebelumnya.
- **Gambar arsitektur sistem** (diagram blok/komponen): tunjukkan seluruh modul, arah aliran data, dan **titik-titik instrumentasi Prometheus (`/metrics`)** di setiap modul sebagai elemen visual utama.
- **Sequence diagram alur data seismik**: dari ingesti data hingga diseminasi ke klien, termasuk titik scraping metrik oleh Prometheus.
- Perancangan skema topik Kafka (`trace_topic`, `p_wave_topic`, `loc_mag_topic`, `result_topic`).

### 3.4 Implementasi Sistem

Sub-sub-bab berikut wajib ada:

#### 3.4.1 Implementasi Pipeline Inti EEWS
- Implementasi Data Provider (ingesti via SeedLink/ObsPy, strategi paralelisasi jika relevan).
- Implementasi P-Wave Detector (mode consumer langsung dan mode load-balanced via HTTP).
- Implementasi Load Balancer (Kafka consumer → HTTP forwarder, strategi distribusi/round-robin).
- Implementasi Location & Magnitude Detector.
- Implementasi Data Archiver (penyimpanan ke basis data).
- Implementasi WebSocket Server (varian dan alasan penyediaan lebih dari satu implementasi jika ada, mis. Express.js/Socket.IO vs FastAPI native WebSocket).

#### 3.4.2 Implementasi Instrumentasi Prometheus
- Penambahan pustaka `prometheus_client` (dan padanan Node.js) pada tiap modul.
- Definisi jenis metrik per modul (Counter/Gauge/Histogram) — turunkan dari tabel rencana metrik pada dokumen rancangan aplikasi sebelumnya.
- Konfigurasi endpoint `/metrics` per modul pada port unik.
- Konfigurasi `prometheus.yml` (scrape target, interval scraping).

#### 3.4.3 Implementasi Dashboard Grafana
- Penambahan datasource Prometheus (terpisah dari datasource lain jika ada).
- Perancangan panel dashboard: latensi per modul, penggunaan CPU/memori, data delay end-to-end, jumlah klien WebSocket aktif, dsb.
- Penjelasan pemilihan jenis visualisasi (time-series graph, gauge, heatmap) per jenis metrik.

#### 3.4.4 Konfigurasi Docker Compose
- Definisi service, jaringan, dan volume untuk seluruh komponen (termasuk Prometheus, Node Exporter, Grafana) dalam satu/lebih file orkestrasi.
- Konfigurasi health check antar-service agar scraping hanya berjalan setelah target siap.

### 3.5 Perancangan Skenario Pengujian

Tabel skenario pengujian (kode, deskripsi, variasi parameter, variabel yang diukur), turunkan dan sesuaikan dari dokumen rancangan aplikasi sebelumnya, misalnya:

| Kode | Skenario | Variasi Parameter | Variabel Diukur |
|---|---|---|---|
| S1 | Overhead Instrumentasi Prometheus | Sistem dengan vs tanpa `prometheus_client` aktif | Selisih CPU (%), memori (MB), latensi (ms) |
| S2 | Skalabilitas Multi-Container | Variasi jumlah instance P-Wave Detector/Data Archiver | Data delay end-to-end (s), throughput, CPU/memori agregat |
| S3 | Perbandingan Implementasi WebSocket Server | Varian A vs varian B pada beban klien bertingkat | Data delay (s), CPU (%), memori (MB), jumlah klien aktif |
| S4 | Observabilitas Kafka + NGINX Load Balancer | Konfigurasi load balancing berbeda | Data delay (s), CPU (%), memori (MB) |

- Jumlah trial per skenario dan alasan (stabilitas statistik).
- Prosedur restart sistem antar-skenario untuk menjaga kondisi awal konsisten.

### 3.6 Pengumpulan dan Analisis Data
- Mekanisme pengumpulan data: Prometheus API (PromQL) untuk metrik time-series, opsional Docker Stats API sebagai pembanding.
- Format penyimpanan data pengujian (mis. CSV) untuk analisis lanjutan.
- Metode analisis: statistik deskriptif (mean, median, standar deviasi, P95), visualisasi time-series via Grafana, box plot untuk perbandingan distribusi antar-kondisi.

---

## 5. BAB IV — IMPLEMENTASI DAN PENGUJIAN

Kalimat pembuka bab: satu paragraf yang menyatakan bab ini memaparkan hasil implementasi sistem sesuai rancangan Bab III, beserta hasil pengujian dan pembahasannya.

> Catatan struktur: Bab ini menggabungkan pola "Tahap Implementation" (dari contoh skripsi ICONIX) dan pola "Hasil Pengujian Sistem" (dari contoh skripsi Scrum), disesuaikan untuk konteks eksperimental — implementasi dipaparkan per modul dengan potongan kode kunci, lalu pengujian dipaparkan per skenario dengan data dan grafik hasil nyata.

### 4.1 Lingkungan Implementasi
- Spesifikasi perangkat keras dan perangkat lunak yang digunakan (tabel), **tanpa mencantumkan nomor versi spesifik** kecuali sudah difinalisasi.
- Struktur direktori proyek (opsional, sebagai tabel/gambar).

### 4.2 Implementasi Arsitektur Sistem
- Realisasi arsitektur (diagram akhir yang benar-benar diimplementasikan, dibandingkan dengan rancangan Bab III bila ada perbedaan).
- Pemetaan modul ke komponen Docker (tabel: nama service, image/base, port, dependency).

### 4.3 Implementasi Source Code Kunci

Untuk tiap modul penting, sajikan **potongan kode representatif** (bukan seluruh kode) dengan format Source Code sesuai aturan template (tabel 2 baris 1 kolom, font Courier New 10pt, tanpa caption/nomor daftar), disertai narasi penjelasan sebelum/sesudahnya:

- Source Code — inisialisasi metrik Prometheus (`Counter`, `Gauge`, `Histogram`) pada salah satu modul.
- Source Code — endpoint `/metrics` (`start_http_server` atau middleware Express/FastAPI setara).
- Source Code — logika inti modul kritis (mis. handler `POST /trace` pada P-Wave Detector, atau logika distribusi pada Load Balancer).
- Source Code — konfigurasi `prometheus.yml` (scrape target).
- Source Code — potongan `docker-compose.yml` untuk service Prometheus/Grafana/Node Exporter.

### 4.4 Implementasi Dashboard Grafana
- Tangkapan layar/deskripsi panel dashboard yang berhasil dibangun (per kategori: latensi, resource usage, data delay, klien aktif).
- Penjelasan bagaimana tiap panel memetakan ke metrik/PromQL tertentu.

### 4.5 Lingkungan Pengujian
- Spesifikasi mesin pengujian, kondisi jaringan, dataset seismik yang dipakai untuk pengujian.
- Prosedur eksekusi pengujian (skrip otomatis, jumlah trial, cara reset sistem).

### 4.6 Hasil Pengujian per Skenario

Untuk **setiap skenario (S1–S4)**, gunakan struktur pemaparan yang konsisten:

1. **Tujuan skenario** (1 kalimat, mengulang dari Bab III).
2. **Prosedur pelaksanaan** (ringkas, merujuk Bab III).
3. **Tabel/grafik hasil** `[DATA HASIL PENGUJIAN]` — wajib berupa angka nyata hasil eksperimen, bukan estimasi.
4. **Pembahasan hasil** — interpretasi kenapa hasil seperti itu terjadi, dikaitkan dengan teori Bab II (mis. jika CPU naik signifikan saat instrumentasi aktif, kaitkan dengan konsep overhead observabilitas dari Faseeha dkk. atau sejenis).

Sub-sub-bab yang disarankan:
- 4.6.1 Hasil Pengujian S1 — Overhead Instrumentasi Prometheus
- 4.6.2 Hasil Pengujian S2 — Skalabilitas Multi-Container
- 4.6.3 Hasil Pengujian S3 — Perbandingan Implementasi WebSocket Server
- 4.6.4 Hasil Pengujian S4 — Observabilitas Kafka + NGINX Load Balancer

### 4.7 Analisis dan Pembahasan Keseluruhan
- Sintesis lintas-skenario: pola umum apa yang muncul (mis. trade-off overhead vs visibilitas performa).
- Kaitan hasil dengan rumusan masalah dan tujuan penelitian di Bab I (jawab eksplisit tiap poin rumusan masalah dengan temuan hasil pengujian).
- Keterbatasan yang ditemukan selama implementasi/pengujian (jika ada), disampaikan secara jujur dan proporsional.

---

## 6. BAB V — PENUTUP

Kalimat pembuka bab: satu paragraf yang menyatakan bab ini memuat kesimpulan dari keseluruhan penelitian serta saran untuk pengembangan lebih lanjut.

### 5.1 Kesimpulan
- Ditulis sebagai poin bernomor, **selaras 1-ke-1 dengan tujuan penelitian di Bab I** (bukan ringkasan bebas) — setiap tujuan dijawab dengan satu simpulan yang didukung `[DATA HASIL PENGUJIAN]`.
- Contoh pola kalimat: *"Arsitektur microservices EEWS berbasis Kafka dan WebSocket berhasil dirancang dan diimplementasikan, terdiri atas enam modul utama yang saling berkomunikasi secara asinkron melalui tiga topik Kafka."*
- Tutup dengan simpulan tentang overhead observabilitas (jawaban rumusan masalah ke-4) sebagai temuan kunci penelitian.

### 5.2 Saran
- Ditulis sebagai poin bernomor, mencakup:
  - Saran teknis pengembangan lanjutan (mis. alerting otomatis berbasis Prometheus Alertmanager, tracing terdistribusi/OpenTelemetry sebagai pelengkap metrik).
  - Saran metodologis untuk penelitian lanjutan (mis. pengujian pada skala data/klaster yang lebih besar, pengujian pada infrastruktur cloud produksi).
  - Saran praktis bagi pengembang sistem EWS lain yang ingin mengadopsi pendekatan observabilitas serupa.

---

## 7. DAFTAR PUSTAKA & LAMPIRAN (Pedoman Singkat)

- **Daftar Pustaka:** disusun alfabetis berdasarkan nama belakang penulis, mengikuti format pada template resmi (gaya APA seperti kedua contoh skripsi acuan). Prioritaskan sumber jurnal/prosiding terindeks Scopus/IEEE dalam rentang tahun terbaru, ditambah dokumentasi resmi teknologi (Kafka, Prometheus, Grafana, Docker) bila diperlukan untuk penjelasan teknis.
- **Lampiran (usulan isi):**
  - Lampiran 1 — Konfigurasi lengkap `prometheus.yml` dan `docker-compose.yml`.
  - Lampiran 2 — Tabel mentah hasil pengujian tiap skenario (sebelum diringkas jadi statistik deskriptif di Bab IV).
  - Lampiran 3 — Contoh query PromQL yang digunakan pada tiap panel dashboard Grafana.
  - Lampiran 4 — Dokumentasi tangkapan layar dashboard Grafana secara lengkap.

---

## 8. Daftar Placeholder yang Wajib Diisi dengan Data Nyata (Bukan Dikarang)

Agar AI penulis lain tidak "mengarang" angka, seluruh bagian berikut **wajib ditandai eksplisit** sebagai placeholder dalam draf sampai data eksperimen tersedia:

- `[DATA HASIL PENGUJIAN]` — seluruh angka pada Bab IV Sub-bab 4.6 (tabel/grafik hasil S1–S4).
- `[SPESIFIKASI PERANGKAT]` — spesifikasi mesin implementasi & pengujian pada Sub-bab 4.1 dan 4.5.
- `[JUDUL FINAL]`, `[NAMA PEMBIMBING]`, `[TANGGAL SIDANG]` — metadata halaman judul/pengesahan sesuai template resmi.
- `[VERSI PUSTAKA/ENVIRONMENT]` — hanya diisi setelah versi final ditentukan, sesuai catatan pada Bagian 0 poin 7.

---

## 9. Ringkasan Peta Bab (untuk Sistematika Penulisan Bab I.5)

| Bab | Isi Ringkas |
|---|---|
| I — Pendahuluan | Urgensi observabilitas pada EEWS microservices, rumusan masalah, tujuan/manfaat, ruang lingkup |
| II — Tinjauan Pustaka | Penelitian terdahulu (EEWS, microservices/Kafka/WebSocket, observabilitas) + dasar teori pendukung |
| III — Metode Penelitian | Jenis penelitian eksperimental-kuantitatif, tahap perancangan arsitektur, implementasi, instrumentasi Prometheus, dashboard Grafana, skenario pengujian, metode analisis data |
| IV — Implementasi dan Pengujian | Realisasi sistem (kode, konfigurasi, dashboard) + hasil pengujian tiap skenario + pembahasan |
| V — Penutup | Kesimpulan selaras tujuan penelitian + saran pengembangan lanjutan |
