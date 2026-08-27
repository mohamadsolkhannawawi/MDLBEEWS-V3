# Kumpulan Prompt Penulisan Skripsi — EEWS Microservices dengan Observabilitas Prometheus & Grafana

> **Versi:** Revisi-1 — disesuaikan dengan `rancangan-isi-skripsi-eews-observabilitas.md` versi Revisi-1 (BAB II sudah 10 subbab dasar teori, BAB III diperluas dengan Gambar 3.1 alur metodologi, notasi C4 *Model*/DFD, Tabel Definisi Variabel, dan skenario pengujian berprofil beban kerja).
>
> **Fungsi dokumen:** Kumpulan prompt siap pakai untuk men-generate isi skripsi (Bab I–V) menggunakan AI, disusun dari empat dokumen acuan:
> 1. `konteks-aplikasi-eews-observabilitas.md` — kebenaran teknis sistem (arsitektur, modul, status implementasi).
> 2. `rancangan-isi-skripsi-eews-observabilitas.md` (Revisi-1) — blueprint isi tiap bab/subbab.
> 3. `rancangan-daftar-pustaka-eews-observabilitas.md` — pemetaan pustaka yang boleh dipakai per subbab.
> 4. **Bab yang sudah final** (`BAB_I_Pendahuluan.md`, `BAB_II_Tinjauan_Pustaka.md`, dst. — bertambah seiring progres) — **[BARU]** dokumen bab yang sudah selesai ditulis dan disepakati, berfungsi sebagai sumber kebenaran yang **lebih tinggi prioritasnya** daripada blueprint bila keduanya berbeda, karena blueprint adalah rencana sedangkan bab final adalah realisasi yang sudah dirujuk balik oleh bab-bab sesudahnya (mis. BAB III wajib konsisten dengan notasi dan sitasi yang sudah dipakai BAB II).
>
> **Prinsip utama yang WAJIB ditegaskan di setiap prompt:** topik penelitian **sudah berpindah** dari proposal lama berbasis **gRPC** menjadi rancangan baru berbasis **HTTP biasa + WebSocket + Kafka**, dengan kontribusi utama **observabilitas Prometheus & Grafana**. Proposal lama (`TubesMPPI_Genap22526_...pdf`) **hanya boleh dipakai sebagai referensi gaya/format penulisan** (cara menyusun paragraf, tabel, sitasi APA), **bukan** sebagai sumber kebenaran teknis — setiap detail arsitektur, protokol, dan pustaka di proposal lama yang bertentangan dengan dokumen acuan di atas harus diabaikan.

---

## 0. Cara Menggunakan Dokumen Ini

1. Setiap sesi generate isi skripsi (per bab atau per subbab), **selalu mulai dengan PROMPT MASTER** di Bagian 1 sebagai pesan pertama (atau digabung di awal prompt subbab), lalu lampirkan **seluruh file** sesuai **Tabel Lampiran per Sesi** di bawah — bukan hanya tiga file acuan lama, karena BAB III ke atas sekarang bergantung pada bab-bab final sebelumnya.
2. Gunakan **PROMPT ABSTRAK** hanya setelah seluruh Bab I–V memiliki draf, karena Abstrak adalah ringkasan dari keseluruhan isi (khususnya kesimpulan Bab V).
3. **PROMPT PER BAB** dipakai jika ingin men-generate satu bab penuh sekaligus (cocok untuk draf kasar/awal). Untuk BAB I dan BAB II yang **sudah final**, prompt "per bab lengkap" pada dokumen ini bersifat historis/arsip — pakai **PROMPT PER SUB BAB** saja bila sewaktu-waktu perlu merevisi sebagian kecil dari bab yang sudah final, agar bagian yang sudah disepakati tidak ikut ditulis ulang tanpa perlu.
4. **PROMPT PER SUB BAB** dipakai untuk revisi/pendalaman granular per subbab (cocok untuk penulisan final yang presisi).
5. Setiap prompt sudah menyertakan placeholder `[DATA HASIL PENGUJIAN]`, `[SPESIFIKASI PERANGKAT]`, `[JUDUL FINAL]`, `[VERSI PUSTAKA/ENVIRONMENT]` — **jangan minta AI mengarang nilai ini**; AI harus mempertahankan placeholder tersebut apa adanya sampai data nyata tersedia.
6. Jika keluaran AI menyebut gRPC, Protocol Buffers, atau `.proto` di manapun (kecuali di kalimat yang secara eksplisit menjelaskan riwayat perubahan topik), **tolak keluaran tersebut** dan minta revisi — ini adalah tanda AI salah mengacu ke proposal lama.

### Tabel Lampiran per Sesi — **[BARU, wajib dicek sebelum mengirim prompt]**

Lampirkan **seluruh file** pada baris yang sesuai dengan bab/subbab yang sedang digarap. File di kolom "Wajib selalu" dilampirkan di setiap sesi apa pun; file di kolom "Tambahan wajib" hanya berlaku untuk sesi bab tersebut.

| Sesi yang dikerjakan | Wajib selalu | Tambahan wajib untuk sesi ini |
|---|---|---|
| ABSTRAK & ABSTRACT | `konteks-aplikasi-eews-observabilitas.md`, `rancangan-isi-skripsi-eews-observabilitas.md`, `rancangan-daftar-pustaka-eews-observabilitas.md` | `BAB_I_Pendahuluan.md`, `BAB_V_Penutup.md` (khususnya Sub Bab 5.1 yang sudah diisi data nyata) |
| BAB I — Pendahuluan (revisi granular; bab ini sudah final) | idem | — (bab sudah final; lampirkan `BAB_I_Pendahuluan.md` itu sendiri sebagai basis revisi) |
| BAB II — Tinjauan Pustaka (revisi granular; bab ini sudah final) | idem | `BAB_I_Pendahuluan.md` (untuk cek konsistensi verbatim paragraf pembuka & istilah), `BAB_II_Tinjauan_Pustaka.md` itu sendiri sebagai basis revisi |
| **BAB III — Metode Penelitian** | idem | `BAB_I_Pendahuluan.md` **dan** `BAB_II_Tinjauan_Pustaka.md` — **wajib**, karena BAB III harus merujuk balik ke notasi (C4 *Model*, DFD) dan teori (Sugiyono 2022, Raptis dkk. 2024, Tzanettis dkk. 2022, Martín dkk. 2022) yang sudah ditulis di BAB II Sub Bab 2.2.8–2.2.10, bukan mendefinisikan ulang dari nol |
| BAB IV — Implementasi dan Pengujian | idem | `BAB_III_Metode_Penelitian.md` (draf final Bab III yang sedang/sudah ditulis) |
| BAB V — Penutup | idem | `BAB_I_Pendahuluan.md` (untuk pencocokan 1-ke-1 dengan Tujuan Penelitian) dan `BAB_IV_Implementasi_dan_Pengujian.md` Sub Bab 4.6–4.7 yang sudah diisi data nyata |
| Daftar Pustaka & Lampiran | idem | Seluruh draf Bab I–V yang sudah ditulis sejauh sesi ini berjalan |

> **Catatan:** nama file bab final di atas (`BAB_III_Metode_Penelitian.md`, `BAB_IV_Implementasi_dan_Pengujian.md`, dst.) mengikuti pola penamaan yang sudah dipakai untuk `BAB_I_Pendahuluan.md` dan `BAB_II_Tinjauan_Pustaka.md` — sesuaikan bila nama file aktual berbeda.

---

## 1. PROMPT MASTER (wajib disertakan di setiap sesi)

```
Kamu berperan sebagai penulis akademik profesional bidang Rekayasa Perangkat Lunak,
membantu menyusun skripsi S1 Informatika (FSM Undip) dengan topik:

"Perancangan dan Implementasi Observabilitas Berbasis Prometheus dan Grafana pada
Arsitektur Microservices Earthquake Early Warning System" [JUDUL FINAL — sesuaikan bila
pembimbing menetapkan judul berbeda].

FILE YANG DILAMPIRKAN PADA SESI INI (sebutkan ulang secara eksplisit di awal jawabanmu,
satu per satu, agar dapat diverifikasi bahwa tidak ada yang terlewat sebelum menulis):
1. konteks-aplikasi-eews-observabilitas.md — kebenaran teknis sistem: modul, arsitektur,
   status implementasi (sudah/belum), dan aturan penulisan teknis.
2. rancangan-isi-skripsi-eews-observabilitas.md (Revisi-1) — blueprint isi tiap
   bab/subbab, termasuk kalimat kunci wajib, struktur paragraf, dan tabel/gambar yang
   harus ada.
3. rancangan-daftar-pustaka-eews-observabilitas.md — daftar pustaka yang SAH dipakai per
   subbab, lengkap dengan pemetaan dan pustaka yang harus DIKELUARKAN.
4. [FILE BAB FINAL TAMBAHAN sesuai Tabel Lampiran per Sesi Bagian 0 dokumen prompt —
   SEBUTKAN nama file yang benar-benar dilampirkan di sesi ini, mis. BAB_I_Pendahuluan.md
   dan/atau BAB_II_Tinjauan_Pustaka.md. Jika sesi ini mengerjakan BAB III atau sesudahnya
   dan salah satu file bab final yang disyaratkan TIDAK dilampirkan, HENTIKAN dan minta
   file tersebut terlebih dahulu sebelum menulis apa pun — JANGAN menulis berdasarkan
   asumsi isi bab final yang belum benar-benar dilampirkan.]

ATURAN PRIORITAS SUMBER BILA TERJADI KONFLIK ANTAR-FILE — [BARU]:
- Bila isi file bab final (mis. BAB_II_Tinjauan_Pustaka.md) berbeda dengan
  rancangan-isi-skripsi-eews-observabilitas.md, IKUTI isi bab final — blueprint adalah
  rencana, bab final adalah realisasi yang sudah disepakati.
- Bila hal ini terjadi, laporkan secara singkat perbedaannya di awal jawaban (1–2
  kalimat) sebelum melanjutkan menulis, agar pengguna sadar ada penyesuaian.

ATURAN TEKNIS YANG TIDAK BOLEH DILANGGAR:
- Sistem TIDAK menggunakan gRPC, Protocol Buffers, atau RPC biner dalam bentuk apa pun.
  Komunikasi antar-layanan kritis memakai HTTP biasa; diseminasi ke klien memakai
  WebSocket standar. Ini adalah keputusan desain, BUKAN hasil migrasi dari gRPC yang
  "ditinggalkan" — jangan menulis narasi seolah-olah gRPC pernah dipertimbangkan lalu
  digantikan.
- Ada satu berkas proposal lama (TubesMPPI_..._Mohamad.pdf) yang membahas gRPC. Berkas
  itu HANYA boleh dipakai sebagai contoh gaya penulisan/format (struktur paragraf, cara
  membuat tabel State of the Art, gaya sitasi APA) — SELURUH substansi teknis di
  dalamnya (gRPC, Protocol Buffers, Niswar dkk. sebagai justifikasi gRPC, dst.) tidak
  boleh dipindahkan ke draf baru.
- Modul sistem yang sah disebut (nama baku, huruf kapital di awal kata, konsisten):
  Data Provider, P-Wave Detector, Load Balancer, Location & Magnitude Detector,
  Data Archiver, WebSocket Server, Prometheus Server, Node Exporter, Grafana Dashboard.
- Topik Kafka yang sah: trace_topic, p_wave_topic, loc_mag_topic, result_topic
  (result_loc_mag_topic sebagai alternatif nama, sesuai konteks aplikasi).
- Pustaka yang boleh dikutip HANYA yang ada di rancangan-daftar-pustaka-eews-observabilitas.md
  Bagian 1 (dipertahankan) dan Bagian 4/4A (pustaka baru WebSocket & NGINX). JANGAN
  mengutip pustaka dari Bagian 2 (dikeluarkan) atau Bagian 3 (marginal/ditolak), dan
  JANGAN mengarang pustaka baru yang tidak ada di dokumen acuan. Pengecualian: bila
  salah satu file bab final yang dilampirkan (mis. BAB_II_Tinjauan_Pustaka.md) sudah
  mengutip pustaka tambahan yang terbukti relevan (mis. Sugiyono 2022, Kitchenham &
  Charters 2007, Newman 2021, Sommerville 2016, Brown 2022, Kendall & Kendall 2011),
  pustaka tersebut TETAP SAH dipakai secara konsisten di bab-bab berikutnya walau belum
  eksplisit tercantum di rancangan-daftar-pustaka — verifikasi dulu bahwa pustaka itu
  memang benar-benar muncul di file bab final yang dilampirkan, jangan menduga-duga.
- JANGAN mencantumkan nomor versi pustaka/environment spesifik (Python, Kafka, Docker,
  dsb.) — cukup nama teknologi, atau tandai [VERSI PUSTAKA/ENVIRONMENT] bila memang perlu.
- JANGAN merujuk proyek/paper eksternal sebagai dasar arsitektur — seluruh sistem
  diposisikan sebagai rancangan dan implementasi orisinal untuk penelitian ini.
- Placeholder [DATA HASIL PENGUJIAN], [SPESIFIKASI PERANGKAT], [JUDUL FINAL],
  [NAMA PEMBIMBING], [TANGGAL SIDANG], [VERSI PUSTAKA/ENVIRONMENT] TIDAK BOLEH diisi
  dengan angka/nama karangan — biarkan sebagai placeholder eksplisit dalam draf.

ATURAN GAYA PENULISAN (berlaku di seluruh bab, lihat Bagian 0 rancangan-isi-skripsi):
- Satu paragraf = satu gagasan utama; kalimat pertama adalah kalimat utama yang kuat dan
  berdiri sendiri; kalimat berikutnya hanya menjelaskan/mendukung, bukan menambah gagasan
  baru.
- Idealnya 3–5 kalimat per paragraf. Jika sebuah gagasan butuh lebih, pecah jadi dua
  paragraf, jangan memanjangkan satu paragraf.
- Setiap tabel/gambar/source code disitasi dalam teks sebelum atau sesudah kemunculannya
  (contoh: "...ditunjukkan pada Tabel 3.1").
- Penomoran sub-bab maksimal 4 level.
- Bahasa formal ilmiah, tanpa kata ganti orang pertama tunggal ("saya") — gunakan bentuk
  pasif atau "penulis"/"peneliti".
- Sitasi mengikuti gaya APA: (Nama dkk., Tahun); Daftar Pustaka disusun alfabetis.
- Paragraf pembuka tiap bab harus identik verbatim dengan paragraf deskripsi bab tersebut
  di Sub Bab 1.5 Sistematika Penulisan — tulis satu kali, salin-tempel ke dua tempat.

TUGAS SPESIFIK UNTUK SESI INI: [diisi sesuai prompt bab/subbab yang dipilih di bawah]

Sebelum menulis, (1) sebutkan ulang daftar file yang berhasil kamu baca pada sesi ini
sesuai poin "FILE YANG DILAMPIRKAN" di atas, (2) jika ada file wajib yang disyaratkan
Tabel Lampiran per Sesi tetapi tidak kamu temukan terlampir, hentikan dan minta file itu
lebih dulu, (3) baru lanjutkan menulis draf sesuai tugas spesifik di atas.
```

---

## 2. PROMPT ABSTRAK & ABSTRACT

```
[Sertakan PROMPT MASTER di atas sebagai konteks, lalu lanjutkan dengan tugas berikut.]

TUGAS: Tulis ABSTRAK (Bahasa Indonesia) dan ABSTRACT (terjemahan maknawi ke Bahasa
Inggris, bukan kata-per-kata) untuk skripsi ini.

ATURAN FORMAT (dari template resmi):
- Satu paragraf, tanpa indentasi baris pertama, maksimal 300 kata.
- Wajib memuat 4 unsur berurutan dalam satu paragraf mengalir (jangan diberi subjudul):
  1. WHY (urgensi): gempa bumi sebagai bencana yang butuh peringatan dini cepat; sistem
     EEWS berbasis microservices umumnya sulit dipantau performanya secara real-time dan
     reproducible karena tidak memiliki lapisan observabilitas terstruktur.
  2. WHAT (apa yang dihasilkan): sistem EEWS berbasis microservices (Data Provider,
     P-Wave Detector, Load Balancer, Location & Magnitude Detector, Data Archiver,
     WebSocket Server) yang diorkestrasi dengan Kafka dan Docker, dilengkapi lapisan
     observabilitas Prometheus + Grafana.
  3. HOW (proses implementasi): instrumentasi metrik (Counter, Gauge, Histogram) pada
     setiap modul via prometheus_client (dan padanan Node.js), scraping periodik oleh
     Prometheus Server, visualisasi via dashboard Grafana, diuji melalui beberapa
     skenario (S1 overhead instrumentasi, S2 skalabilitas multi-container, S3
     perbandingan WebSocket server, S4 observabilitas Kafka + NGINX load balancer).
  4. CONCLUSION: ringkasan hasil — GUNAKAN placeholder [DATA HASIL PENGUJIAN] untuk
     angka/simpulan kuantitatif, JANGAN mengarang angka.
- Kata kunci (5–7 kata/frasa): Earthquake Early Warning System, microservices, Apache
  Kafka, WebSocket, Prometheus, Grafana, observabilitas.
- TIDAK BOLEH menyebut gRPC, Protocol Buffers, atau perbandingan protokol biner vs REST
  di manapun dalam abstrak.

KELUARAN: dua blok teks terpisah — "ABSTRAK" (Bahasa Indonesia) dan "ABSTRACT" (Bahasa
Inggris), masing-masing diikuti baris "Kata kunci :" / "Keywords :".
```

---

## 3. PROMPT BAB I — PENDAHULUAN

> **[STATUS: BAB INI SUDAH FINAL — `BAB_I_Pendahuluan.md`]** Sub Bab 3.1 di bawah adalah arsip prompt "generate lengkap" yang dipakai saat BAB I pertama kali disusun. Gunakan **Sub Bab 3.2 (Prompt Per Sub Bab I)** untuk revisi/pendalaman granular; jangan menulis ulang bab ini dari nol tanpa alasan kuat, karena bab-bab sesudahnya (II, III, ...) sudah dirujuk balik ke rumusan masalah dan tujuan penelitian final di bab ini.

### 3.1 Prompt Bab I (versi lengkap sekaligus) — ARSIP, JANGAN DIPAKAI ULANG

```
[Sertakan PROMPT MASTER, lalu lanjutkan.]

TUGAS: Tulis BAB I PENDAHULUAN secara lengkap, terdiri atas: paragraf pembuka bab,
1.1 Latar Belakang, 1.2 Rumusan Masalah, 1.3 Tujuan dan Manfaat (1.3.1 Tujuan Penelitian,
1.3.2 Manfaat Penelitian), 1.4 Ruang Lingkup, dan 1.5 Sistematika Penulisan.

PARAGRAF PEMBUKA BAB: satu paragraf yang menyebut isi bab (latar belakang, rumusan
masalah, tujuan dan manfaat, ruang lingkup, sistematika penulisan) DAN inti permasalahan
spesifik topik ini (ketiadaan mekanisme pemantauan operasional terstruktur pada EEWS
microservices, serta usulan integrasi Prometheus & Grafana). Paragraf ini harus SAMA
PERSIS (verbatim) dengan paragraf BAB I di Sub Bab 1.5 — tulis sekali, salin ke dua
tempat.

1.1 LATAR BELAKANG — ikuti pola inverted funnel LIMA paragraf (satu paragraf per lapis,
3–5 kalimat, JANGAN ditulis sebagai poin bebas):
  1. Status Quo: EEWS berbasis microservices sudah lazim — tiap tahap pemrosesan
     (ingesti, deteksi gelombang-P, estimasi lokasi/magnitudo, diseminasi) dipisah
     menjadi layanan independen terkontainerisasi, berkomunikasi via Kafka dan
     WebSocket.
  2. What's wrong: sistem semacam ini umumnya tidak dilengkapi mekanisme pemantauan
     operasional terstruktur — performa layanan biasanya diamati manual dan sesaat.
  3. Why this is a problem: ketiadaan observabilitas membuat evaluasi performa sulit
     direproduksi ilmiah, sulit mendeteksi bottleneck dini, berisiko pada sistem
     time-critical seperti EEWS.
  4. How you intend to fix it: penelitian ini merancang lapisan observabilitas berbasis
     Prometheus (pengumpulan metrik terstruktur) dan Grafana (visualisasi dashboard
     real-time) di atas arsitektur EEWS berbasis Kafka dan WebSocket.
  5. Objective: paragraf penutup bernada HARAPAN (bukan klaim capaian/kesimpulan) —
     harapan agar sistem EEWS yang dibangun dapat diamati dan dievaluasi performanya
     secara transparan sebagai acuan pengembangan sistem serupa.
  Kalimat kunci wajib muncul: "mekanisme pemantauan operasional yang terstruktur",
  "evaluasi performa secara ilmiah dan reproducible", "Prometheus dan Grafana sebagai
  lapisan observabilitas".
  Sitasi paragraf 1–4 memakai pustaka dari rancangan-daftar-pustaka-eews-observabilitas.md
  Bagian 1 (klaster EEWS, microservices, observabilitas) — TIDAK memakai pustaka Bagian 2.

1.2 RUMUSAN MASALAH — gunakan Opsi A (fokus tunggal, SATU paragraf berisi SATU kalimat
tanya, TIDAK dipecah poin):
  "Bagaimana merancang dan mengimplementasikan lapisan observabilitas berbasis
  Prometheus dan Grafana pada arsitektur microservices Earthquake Early Warning System
  yang menggunakan Kafka dan WebSocket, sehingga performa sistem — mencakup latensi,
  penggunaan sumber daya, dan data delay end-to-end — dapat dipantau secara real-time
  dan dianalisis secara reproducible?"
  (Sesuaikan redaksi seperlunya, tetap satu paragraf satu kalimat tanya utama.)

1.3.1 TUJUAN PENELITIAN — selaras 1-ke-1 dengan Rumusan Masalah Opsi A, ditulis sebagai
HASIL/OUTCOME (gunakan "dihasilkannya/diperolehnya/tersedianya", BUKAN kata kerja proses
seperti "merancang/mengimplementasikan" sebagai kata kerja utama pembuka kalimat):
  "Penelitian ini bertujuan untuk menghasilkan arsitektur microservices Earthquake Early
  Warning System berbasis Kafka dan WebSocket yang dilengkapi lapisan observabilitas
  Prometheus dan Grafana, sehingga performa sistem dapat dipantau secara real-time dan
  dianalisis secara reproducible."

1.3.2 MANFAAT PENELITIAN — pisahkan manfaat Teoritis (kontribusi kerangka evaluasi
performa berbasis observabilitas untuk EEWS, rujukan metodologis penelitian lanjutan) dan
Praktis (prototipe EEWS dengan dashboard monitoring siap pakai bagi komunitas riset
kebencanaan; bukti empiris overhead vs manfaat observabilitas pada sistem time-critical).

1.4 RUANG LINGKUP — poin bernomor, WAJIB mencakup ketujuh batasan berikut (boleh
diparafrasakan, jangan dihilangkan satupun):
  1. Arsitektur microservices, dikontainerisasi Docker/Docker Compose, lingkungan lokal.
  2. Modul: Data Provider, P-Wave Detector, Load Balancer, Location & Magnitude
     Detector, Data Archiver, WebSocket Server, Prometheus Server, Node Exporter,
     Grafana Dashboard.
  3. Komunikasi antar-layanan kritis via HTTP biasa; diseminasi ke klien via WebSocket.
     TIDAK menggunakan gRPC/Protocol Buffers/RPC biner lain.
  4. Data seismik simulasi/historis via SeedLink/ObsPy, bukan sensor fisik langsung.
  5. Evaluasi performa: latensi komunikasi (ms), penggunaan CPU (%), penggunaan memori
     (MB), data delay end-to-end (s) — seluruhnya via Prometheus.
  6. Model deep learning P-wave & lokasi-magnitudo memakai model yang sudah
     tersedia/terlatih, bukan fokus pengembangan model baru.
  7. Tidak mencakup deployment cloud produksi maupun pengujian pada sensor seismik fisik
     sesungguhnya.

1.5 SISTEMATIKA PENULISAN — lima paragraf (satu per bab), masing-masing terdiri dari
kalimat generik (isi bab) + kalimat spesifik (fokus topik ini). Paragraf BAB I di sini
harus identik verbatim dengan paragraf pembuka bab di atas. Gunakan draf lima paragraf
sesuai rancangan-isi-skripsi-eews-observabilitas.md Sub Bab 1.5 sebagai basis, sesuaikan
redaksi bila perlu tanpa mengubah maknanya.

KELUARAN: teks lengkap Bab I dengan penomoran subbab sesuai di atas, sitasi APA inline,
placeholder tetap dipertahankan bila relevan.
```

### 3.2 Prompt Per Sub Bab I (granular) — DIPERBARUI, gunakan ini untuk revisi

```
[Sertakan PROMPT MASTER, lampirkan juga BAB_I_Pendahuluan.md (bab ini sudah final,
dipakai sebagai basis revisi). Lalu pilih SATU dari blok berikut sesuai subbab yang
ingin digarap. Ganti [SUBBAB] dengan salah satu: 1.1 Latar Belakang |
1.2 Rumusan Masalah | 1.3.1 Tujuan Penelitian | 1.3.2 Manfaat Penelitian |
1.4 Ruang Lingkup | 1.5 Sistematika Penulisan.]

TUGAS: Tulis ULANG/PERDALAM subbab [SUBBAB] pada BAB I, mengikuti persis kerangka isi
dan kalimat kunci pada rancangan-isi-skripsi-eews-observabilitas.md Bagian 2, Sub Bab
[SUBBAB]. Jangan menulis subbab lain di luar yang diminta. Jika subbab ini bergantung
pada subbab lain (mis. 1.3.1 Tujuan harus selaras dengan 1.2 Rumusan Masalah), tampilkan
juga ringkasan satu kalimat dari subbab yang menjadi acuannya sebelum menulis subbab
yang diminta, agar keselarasan dapat diperiksa.

KELUARAN: teks subbab yang diminta saja, siap tempel ke draf, plus catatan singkat (2–3
kalimat) di akhir tentang bagian mana dari rancangan-isi-skripsi yang belum bisa dipenuhi
karena keterbatasan informasi (jika ada), tanpa mengarang isinya.
```

---

## 4. PROMPT BAB II — TINJAUAN PUSTAKA

> **[STATUS: BAB INI SUDAH FINAL — `BAB_II_Tinjauan_Pustaka.md`]** Sub Bab 4.1 di bawah adalah arsip prompt "generate lengkap" yang dipakai saat BAB II pertama kali disusun; **jangan dipakai lagi** untuk menulis ulang seluruh bab dari nol, karena struktur aktual sudah berkembang menjadi 10 subbab dasar teori (2.2.1–2.2.10, termasuk notasi pemodelan sistem, desain eksperimen, dan benchmarking yang tidak ada di prompt arsip ini) — lihat `rancangan-isi-skripsi-eews-observabilitas.md` Bagian 3 (Revisi-1) untuk struktur final. Gunakan **Sub Bab 4.2 (Prompt Per Sub Bab II)** yang sudah diperbarui bila perlu merevisi/memperdalam salah satu subbab yang sudah final.

### 4.1 Prompt Bab II (versi lengkap sekaligus) — ARSIP, JANGAN DIPAKAI ULANG

```
[Sertakan PROMPT MASTER, lalu lanjutkan.]

TUGAS: Tulis BAB II TINJAUAN PUSTAKA secara lengkap: paragraf pembuka bab (identik
dengan Sub Bab 1.5 pada Bab I), 2.1 Penelitian Terdahulu, dan 2.2 Dasar Teori
(2.2.1–2.2.7).

DAFTAR PUSTAKA YANG BOLEH DIPAKAI: HANYA yang tercantum di
rancangan-daftar-pustaka-eews-observabilitas.md Bagian 1 (24 entri dipertahankan) dan
Bagian 4/4A (4 entri baru: Wang dkk. 2025, Chodorek & Chodorek 2025, Nguyen dkk. 2022,
selain Ma & Chi 2022 yang sudah ada di Bagian 1). JANGAN memakai lima pustaka di Bagian 2
(Niswar dkk. 2024, L. Zhang dkk. 2023, Kumar dkk. 2026, Luis dkk. 2021, Kaviarasan dkk.
2022) — kelimanya spesifik gRPC/RPC/serialisasi biner dan tidak relevan lagi. JANGAN
memakai pustaka di Bagian 3 (Shahid dkk. 2023, de Carvalho Neto dkk. 2025, Hlayel dkk.
2025) karena sudah ditarik dari daftar setelah verifikasi.

2.1 PENELITIAN TERDAHULU:
- Susun narasi naratif berkelompok 3 klaster tematik:
  Klaster 1 — EEWS berbasis deep learning & arsitektur terdistribusi (Zhu dkk. 2023,
    M. Zhang dkk. 2022, Wibowo dkk. 2024, Naoi dkk. 2024, Lian dkk. 2024, Liu & Tan
    2025, Carvalho dkk. 2025, Temneanu dkk. 2025, Kolivand dkk. 2024, Abdalzaher dkk.
    2023, Ranasinghe dkk. 2024, Häusler dkk. 2022, Melgarejo-Hernández dkk. 2026).
  Klaster 2 — Microservices, message broker, WebSocket, load balancing (Al Qassem dkk.
    2024, Song & Kook 2022, Martín dkk. 2022, Raptis & Passarella 2023, Raptis dkk.
    2024, Wang dkk. 2025, Chodorek & Chodorek 2025, Ma & Chi 2022, Nguyen dkk. 2022).
  Klaster 3 — Observabilitas & benchmarking sistem terdistribusi (Faseeha dkk. 2025,
    Usman dkk. 2022, Tzanettis dkk. 2022, Henning & Hasselbring 2024, Oluwasakin dkk.
    2023).
- Setiap penelitian dirujuk dengan pola: "penulis (tahun) melakukan/mengembangkan X,
  menghasilkan Y, dengan keterbatasan/gap Z."
- Buat Tabel 2.1 Ringkasan Penelitian Terkait: kolom [Penulis (Tahun) | Topik |
  Metode/Teknologi | Hasil/Kontribusi], mencakup seluruh pustaka di ketiga klaster.
- Buat Tabel 2.2 Posisi Penelitian: baris = penelitian terdahulu (pilih representatif
  dari tiap klaster) + "Penelitian Ini"; kolom fitur kunci = Microservices, Kafka,
  Docker, WebSocket, Prometheus, Grafana, Evaluasi Latensi/Reproducibility. Baris
  "Penelitian Ini" WAJIB mencentang WebSocket, Prometheus, DAN Grafana secara
  bersamaan — TIDAK ada kolom gRPC.
- Paragraf penutup: sintesis gap penelitian secara eksplisit — "belum ada penelitian
  yang secara bersamaan mengintegrasikan arsitektur microservices berbasis WebSocket
  dengan lapisan observabilitas Prometheus dan Grafana pada konteks EEWS."

2.2 DASAR TEORI — tulis tujuh sub-subbab berurutan dari umum ke spesifik:
  2.2.1 Earthquake Early Warning System (EEWS) — definisi, prinsip kerja tiga tahap
    (deteksi onset gelombang-P → estimasi parameter gempa → diseminasi peringatan),
    tantangan kecepatan vs akurasi dan keandalan pada kondisi kritis. Sitasi: Kolivand
    dkk. 2024, Temneanu dkk. 2025, Ranasinghe dkk. 2024, Wibowo dkk. 2024.
  2.2.2 Arsitektur Microservices dan Kontainerisasi Docker — definisi microservices vs
    monolitik, Docker & Docker Compose. Sitasi: Al Qassem dkk. 2024, Song & Kook 2022.
  2.2.3 Apache Kafka sebagai Message Broker — topic, partition, consumer group, broker;
    peran Kafka di pipeline EEWS (asinkron, fault-tolerant). Sitasi: Martín dkk. 2022,
    Raptis & Passarella 2023, Raptis dkk. 2024.
  2.2.4 WebSocket sebagai Protokol Komunikasi Real-Time — definisi, karakteristik
    full-duplex, perbedaan dengan HTTP polling/REST biasa, alasan pemilihan WebSocket
    (ringan, cukup untuk skala sistem, mudah diimplementasikan di klien berbasis
    browser). PENTING: JANGAN membandingkan dengan gRPC sebagai opsi yang sempat
    dipertimbangkan lalu ditinggalkan — WebSocket dibahas sebagai pilihan desain
    langsung. Sitasi: Wang dkk. 2025, Chodorek & Chodorek 2025.
  2.2.5 Load Balancing dengan NGINX — definisi load balancing, algoritma umum
    (round-robin, least connection), peran NGINX sebagai reverse proxy pada endpoint
    HTTP dan/atau broker Kafka. Sitasi: Ma & Chi 2022 (rujukan teknis utama NGINX),
    Nguyen dkk. 2022 (pembanding pendekatan proxy-based vs orchestrator-based —
    posisikan sebagai pembanding, BUKAN deskripsi teknis NGINX itu sendiri, karena
    levelnya container/Kubernetes bukan NGINX secara harfiah).
  2.2.6 Observabilitas Sistem Terdistribusi — definisi observabilitas (bukan sekadar
    monitoring), tiga pilar (metrik/log/trace); Prometheus (model scraping, time-series
    database, PromQL, jenis metrik Counter/Gauge/Histogram); Node Exporter (metrik host);
    Grafana (visualisasi, integrasi datasource Prometheus); pustaka prometheus_client
    (Python) dan padanan Node.js. Sitasi: Faseeha dkk. 2025 (definisi utama tiga pilar),
    Usman dkk. 2022, Tzanettis dkk. 2022.
  2.2.7 Benchmarking Sistem Terdistribusi — definisi benchmarking, metrik umum (latensi,
    throughput, resource usage), prinsip reproducibility (jumlah trial, kontrol
    variabel, statistik deskriptif mean/median/P95), justifikasi P95 lebih relevan
    daripada rata-rata untuk sistem time-critical. Sitasi: Henning & Hasselbring 2024
    (rujukan metodologis utama), Oluwasakin dkk. 2023 (opsional, relevansi lebih tipis).

KELUARAN: teks lengkap Bab II dengan Tabel 2.1 dan Tabel 2.2 dalam format tabel markdown,
sitasi APA inline, tanpa satupun pustaka dari daftar yang dikeluarkan/ditolak.
```

### 4.2 Prompt Per Sub Bab II (granular) — DIPERBARUI, gunakan ini untuk revisi

```
[Sertakan PROMPT MASTER, lampirkan juga BAB_II_Tinjauan_Pustaka.md (bab ini sudah final,
dipakai sebagai basis revisi) dan BAB_I_Pendahuluan.md (untuk cek konsistensi istilah dan
verbatim paragraf pembuka). Lalu pilih SATU subbab: 2.1 Penelitian Terdahulu |
2.2.1 EEWS | 2.2.2 Microservices & Docker (termasuk 2.2.2.1 Dekomposisi Layanan Berbasis
Domain) | 2.2.3 Apache Kafka | 2.2.4 WebSocket | 2.2.5 Load Balancing NGINX |
2.2.6 Observabilitas | 2.2.7 Framework & Teknologi Pendukung (2.2.7.1–2.2.7.5) |
2.2.8 Notasi Pemodelan Sistem (2.2.8.1 UML | 2.2.8.2 Flowchart | 2.2.8.3 C4 Model |
2.2.8.4 DFD) | 2.2.9 Desain Penelitian Eksperimental Kuantitatif |
2.2.10 Pengujian Perangkat Lunak dan Benchmarking Sistem Terdistribusi.]

TUGAS: Tulis ULANG/PERDALAM subbab [SUBBAB] pada BAB II, dengan tetap konsisten dengan
isi subbab [SUBBAB] yang SUDAH ADA di BAB_II_Tinjauan_Pustaka.md yang dilampirkan
(nomor Gambar/Tabel yang sudah dipakai TIDAK BOLEH diubah nomornya kecuali memang
diminta eksplisit). Sebelum menulis, sebutkan secara eksplisit daftar pustaka yang akan
dipakai/dipertahankan untuk subbab ini, merujuk baik ke
rancangan-daftar-pustaka-eews-observabilitas.md maupun ke pustaka yang SUDAH terbukti
dikutip di subbab tersebut pada BAB_II_Tinjauan_Pustaka.md (mis. Sugiyono 2022 untuk
2.2.9, Sommerville 2016 untuk 2.2.10, Brown 2022 untuk 2.2.8.3), baru tulis isi subbab.
Jika subbab yang diminta adalah 2.2.4 (WebSocket) atau 2.2.5 (Load Balancing NGINX),
tegaskan kembali batasan kecocokan pustaka sesuai catatan di rancangan-daftar-pustaka
Bagian 4/4A sebelum menulis.

KELUARAN: teks subbab yang diminta saja, siap tempel ke draf.
```

---

## 5. PROMPT BAB III — METODE PENELITIAN

> **[REVISI UTAMA]** Bagian ini dirombak total mengikuti `rancangan-isi-skripsi-eews-observabilitas.md` Bagian 4 (Revisi-1). Tiga perbedaan penting dari versi lama: (1) wajib melampirkan `BAB_I_Pendahuluan.md` dan `BAB_II_Tinjauan_Pustaka.md` karena BAB III sekarang merujuk balik ke teori dan notasi yang sudah ditulis di sana, bukan mendefinisikan ulang; (2) ditambahkan Gambar 3.1 alur metodologi menyeluruh serta notasi arsitektur eksplisit (C4 *Model*, DFD); (3) Tabel skenario pengujian (S1–S4) mendapat kolom profil beban kerja dan prosedur otomatisasi, plus opsi S5 yang bersifat opsional.

### 5.1 Prompt Bab III (versi lengkap sekaligus)

```
[Sertakan PROMPT MASTER. WAJIB lampirkan juga BAB_I_Pendahuluan.md dan
BAB_II_Tinjauan_Pustaka.md di luar tiga file acuan standar — JANGAN lanjutkan menulis
jika salah satu dari kedua file ini tidak dilampirkan, karena instruksi di bawah
mengasumsikan isi keduanya sudah dibaca.]

TUGAS: Tulis BAB III METODE PENELITIAN secara lengkap: paragraf pembuka bab, Gambar 3.1
Alur Metodologi Penelitian, 3.1 Jenis dan Pendekatan Penelitian, 3.2 Studi Literatur dan
Analisis Kebutuhan, 3.3 Perancangan Arsitektur Sistem, 3.4 Implementasi Sistem
(3.4.1–3.4.4), 3.5 Perancangan Skenario Pengujian, 3.6 Pengumpulan dan Analisis Data.

PARAGRAF PEMBUKA BAB: harus SAMA PERSIS (verbatim) dengan kalimat berikut, dan salin
persis pula ke entri BAB III pada Sub Bab 1.5 BAB_I_Pendahuluan.md bila belum sama:
"Bab ini membahas jenis dan pendekatan penelitian, tahap perancangan arsitektur sistem,
implementasi sistem, hingga perancangan skenario pengujian. Bab ini menjelaskan
bagaimana lapisan observabilitas Prometheus dan Grafana dirancang dan diintegrasikan ke
dalam pipeline EEWS, serta metode yang digunakan untuk mengukur performanya."

GAMBAR 3.1 ALUR METODOLOGI PENELITIAN — WAJIB ADA sebelum Sub Bab 3.1, mengikuti pola
diagram alir "Mulai → tahap-tahap berurutan → Selesai" (bukan diagram Scrum/ICONIX
karena penelitian ini eksperimental-linear). Tuliskan sebagai deskripsi gambar (karena
gambar aktual dibuat terpisah) dengan urutan tahap PERSIS: Mulai → (3.1) Jenis &
Pendekatan Penelitian dan Definisi Variabel → (3.2) Studi Literatur & Analisis Kebutuhan
→ (3.3) Perancangan Arsitektur Sistem → (3.4) Implementasi Sistem → (3.5) Perancangan
Skenario Pengujian → (3.6) Pelaksanaan Pengujian & Pengumpulan Data → (3.7) Analisis
Data → Selesai. Sertakan paragraf narasi singkat (deskripsi gambar) di bawah judul
gambar, mengikuti gaya penulisan deskripsi gambar pada kedua contoh skripsi acuan gaya.

3.1 JENIS DAN PENDEKATAN PENELITIAN:
- Jenis: penelitian eksperimental (experimental research) dengan pendekatan kuantitatif.
  RUJUK BALIK (jangan definisikan ulang dari nol) ke definisi Sugiyono (2022) yang SUDAH
  dijelaskan di Sub Bab 2.2.9 BAB_II_Tinjauan_Pustaka.md — cukup satu kalimat rujukan
  singkat lalu langsung terapkan ke konteks penelitian ini.
- Tegaskan secara eksplisit prinsip "satu variabel bebas per rangkaian pengujian",
  diadopsi dari pola Raptis dkk. (2024) yang SUDAH disebut di Sub Bab 2.2.9
  BAB_II_Tinjauan_Pustaka.md — kutip kembali secara singkat (bukan re-derivasi), lalu
  jelaskan bahwa setiap skenario S1–S4 di Sub Bab 3.5 hanya memvariasikan satu variabel
  bebas.
- Buat Tabel 3.1 Definisi Variabel Penelitian dengan EMPAT baris (bukan tiga seperti
  versi lama): Variabel bebas (rinci per skenario S1–S4, rujuk ke Tabel 3.3 Sub Bab 3.5),
  Variabel terikat (latensi ms, CPU %, memori MB, data delay end-to-end s — PERSIS empat
  metrik pada Ruang Lingkup Bab I, JANGAN menambah metrik lain), Variabel kontrol
  (spesifikasi mesin host, dataset seismik, bobot model deep learning tetap, topologi
  Kafka, profil beban kerja per skenario), dan Variabel diagnostik pelengkap (consumer
  lag Kafka — SEBUTKAN eksplisit bahwa ini BUKAN variabel terikat utama dan hanya
  dipakai untuk membantu interpretasi penyebab, mengadopsi Henning & Hasselbring 2024
  yang sudah dibahas di Sub Bab 2.2.10 BAB_II_Tinjauan_Pustaka.md, agar TIDAK dianggap
  memperluas Ruang Lingkup Bab I).

3.2 STUDI LITERATUR DAN ANALISIS KEBUTUHAN:
- Sumber literatur: basis data jurnal terindeks Scopus, rentang tahun 2020–2026 — SEBUT
  bahwa ini kelanjutan langsung dari metodologi SLR yang sudah dijelaskan di Sub Bab 2.1
  BAB_II_Tinjauan_Pustaka.md, bukan proses studi literatur terpisah.
- Kebutuhan fungsional: daftar modul dan alur data (mengacu Bagian 3
  konteks-aplikasi-eews-observabilitas.md).
- Kebutuhan non-fungsional: target latensi jalur kritis, granularitas metrik, interval
  scraping (JANGAN kunci angka spesifik jika belum final; tandai sebagai rentang atau
  [nilai final ditentukan saat implementasi]).
- Identifikasi titik kritis pipeline: jalur Load Balancer → P-Wave Detector, jelaskan
  singkat alasannya (melibatkan pemanggilan HTTP sinkron di tengah alur asinkron Kafka).

3.3 PERANCANGAN ARSITEKTUR SISTEM:
- Tabel 3.2 Komponen Arsitektur Sistem (nama modul, teknologi, protokol komunikasi,
  topik Kafka terkait, deskripsi fungsi) — turunkan persis dari Tabel modul di Bagian 3.1
  konteks-aplikasi-eews-observabilitas.md. Modul yang WAJIB masuk tabel: Data Provider,
  P-Wave Detector (mode consumer & mode load-balanced), Load Balancer, Location &
  Magnitude Detector, Data Archiver, WebSocket Server (varian Express.js/Socket.IO dan
  FastAPI), NGINX, Kafka Cluster, Prometheus Server, Node Exporter, Grafana Dashboard.
- Gambar 3.2 Diagram Container (C4 Model) — WAJIB memakai istilah "Container diagram
  C4 Model" secara eksplisit (BUKAN "diagram blok/komponen" generik), karena notasi ini
  SUDAH dijanjikan di Sub Bab 2.2.8.3 BAB_II_Tinjauan_Pustaka.md. Deskripsikan (karena
  gambar aktual dibuat terpisah): enam modul EEWS + tiga container observabilitas
  (Prometheus Server, Node Exporter, Grafana Dashboard) masing-masing sebagai satu
  container, panah berlabel protokol (Kafka/HTTP/WebSocket), dan titik instrumentasi
  /metrics ditandai pada tiap modul sebagai elemen visual utama.
- Gambar 3.3 Data Flow Diagram (DFD) Level Konteks dan Level 0 — WAJIB ADA (subbab ini
  TIDAK ADA di versi lama), mengikuti notasi DFD yang sudah dijelaskan di Sub Bab 2.2.8.4
  BAB_II_Tinjauan_Pustaka.md: gambarkan alur data seismik secara logis dari Data Provider
  hingga WebSocket Server tanpa detail protokol, sebagai jembatan antara Gambar 3.2 dan
  Gambar 3.4.
- Gambar 3.4 Sequence Diagram Alur Data Seismik: dari ingesti hingga diseminasi,
  termasuk titik scraping metrik oleh Prometheus.
- Jelaskan skema topik Kafka: trace_topic, p_wave_topic, loc_mag_topic, result_topic.

3.4 IMPLEMENTASI SISTEM — tulis empat sub-subbab:
  3.4.1 Implementasi Pipeline Inti EEWS — Data Provider (ingesti SeedLink/ObsPy, varian
    strategi paralelisasi jika relevan), P-Wave Detector (mode consumer langsung & mode
    load-balanced via HTTP), Load Balancer (Kafka consumer → HTTP forwarder, strategi
    distribusi), Location & Magnitude Detector, Data Archiver, WebSocket Server (varian
    Express.js/Socket.IO vs FastAPI dan alasan penyediaan lebih dari satu implementasi).
  3.4.2 Implementasi Instrumentasi Prometheus — pustaka prometheus_client (dan padanan
    Node.js) di tiap modul; jenis metrik per modul (Counter/Gauge/Histogram) diturunkan
    dari tabel rencana metrik Bagian 4 konteks-aplikasi-eews-observabilitas.md; endpoint
    /metrics per modul pada port unik; konfigurasi prometheus.yml.
  3.4.3 Implementasi Dashboard Grafana — datasource Prometheus, TEGASKAN secara eksplisit
    bahwa datasource ini DIPISAHKAN dari datasource InfluxDB yang sudah lebih dulu ada
    untuk data arsip seismik (lihat status komponen Bagian 3.3
    konteks-aplikasi-eews-observabilitas.md) — jangan biarkan pembaca mengira dashboard
    observabilitas adalah perluasan dashboard arsip yang sudah ada; rancangan panel
    (latensi per modul, CPU/memori, data delay end-to-end, jumlah klien WebSocket aktif);
    jenis visualisasi per jenis metrik (time-series graph, gauge, heatmap).
  3.4.4 Konfigurasi Docker Compose — definisi service/jaringan/volume untuk seluruh
    komponen termasuk Prometheus, Node Exporter, Grafana; konfigurasi health check agar
    scraping berjalan setelah target siap.

3.5 PERANCANGAN SKENARIO PENGUJIAN — buat Tabel 3.3 Skenario Pengujian dengan kolom
[Kode | Skenario | Variabel Bebas | Profil Beban Kerja | Variabel Terikat yang Diukur]
— kolom "Profil Beban Kerja" WAJIB ADA (tidak ada di versi lama), berisi PERSIS empat
skenario berikut:
  S1 — Overhead Instrumentasi Prometheus: variabel bebas aktif/tidaknya
    prometheus_client di seluruh modul; profil beban KONSTAN (smooth) pada laju data
    seismik tetap → selisih CPU (%), memori (MB), latensi (ms).
  S2 — Skalabilitas Multi-Container: variabel bebas jumlah instance P-Wave
    Detector/Data Archiver; profil beban smooth, dinaikkan bertahap mengikuti jumlah
    instance → data delay end-to-end (s), CPU/memori agregat.
  S3 — Perbandingan Implementasi WebSocket Server: variabel bebas jenis implementasi
    (Express.js/Socket.IO vs FastAPI); profil beban klien bertingkat (smooth naik
    bertahap) → data delay (s), CPU (%), memori (MB), jumlah klien aktif.
  S4 — Observabilitas Kafka + NGINX Load Balancer: variabel bebas konfigurasi load
    balancing (Kafka saja vs Kafka+NGINX); profil beban BURSTY (lonjakan permintaan
    mendadak), sebagai pembanding S1–S3 yang memakai beban smooth → data delay (s),
    CPU (%), memori (MB).
JELASKAN kontras profil smooth (S1–S3) vs bursty (S4) sebagai adaptasi LANGSUNG dari
Tzanettis dkk. (2022) yang SUDAH dibahas di Sub Bab 2.2.9/2.2.10 BAB_II_Tinjauan_Pustaka.md
— rujuk balik, jangan mendesain ulang dari nol seolah ide baru.

JELASKAN JUGA prosedur otomatisasi dan reproduksibilitas pengujian: setiap skenario
dijalankan melalui skrip pengujian yang identik prosedurnya lintas skenario (adaptasi
kerangka otomatisasi eksperimen reusable dari Raptis dkk. 2024, sudah dibahas di Sub Bab
2.2.10 BAB_II_Tinjauan_Pustaka.md), mencakup: (1) reset/restart seluruh container ke
kondisi awal, (2) menjalankan pembangkit beban sesuai profil yang ditentukan, (3)
mengumpulkan metrik via Prometheus API selama durasi pengujian tetap, (4) menyimpan hasil
mentah sebelum lanjut ke trial berikutnya. Sertakan jumlah trial per skenario dan alasan
stabilitas statistik.

SETELAH Tabel 3.3, sertakan SATU paragraf terpisah (JANGAN dijadikan skenario kelima
dalam tabel kecuali diminta eksplisit) yang menyebut kemungkinan skenario tambahan S5 —
Ketahanan terhadap Degradasi Layanan, adaptasi pola Martín dkk. (2022) yang sudah
dirujuk di Sub Bab 2.2.10 BAB_II_Tinjauan_Pustaka.md, DITEGASKAN sebagai OPSIONAL dan
memerlukan konfirmasi pembimbing sebelum dimasukkan sebagai skenario wajib, karena akan
memperluas Ruang Lingkup Bab I yang sudah final.

3.6 PENGUMPULAN DAN ANALISIS DATA:
- Mekanisme: Prometheus API (PromQL) untuk metrik time-series; consumer lag Kafka
  dipantau sebagai data diagnostik pelengkap (rujuk Tabel 3.1), BUKAN metrik hasil yang
  dilaporkan tersendiri.
- Format penyimpanan data pengujian (CSV).
- Metode analisis: statistik deskriptif (mean, median, standar deviasi, P95) — RUJUK
  BALIK ke justifikasi P95 yang SUDAH dijelaskan di Sub Bab 2.2.10
  BAB_II_Tinjauan_Pustaka.md, jangan dijelaskan ulang dari nol; visualisasi time-series
  via Grafana, box plot untuk perbandingan distribusi antar-kondisi.
- Jelaskan bahwa setiap hasil skenario akan dipetakan kembali ke Rumusan Masalah TUNGGAL
  Bab I (bukan ke beberapa rumusan masalah terpisah), dengan S1 khusus menjawab dimensi
  overhead pada Tujuan Penelitian.

KELUARAN: teks lengkap Bab III dengan Tabel 3.1, Tabel 3.2, dan Tabel 3.3 dalam format
tabel markdown, deskripsi Gambar 3.1–3.4 sebagai teks (karena gambar aktual dibuat
terpisah), tanpa satupun penyebutan gRPC/.proto/Protocol Buffers.
```

### 5.2 Prompt Per Sub Bab III (granular)

```
[Sertakan PROMPT MASTER. WAJIB lampirkan juga BAB_I_Pendahuluan.md dan
BAB_II_Tinjauan_Pustaka.md. Lalu pilih SATU subbab: Gambar 3.1 Alur Metodologi
Penelitian | 3.1 Jenis dan Pendekatan Penelitian | 3.2 Studi Literatur dan Analisis
Kebutuhan | 3.3 Perancangan Arsitektur Sistem | 3.4.1 Implementasi Pipeline Inti EEWS |
3.4.2 Implementasi Instrumentasi Prometheus | 3.4.3 Implementasi Dashboard Grafana |
3.4.4 Konfigurasi Docker Compose | 3.5 Perancangan Skenario Pengujian |
3.6 Pengumpulan dan Analisis Data.]

TUGAS: Tulis ULANG/PERDALAM subbab [SUBBAB] pada BAB III, sesuai isi wajib pada
rancangan-isi-skripsi-eews-observabilitas.md Bagian 4 (Revisi-1), Sub Bab [SUBBAB]. Jika
subbab yang diminta merujuk ke teori/notasi yang sudah dibahas di BAB II (mis. 3.1 ke
Sub Bab 2.2.9, atau 3.3 ke Sub Bab 2.2.8), KUTIP BALIK secara singkat — JANGAN
menjelaskan ulang teori tersebut dari nol seolah subbab BAB III berdiri sendiri. Jika
subbab membutuhkan detail modul/metrik/topik Kafka, rujuk PERSIS ke tabel/daftar pada
konteks-aplikasi-eews-observabilitas.md (Bagian 3 untuk modul, Bagian 4 untuk metrik,
Bagian 5 untuk skenario pengujian) — JANGAN menambah modul, metrik, atau skenario yang
tidak tercantum di sana, kecuali skenario opsional S5 yang memang harus ditandai
eksplisit sebagai opsional bila diminta.

KELUARAN: teks subbab yang diminta saja, siap tempel ke draf.
```

---

## 6. PROMPT BAB IV — IMPLEMENTASI DAN PENGUJIAN

### 6.1 Prompt Bab IV (versi lengkap sekaligus)

```
[Sertakan PROMPT MASTER. WAJIB lampirkan juga BAB_III_Metode_Penelitian.md (draf final
Bab III) karena Bab IV harus konsisten dengan rancangan arsitektur, tabel skenario S1–S4,
dan definisi variabel yang sudah ditetapkan di sana — JANGAN mengubah kode/nama skenario
dari yang sudah ada di Bab III.]

TUGAS: Tulis BAB IV IMPLEMENTASI DAN PENGUJIAN secara lengkap: paragraf pembuka bab,
4.1 Lingkungan Implementasi, 4.2 Implementasi Arsitektur Sistem, 4.3 Implementasi Source
Code Kunci, 4.4 Implementasi Dashboard Grafana, 4.5 Lingkungan Pengujian, 4.6 Hasil
Pengujian per Skenario (4.6.1–4.6.4), 4.7 Analisis dan Pembahasan Keseluruhan.

PERINGATAN KRITIS: Bab ini adalah bab yang PALING RENTAN terhadap karangan data. SETIAP
angka kuantitatif (latensi, CPU, memori, throughput, data delay, spesifikasi perangkat)
WAJIB berupa placeholder eksplisit — JANGAN mengisi satu angka pun secara mandiri.
Gunakan format placeholder persis: [DATA HASIL PENGUJIAN] untuk hasil pengujian, dan
[SPESIFIKASI PERANGKAT] untuk spesifikasi mesin/lingkungan.

4.1 LINGKUNGAN IMPLEMENTASI — tabel spesifikasi perangkat keras/lunak (isi kolom nilai
dengan [SPESIFIKASI PERANGKAT], JANGAN mencantumkan nomor versi pustaka spesifik kecuali
ditandai [VERSI PUSTAKA/ENVIRONMENT]); opsional struktur direktori proyek diturunkan dari
Bagian 6 konteks-aplikasi-eews-observabilitas.md (bedakan yang "sudah ada" vs "rencana
penambahan" sesuai status di dokumen tersebut).

4.2 IMPLEMENTASI ARSITEKTUR SISTEM — realisasi arsitektur dibandingkan rancangan Bab III
(sebutkan bila ada perbedaan, atau nyatakan sesuai rancangan bila tidak ada); tabel
pemetaan modul ke komponen Docker (nama service, image/base — TANPA versi spesifik,
port, dependency), rujuk struktur docker-compose.yml pada Bagian 6
konteks-aplikasi-eews-observabilitas.md.

4.3 IMPLEMENTASI SOURCE CODE KUNCI — untuk tiap potongan kode, sajikan narasi penjelasan
sebelum/sesudah kode (format Source Code sesuai template: tabel 2 baris 1 kolom, tanpa
caption/nomor daftar). WAJIB mencakup minimal:
  - Source Code inisialisasi metrik Prometheus (Counter/Gauge/Histogram) pada salah satu
    modul (mis. P-Wave Detector).
  - Source Code endpoint /metrics (start_http_server atau middleware Express/FastAPI).
  - Source Code logika inti modul kritis (mis. handler POST /trace pada P-Wave Detector
    mode load-balanced, atau logika distribusi pada Load Balancer).
  - Source Code potongan konfigurasi prometheus.yml (scrape target).
  - Source Code potongan docker-compose.yml untuk service Prometheus/Grafana/Node
    Exporter.
  CATATAN: karena kode sesungguhnya tidak dilampirkan dalam sesi ini, tulis kode berupa
  KERANGKA/CONTOH REPRESENTATIF yang konsisten dengan arsitektur pada
  konteks-aplikasi-eews-observabilitas.md, dan tandai dengan jelas jika kode ini perlu
  disesuaikan dengan kode implementasi aktual sebelum dimasukkan ke skripsi final.

4.4 IMPLEMENTASI DASHBOARD GRAFANA — deskripsi panel dashboard per kategori (latensi,
resource usage, data delay, klien aktif); jelaskan pemetaan tiap panel ke metrik/PromQL
tertentu (beri contoh query PromQL yang konsisten dengan metrik di Bagian 4
konteks-aplikasi-eews-observabilitas.md). Tandai bagian tangkapan layar dashboard sebagai
[LAMPIRAN GAMBAR DASHBOARD] karena gambar aktual dilampirkan terpisah.

4.5 LINGKUNGAN PENGUJIAN — spesifikasi mesin pengujian, kondisi jaringan, dataset
seismik ([SPESIFIKASI PERANGKAT]); prosedur eksekusi pengujian (skrip otomatis, jumlah
trial, cara reset sistem) konsisten dengan Bagian 5 rancangan-isi-skripsi (3.5).

4.6 HASIL PENGUJIAN PER SKENARIO — untuk S1–S4, gunakan struktur konsisten per skenario:
  1. Tujuan skenario (1 kalimat, mengulang Bab III).
  2. Prosedur pelaksanaan (ringkas, merujuk Bab III).
  3. Tabel/grafik hasil — WAJIB [DATA HASIL PENGUJIAN], bukan angka karangan.
  4. Pembahasan hasil — interpretasi dikaitkan teori Bab II (mis. overhead observabilitas
     dikaitkan dengan Faseeha dkk. 2025).
  Sub-subbab:
    4.6.1 Hasil Pengujian S1 — Overhead Instrumentasi Prometheus
    4.6.2 Hasil Pengujian S2 — Skalabilitas Multi-Container
    4.6.3 Hasil Pengujian S3 — Perbandingan Implementasi WebSocket Server
    4.6.4 Hasil Pengujian S4 — Observabilitas Kafka + NGINX Load Balancer

4.7 ANALISIS DAN PEMBAHASAN KESELURUHAN — sintesis lintas-skenario (pola umum, mis.
trade-off overhead vs visibilitas performa); kaitkan hasil dengan rumusan masalah/tujuan
Bab I secara eksplisit; sampaikan keterbatasan implementasi/pengujian secara jujur dan
proporsional (jika ada).

KELUARAN: teks lengkap Bab IV dengan seluruh placeholder data dipertahankan apa adanya,
source code berupa kerangka representatif yang ditandai jelas sebagai contoh.
```

### 6.2 Prompt Per Sub Bab IV (granular)

```
[Sertakan PROMPT MASTER, lalu pilih SATU subbab: 4.1 Lingkungan Implementasi |
4.2 Implementasi Arsitektur Sistem | 4.3 Implementasi Source Code Kunci |
4.4 Implementasi Dashboard Grafana | 4.5 Lingkungan Pengujian |
4.6.1 Hasil Pengujian S1 | 4.6.2 Hasil Pengujian S2 | 4.6.3 Hasil Pengujian S3 |
4.6.4 Hasil Pengujian S4 | 4.7 Analisis dan Pembahasan Keseluruhan.]

TUGAS: Tulis ULANG/PERDALAM subbab [SUBBAB] pada BAB IV. WAJIB mempertahankan setiap
placeholder [DATA HASIL PENGUJIAN] dan [SPESIFIKASI PERANGKAT] yang relevan dengan
subbab ini — JANGAN mengisi satu angka pun secara mandiri, bahkan sebagai "contoh
ilustratif", kecuali diminta eksplisit oleh pengguna dan ditandai jelas sebagai ilustrasi
bukan data nyata.

KELUARAN: teks subbab yang diminta saja, siap tempel ke draf.
```

---

## 7. PROMPT BAB V — PENUTUP

```
[Sertakan PROMPT MASTER, lalu lanjutkan. WAJIB lampirkan juga hasil akhir Bab IV Sub Bab
4.6–4.7 yang sudah diisi data nyata, serta BAB_I_Pendahuluan.md, karena Bab V bergantung
penuh pada hasil tersebut dan harus selaras 1-ke-1 dengan Tujuan Penelitian di Bab I.]

TUGAS: Tulis BAB V PENUTUP secara lengkap: paragraf pembuka bab, 5.1 Kesimpulan, 5.2
Saran.

Paragraf pembuka bab: satu paragraf yang menyatakan bab ini memuat kesimpulan dari
keseluruhan penelitian serta saran pengembangan lebih lanjut. (Selaraskan verbatim dengan
paragraf BAB V pada Sub Bab 1.5 Bab I bila belum sama persis.)

5.1 KESIMPULAN:
- Ditulis sebagai poin bernomor, SELARAS 1-KE-1 dengan Tujuan Penelitian di Bab I (bukan
  ringkasan bebas) — setiap tujuan dijawab dengan satu simpulan yang didukung
  [DATA HASIL PENGUJIAN].
- Contoh pola kalimat: "Arsitektur microservices EEWS berbasis Kafka dan WebSocket
  berhasil dirancang dan diimplementasikan, terdiri atas enam modul utama yang saling
  berkomunikasi secara asinkron melalui tiga topik Kafka."
- Tutup dengan simpulan tentang overhead observabilitas (jawaban atas pertanyaan
  validasi S1) sebagai temuan kunci penelitian.
- JANGAN mengarang angka simpulan; jika hasil pengujian belum tersedia saat sesi ini,
  pertahankan [DATA HASIL PENGUJIAN] di titik yang relevan.

5.2 SARAN — poin bernomor, mencakup tiga kategori:
  1. Saran teknis pengembangan lanjutan (mis. alerting otomatis berbasis Prometheus
     Alertmanager, tracing terdistribusi/OpenTelemetry sebagai pelengkap metrik).
  2. Saran metodologis untuk penelitian lanjutan (mis. pengujian pada skala data/klaster
     lebih besar, pengujian pada infrastruktur cloud produksi).
  3. Saran praktis bagi pengembang sistem EWS lain yang ingin mengadopsi pendekatan
     observabilitas serupa.

KELUARAN: teks lengkap Bab V, dengan Kesimpulan yang secara eksplisit menyebut nomor
tujuan penelitian yang dijawab oleh tiap poin.
```

---

## 8. PROMPT DAFTAR PUSTAKA & LAMPIRAN

```
[Sertakan PROMPT MASTER, lalu lanjutkan.]

TUGAS: Susun DAFTAR PUSTAKA final dan daftar usulan LAMPIRAN.

DAFTAR PUSTAKA:
- Kompilasi seluruh pustaka yang benar-benar dikutip di draf Bab I–V yang sudah ditulis
  sejauh ini (bukan seluruh pustaka yang tersedia di rancangan-daftar-pustaka, hanya yang
  benar-benar disitasi).
- Format APA, disusun alfabetis berdasarkan nama belakang penulis, mengikuti gaya pada
  Daftar Pustaka proposal lama (TubesMPPI_..._Mohamad.pdf) HANYA sebagai contoh format
  penulisan entri (bukan sebagai sumber isi) — perhatikan urutan penulis, tahun dalam
  kurung, judul, nama jurnal (italic), volume(issue), halaman, DOI.
- Tandai secara eksplisit bila ada entri yang dikutip di draf tetapi TIDAK ada di
  rancangan-daftar-pustaka-eews-observabilitas.md — ini adalah tanda kutipan yang perlu
  diverifikasi ulang sebelum dipakai (jangan otomatis menghapus, tapi beri catatan
  "[PERLU VERIFIKASI: tidak ditemukan di rancangan pustaka]").

LAMPIRAN (usulan isi, sesuai rancangan-isi-skripsi-eews-observabilitas.md Bagian 7):
  Lampiran 1 — Konfigurasi lengkap prometheus.yml dan docker-compose.yml.
  Lampiran 2 — Tabel mentah hasil pengujian tiap skenario (sebelum diringkas jadi
    statistik deskriptif di Bab IV) — [DATA HASIL PENGUJIAN].
  Lampiran 3 — Contoh query PromQL yang digunakan pada tiap panel dashboard Grafana.
  Lampiran 4 — Dokumentasi tangkapan layar dashboard Grafana secara lengkap.

KELUARAN: Daftar Pustaka lengkap (format APA, alfabetis) + daftar Lampiran dengan
deskripsi singkat tiap lampiran.
```

---

## 9. Checklist Anti-Karang & Anti-Kontaminasi gRPC (jalankan setelah setiap keluaran AI)

Setelah AI menghasilkan draf apa pun dari prompt di atas, periksa manual dengan checklist
berikut sebelum menerima hasilnya:

- [ ] Tidak ada kata "gRPC", "Protocol Buffers", "protobuf", "RPC biner", atau ".proto"
      muncul di manapun (kecuali kalimat historis eksplisit yang sengaja diminta).
- [ ] Semua sitasi yang muncul ada di rancangan-daftar-pustaka-eews-observabilitas.md
      Bagian 1 atau Bagian 4/4A, ATAU terbukti sudah dikutip di file bab final yang
      dilampirkan (mis. Sugiyono 2022, Sommerville 2016, Brown 2022, Newman 2021,
      Kitchenham & Charters 2007, Kendall & Kendall 2011) — tidak ada pustaka dari
      Bagian 2 atau Bagian 3 rancangan-daftar-pustaka, dan tidak ada pustaka karangan.
- [ ] Tidak ada angka kuantitatif hasil pengujian yang "terlihat nyata" tanpa ditandai
      [DATA HASIL PENGUJIAN] atau [SPESIFIKASI PERANGKAT].
- [ ] Tidak ada nomor versi pustaka/environment spesifik yang disebut tanpa penanda
      [VERSI PUSTAKA/ENVIRONMENT].
- [ ] Nama modul konsisten dengan daftar baku (Data Provider, P-Wave Detector, Load
      Balancer, Location & Magnitude Detector, Data Archiver, WebSocket Server,
      Prometheus Server, Node Exporter, Grafana Dashboard).
- [ ] Paragraf pembuka bab (jika ditulis ulang) tetap identik verbatim dengan paragraf
      terkait di Sub Bab 1.5 Sistematika Penulisan.
- [ ] Tidak ada narasi yang memposisikan sistem sebagai "melanjutkan"/"mereplikasi"
      proyek atau paper pihak eksternal.
- [ ] **[Khusus BAB III]** Gambar 3.1 Alur Metodologi Penelitian ada dan urutan
      tahapnya sesuai Sub Bab 3.1–3.6 (tidak memakai pola Scrum/ICONIX).
- [ ] **[Khusus BAB III]** Gambar 3.2 memakai istilah eksplisit "Container diagram
      C4 Model" (bukan "diagram blok/komponen" generik), dan Gambar 3.3 DFD ada sebagai
      subbab tersendiri sebelum sequence diagram.
- [ ] **[Khusus BAB III]** Tabel 3.3 skenario pengujian memiliki kolom "Profil Beban
      Kerja" dengan kontras smooth (S1–S3) vs bursty (S4), dan disertai penjelasan
      prosedur otomatisasi/reproduksibilitas pengujian.
- [ ] **[Khusus BAB III]** Skenario S5 (bila disinggung) ditulis eksplisit sebagai
      OPSIONAL/memerlukan konfirmasi pembimbing, tidak dimasukkan sebagai skenario wajib
      ke-lima di Tabel 3.3 tanpa persetujuan.
- [ ] **[Khusus BAB III]** Definisi teori (jenis penelitian eksperimental, prinsip P95,
      notasi C4/DFD) TIDAK dijelaskan ulang dari nol — hanya dirujuk balik singkat ke
      BAB_II_Tinjauan_Pustaka.md.
