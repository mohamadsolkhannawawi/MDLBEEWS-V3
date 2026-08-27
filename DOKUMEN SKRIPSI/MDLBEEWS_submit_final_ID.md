# *MDLBEEWS: Sistem Peringatan Dini Gempa Bumi Berbasis Deep Learning Modular*

*Satriawan Rasyid Purnama^a^ (satriawanrasyid@live.undip.ac.id)*
*Adi Wibowo^a,\*^ (bowo.adi@live.undip.ac.id)*
*Arjuna Wahyu Kusuma^a^ (arjunawahyukusuma@alumni.undip.ac.id)*
*Liem Roy Marcelino^a^ (liemroym@alumni.undip.ac.id)*
*Indra Waspada^a^ (indrawaspada@lecturer.undip.ac.id)*
*Cecep Pratama^b^ (cecep.pratama@ugm.ac.id)*
*Leni Sophia Heliani^b^ (lheliani@ugm.ac.id)*
*David Prambudi Sahara^c^ (david.sahara@gf.itb.ac.id)*
*Sri Widiyantoro^c^ (ilikwidi@gmail.com)*
*Shindy Rosalia^c^ (shindy.rosalia31@gmail.com)*
*Bondan Febriarta^c^ (32324301@mahasiswa.itb.ac.id)*
*Cahyo Adhi Hartanto^d^ (cahyo.adhi97@gmail.com)*

*^a^Departemen Informatika, Universitas Diponegoro, Semarang, Indonesia*

*^b^Departemen Teknik Geodesi, Universitas Gadjah Mada, Yogyakarta, Indonesia*

*^c^Kelompok Riset Geofisika Global, Fakultas Teknik Pertambangan dan Perminyakan, Institut Teknologi Bandung, Bandung, Indonesia*

*^d^Fakultas Ilmu Komputer, Universitas Indonesia, Depok, Indonesia*

^\*^Penulis korespondensi

## Abstrak

*MDLBEEWS adalah Sistem Peringatan Dini Gempa Bumi (EEWS) yang telah dioptimalkan dengan memanfaatkan deep learning untuk menghasilkan prediksi gempa yang akurat dan tepat waktu. Dengan arsitektur modular dan kontainerisasi Docker, sistem ini menjamin kemudahan deployment dan skalabilitas. Sistem mengintegrasikan multiprocessing untuk pemrosesan data yang efisien serta menggunakan Kafka bersama NGINX untuk meminimalkan keterlambatan data. Komunikasi WebSocket memfasilitasi penyebaran peringatan secara langsung. Dirancang untuk digunakan oleh peneliti geofisika, lembaga penanggulangan bencana, dan pengembang teknologi, sistem ini memberikan peningkatan performa, skalabilitas, dan efisiensi sumber daya, sekaligus mengatasi keterbatasan kritis pada implementasi EEWS yang ada saat ini.*

## Kata Kunci

*Sistem Peringatan Dini Gempa Bumi, Deep Learning, Pemrosesan Data Seismik Real-time, Deployment Terkontainerisasi, Penyebaran Peringatan Berbasis WebSocket*

## Metadata Kode

| **Nr** | **Deskripsi metadata kode** | **Mohon diisi pada kolom ini** |
|---|---|---|
| C1 | Versi kode saat ini | *v1.0* |
| C2 | Tautan permanen ke kode/repositori yang digunakan untuk versi kode ini | *<https://github.com/ArjunaWahyu/paper-eews.git>* |
| C3 | Tautan permanen ke capsule yang dapat direproduksi | <https://codeocean.com/capsule/xxxxxx/tree/v1> |
| C4 | Lisensi hukum kode | *Lisensi MIT* |
| C5 | Sistem pengontrol versi kode yang digunakan | *git* |
| C6 | Bahasa, alat, dan layanan kode perangkat lunak yang digunakan | *Python dan JavaScript* |
| C7 | Persyaratan kompilasi, lingkungan operasi, dan dependensi | *Python \>= 3.7,* *TensorFlow \>= 2.10, Docker, ObsPy, Kafka, FastAPI, Websockets* |
| C8 | Jika tersedia, tautan ke dokumentasi/manual pengembang | *<https://github.com/ArjunaWahyu/paper-eews/blob/main/README.md>* |
| C9 | Email dukungan untuk pertanyaan | *<bowo.adi@live.undip.ac.id>* |

1. **Pendahuluan**

Penyediaan peringatan yang cepat pada momen-momen awal terjadinya gempa bumi sangat penting untuk mengurangi potensi kerusakan dan korban jiwa. Sistem Peringatan Dini Gempa Bumi (EEWS) pada awalnya mengandalkan deteksi manual gelombang seismik, namun sejak itu telah berkembang ke teknik-teknik terbaru seperti STA/LTA dan match filtering [1,2]. Tinjauan sistematis terbaru juga mengonfirmasi bahwa model berbasis AI, khususnya pendekatan neural dan probabilistik, secara signifikan meningkatkan akurasi dan responsivitas EEW [3]. Namun, metode-metode ini masih menghadapi tantangan dalam hal akurasi dan efisiensi. Inovasi terbaru mencakup alur kerja berbasis machine learning seperti PhaseNet, PickNet, dan sistem seperti LOC-FLOW dan QuakeFlow, yang mengintegrasikan deep learning dengan cloud computing untuk meningkatkan kecepatan dan kemampuan deteksi [4,5,6]. Perkembangan terbaru juga menunjukkan kelayakan sistem EEW yang sepenuhnya mandiri (self-contained) menggunakan akselerometer MEMS dan mikrokontroler untuk deteksi berbasis spektral [7].

Beberapa platform perangkat lunak EEWS open-source dan berbasis riset telah dikembangkan, seperti SeisComP, Earthworm, ElarmS, dan PRESTo. Meskipun sistem-sistem ini bernilai, sebagian besar dirancang untuk infrastruktur tersentralisasi atau kurang fleksibel untuk diintegrasikan dengan alur kerja modern berbasis cloud yang mendukung deep learning [8,9].

QuakeFlow merupakan contoh arsitektur EEWS yang canggih, menggabungkan streaming data real-time melalui Kafka, kontainerisasi yang dapat diskalakan dengan Docker dan Kubernetes, serta komunikasi internal dengan FastAPI [10]. Sistem ini mendukung data seismik baik yang terarsip maupun real-time, menawarkan fleksibilitas dan skalabilitas [5]. Meskipun terdapat kemajuan tersebut, penggunaan deep learning dan pemrosesan terdistribusi menimbulkan biaya komputasi dan masalah latensi yang tinggi [2,11–13]. Sistem berbasis machine learning, seperti pengklasifikasi decision tree, telah menunjukkan akurasi prediktif yang tinggi (hingga 95%) untuk deteksi bencana dini [14], yang memperkuat kelayakan pengintegrasian komponen AI ringan ke dalam arsitektur EEWS modular guna menyeimbangkan akurasi dan efisiensi. Model deep learning hibrida yang menggabungkan CapsNet dan LSTM telah menunjukkan performa prediktif yang unggul, mencapai akurasi hingga 95,6% untuk tugas prediksi gempa [15], yang mendukung efektivitas pengintegrasian modul AI serupa ke dalam kerangka kerja EEWS modular.

Dalam studi ini, kami mengembangkan prototipe perangkat lunak EEWS berbasis cloud yang bertujuan untuk mengoptimalkan pemrosesan data seismik real-time dan penyebaran peringatan. Sistem ini mengintegrasikan multiprocessing untuk ingestion data secara paralel [16,17], load balancing berbasis NGINX untuk distribusi yang efisien [18], eksekusi multi-container modular untuk skalabilitas, dan Express.js untuk komunikasi WebSocket dengan latensi rendah [19]. Penelitian ini berkontribusi pada arsitektur perangkat lunak EEWS yang modular, efisien, dan dapat diskalakan, yang mengatasi keterbatasan performa yang ada serta menawarkan kompatibilitas dengan model deteksi berbasis machine learning saat ini maupun di masa depan.

2. **Deskripsi Perangkat Lunak**

**[Gambar: Diagram Arsitektur EEWS yang Diusulkan]** — Deskripsi gambar: Diagram alur sistem berjudul "Earthquake Early Warning System" berbentuk kotak besar dengan rounded corner berisi enam modul: Data Provider, Message Broker, Data Archiver, Database (silinder), P Wave Detector, Location Magnitude Detector, dan WebSocket. Di luar kotak besar, sebuah ikon awan bertuliskan "Seedlink" mengalir masuk ke Data Provider, dan sebuah kotak "Frontend" berada di sisi kanan yang terhubung dengan WebSocket. Panah-panah berwarna menunjukkan jenis aliran data: merah untuk "Waveform Data", biru untuk "P Wave Data", hijau untuk "Location Magnitude Data", garis putus-putus hitam untuk "Request", dan garis hitam penuh untuk "Response". Data Provider mengalir ke Message Broker; Message Broker terhubung ke Data Archiver (yang mengalir ke Database), ke P Wave Detector, ke Location Magnitude Detector, dan ke WebSocket; WebSocket saling bertukar data dengan Database serta dengan Frontend.

> **Gbr 1.** Arsitektur EEWS yang Diusulkan

**2.1. Arsitektur EEWS**

Dalam studi ini, sebuah Sistem Peringatan Dini Gempa Bumi (EEWS) dikembangkan menggunakan kerangka kerja yang modular dan independen sebagaimana diilustrasikan pada Gbr. 1. Sistem ini mengadopsi arsitektur microservices, di mana setiap modul—ingestion data, deteksi real-time, penanganan pesan, penyimpanan, dan notifikasi—beroperasi sebagai layanan independen dengan antarmuka jaringan yang terdefinisi, sehingga meningkatkan fleksibilitas dan skalabilitas sistem [20,21,22]. Pola arsitektur ini mendukung pengembangan dan pemeliharaan aplikasi terdistribusi dan kompleks secara efisien, khususnya untuk pemrosesan seismik real-time. Teknologi kunci yang digunakan meliputi ObsPy untuk pemrosesan data seismik [23–25], Apache Kafka untuk streaming pesan [26], TensorFlow untuk deployment model deep learning [27], dan MongoDB sebagai solusi basis data backend [28]. Arsitektur ini bertujuan untuk mengurangi latensi peringatan gempa dan memastikan peringatan yang tepat waktu dan andal [21].

**2.2. Modul-Modul EEWS**

Sistem Peringatan Dini Gempa Bumi (EEWS) yang diusulkan secara arsitektural diorganisasikan ke dalam beberapa modul khusus yang berkomunikasi melalui Kafka, sehingga memungkinkan penskalaan yang fleksibel dan pemrosesan real-time yang efisien. Setiap modul memenuhi peran penting dalam alur deteksi dan peringatan end-to-end.

- **Data Provider**, sistem dimulai dengan modul Data Provider, yang bertanggung jawab untuk mengambil (ingest) aliran data seismik real-time melalui SeedLink menggunakan ObsPy. Komponen ini menekankan aliran data dengan latensi dan penggunaan sumber daya yang rendah dengan segera mengonversi trace seismik yang masuk ke dalam format JSON yang terstandardisasi. Data ini kemudian dipublikasikan ke topik Kafka tertentu, seperti trace_topic, yang memungkinkan ketersediaan data yang konsisten dan seragam bagi modul-modul berikutnya. Standardisasi ini merupakan persyaratan penting untuk performa EEWS real-time [11].

- **P-Wave Detector**, modul ini menerapkan model deep learning dengan beberapa lapisan konvolusional untuk mendeteksi onset gelombang-P [29]. Diimplementasikan dengan TensorFlow dan disajikan melalui FastAPI, modul ini menawarkan inferensi berkecepatan tinggi dengan delay minimal. FastAPI dipilih karena kemampuan penanganan permintaan asinkron dan integrasinya yang mulus dengan kerangka kerja machine learning, sehingga memfasilitasi deteksi fase yang cepat dan andal—kemampuan yang esensial untuk mengeluarkan peringatan tepat waktu [30].

- **Message Broker**, komponen sentral dalam arsitektur ini yang berfungsi sebagai message broker terdistribusi dengan menggunakan pola publish/subscribe. Kafka menangani transmisi data real-time antar-container dengan mengorganisasikan informasi ke dalam topik-topik, yaitu trace_topic untuk data gelombang, p_wave_topic untuk deteksi pick, dan result_topic untuk output dari location-magnitude detector. Pendekatan ini mendukung pemrosesan paralel oleh beberapa consumer dan memastikan distribusi data yang andal di seluruh pipeline EEWS [26].

- **Data Archiver dan Basis Data**, untuk memastikan ketersediaan data jangka panjang, modul Data Archiver berlangganan (subscribe) pada aliran gelombang dan menyimpannya dalam backend yang persisten. Sistem ini menggunakan MongoDB, basis data dokumen NoSQL yang fleksibel, yang unggul dalam menyimpan data seismik yang tidak terstruktur serta mendukung operasi I/O berkecepatan tinggi. Skema dinamis dan kemampuan indexing lanjutannya menjadikannya ideal untuk menyimpan dan mengambil informasi gelombang dalam lingkungan yang time-critical [28, 31].

- **Location and Magnitude Detector**, modul ini mengestimasi parameter-parameter kunci gempa, yaitu hiposenter dan magnitudo, berdasarkan gelombang-P yang terdeteksi. Modul ini juga memanfaatkan TensorFlow dan mengeluarkan hasil ke result_topic pada Kafka. Desain modularnya mendukung integrasi algoritma alternatif atau model yang lebih kompleks di kemudian hari untuk presisi yang lebih baik, memberikan fleksibilitas bagi evolusi sistem secara berkelanjutan.

- **WebSocket dan Frontend**, sistem ini mencakup layanan WebSocket yang mendengarkan topik Kafka dan meneruskan data real-time ke frontend. Hal ini memungkinkan pembaruan instan terhadap bentuk gelombang seismik, output deteksi, dan parameter gempa pada antarmuka klien. Baik dibangun dengan Express.js, FastAPI, maupun kerangka kerja lain, frontend dapat merender seismogram secara dinamis dan menampilkan pesan peringatan, memastikan pengguna menerima kesadaran situasional secara langsung [19].

**[Gambar: Arsitektur Data Provider yang Diusulkan]** — Deskripsi gambar: Diagram terdiri dari empat panel berlabel a) Sequential, b) Multithreading, c) Multiprocessing, dan d) Multiprocessing + Multithreading, yang membandingkan empat strategi eksekusi modul Data Provider. Panel (a) menunjukkan alur sederhana Seedlink → Data Provider (Main Process, ObsPy) → Kafka. Panel (b) menunjukkan Data Provider dengan Main Process yang men-spawn beberapa Thread (Thread 1, Thread 2, Thread 3, ..., Thread n) yang masing-masing menerima data dari Seedlink dan mengirim ke Kafka. Panel (c) serupa dengan (b) tetapi Main Process men-spawn beberapa Process (Process 1, Process 2, Process 3, ..., Process n) alih-alih thread. Panel (d) menggabungkan keduanya: Main Process men-spawn beberapa Process, dan setiap Process kembali men-spawn beberapa Thread, seluruhnya menerima data dari Seedlink dan mengalirkan hasilnya ke Kafka.

> **Gambar 2.** Arsitektur Data Provider yang Diusulkan
>
> **[Gambar: Arsitektur Message Broker yang Diusulkan dengan NGINX]** — Deskripsi gambar: Diagram menunjukkan Data Provider yang mengirim data ke sebuah "Kafka Cluster" berisi tiga node (Kafka 1, Kafka 2, Kafka 3). Kafka 1 terhubung ke Load Balancer yang meneruskan data ke beberapa instance Data Archiver (Data Archiver 1, Data Archiver 2, ..., Data Archiver N). Kafka 2 terhubung ke WebSocket. Kafka 3 terhubung ke Location Magnitude Detector serta ke Load Balancer lain yang mendistribusikan data ke beberapa instance P Wave Detector (P Wave Detector 1, P Wave Detector 2, ..., P Wave Detector N). Legenda menunjukkan tiga jenis garis: garis merah penuh untuk "All Chennel Waveform Data", garis merah putus-putus untuk "Z Chennel Waveform Data", dan garis biru untuk "P Wave Data".
>
> **Gambar 3.** Arsitektur Message Broker yang Diusulkan dengan NGINX.

**2.3. Optimisasi**

Evaluasi performa Sistem Peringatan Dini Gempa Bumi (EEWS) yang diusulkan berfokus pada identifikasi kombinasi teknologi yang paling efektif untuk mengoptimalkan pemrosesan data real-time dan mengurangi latensi sistem. Beberapa komponen optimisasi dikembangkan dan diuji dalam berbagai skenario untuk menilai dampaknya terhadap metrik performa utama: penggunaan CPU, penggunaan memori, dan keterlambatan data. Evaluasi dilakukan menggunakan 500 sampel uji coba untuk setiap kasus uji, dengan pemantauan sumber daya melalui Docker Desktop. Modul eksperimen adalah sebagai berikut:

- **Multithreaded dan Multiprocessing**, Modul Data Provider diuji menggunakan empat strategi eksekusi: sequential, multithreaded, multiprocessing, dan hibrida multithreaded + multiprocessing. Mode sequential dasar memproses data gelombang seismik satu per satu pada satu thread, yang sering mengakibatkan latensi tinggi dan ketidakstabilan saat beban tinggi. Pendekatan multithreaded meningkatkan throughput dengan memungkinkan operasi konkuren dalam satu proses [17]. Multiprocessing memanfaatkan beberapa proses independen yang didistribusikan di berbagai core CPU untuk meningkatkan skalabilitas dan performa [16]. Model hibrida menggabungkan kedua teknik tersebut, mendistribusikan tugas ke berbagai thread dan proses, sehingga menawarkan pemanfaatan sumber daya yang optimal dalam hal CPU, memori, dan delay. Detail arsitektural dari setiap pendekatan diilustrasikan pada Gbr. 2.

- **Konfigurasi Kafka dengan NGINX**, Pada konfigurasi ini, sebagaimana ditunjukkan pada Gbr. 3, Kafka berfungsi sebagai message broker untuk distribusi gelombang secara real-time. Untuk meningkatkan throughput data dan mendukung pemrosesan yang dapat diskalakan, Kafka di-deploy dengan tiga broker dan topik yang dipartisi (trace_topic, p_wave_topic, result_topic), memungkinkan konsumsi paralel oleh komponen seperti Data Archiver dan P-Wave Detector. Untuk memperkuat throughput dan ketersediaan tinggi, sistem dapat menggunakan tiga broker Kafka bersama NGINX, yang dapat berfungsi sebagai reverse proxy dan load balancer [32]. Dengan menggabungkan NGINX sebagai load balancer, sistem dapat secara efektif mendistribusikan permintaan klien, mengurangi bottleneck, dan meningkatkan efisiensi aliran data [33]. Konfigurasi ini memaksimalkan throughput, meminimalkan delay, dan mengurangi bottleneck performa pada saat traffic tinggi [34–36].

- **Multicontainer**, Untuk lebih meningkatkan responsivitas sistem, modul Data Archiver dan P-Wave Detector diskalakan menggunakan setup multi-container. Dalam pengujian, Data Archiver di-deploy menggunakan 1 hingga 5 container. Hal ini memungkinkan operasi penyimpanan secara paralel, mengurangi bottleneck dan meningkatkan throughput sistem. Desain multi-container ini meningkatkan baik kecepatan maupun skalabilitas penanganan data seismik, memastikan ketersediaan gelombang yang cepat untuk pemrosesan lebih lanjut.

- **Express.js**, Modul WebSocket bertanggung jawab untuk meneruskan data seismik real-time termasuk gelombang, lokasi, dan magnitudo ke antarmuka frontend. Dua kerangka kerja dievaluasi: FastAPI dan Express.js. Meskipun FastAPI menawarkan integrasi yang erat dengan pipeline inferensi berbasis Python dan penanganan asinkron yang efisien [30], Express.js, yang dibangun di atas arsitektur event-driven Node.js, menunjukkan performa yang lebih unggul dalam menangani volume tinggi koneksi WebSocket secara simultan. Express.js mengurangi penggunaan CPU sambil mempertahankan responsivitas dalam penyiaran data [19]. Setiap kerangka kerja memiliki trade-off tergantung pada traffic yang diharapkan dan keselarasan ekosistem.

3. **Contoh**

Untuk menjalankan sistem, pengguna disarankan menggunakan Docker Compose, yang memfasilitasi orkestrasi container secara terstruktur dan dapat direproduksi. Sistem dapat dijalankan dalam mode detached menggunakan perintah "docker-compose up -d", yang memungkinkan eksekusi di latar belakang. Sebagai alternatif, file konfigurasi tertentu dapat ditentukan dengan "docker-compose -f \<file konfigurasi\> up -d", yang memungkinkan pengaturan yang disesuaikan. Fleksibilitas ini mendukung pengujian sistematis di berbagai skenario. Kasus uji didefinisikan melalui berbagai file konfigurasi Docker Compose, yang masing-masing disesuaikan untuk mengevaluasi aspek tertentu dari sistem, seperti metode pemrosesan data paralel, mekanisme load balancing, orkestrasi multi-container, dan komunikasi berbasis WebSocket. Secara khusus, kasus uji yang menargetkan pemrosesan data paralel pada komponen data provider disusun untuk menilai kapasitas sistem dalam mengelola berbagai strategi penanganan data secara simultan. Skenario-skenario ini menyediakan lingkungan terkontrol untuk analisis komparatif dan evaluasi performa sistem di bawah berbagai kondisi arsitektural dan operasional. Kode sumber lengkap dan file konfigurasi tersedia di repositori GitHub resmi: <https://github.com/ArjunaWahyu/MDLBEEWS>.

4. **Dampak**

Pada bagian ini, kami menjelaskan tujuan optimisasi dan pengaturan eksperimen yang dirancang untuk mengevaluasi performa setiap komponen dalam EEWS kami. Tujuan kami adalah mengidentifikasi kombinasi teknologi yang paling efektif untuk meningkatkan kecepatan dan keandalan EEWS. Dengan mengevaluasi berbagai metode penyimpanan data, kerangka kerja komunikasi real-time, dan solusi manajemen data, kami bertujuan untuk mengoptimalkan performa sistem guna memastikan peringatan seismik yang tepat waktu dan akurat.

**Tabel 1.** Hasil Eksperimen Data Provider

| **Skenario** | **Keterlambatan Data (detik)** | **Penggunaan CPU (%)** | **Penggunaan Memori (MB)** | **Catatan** |
|---|---|---|---|---|
| Sequential | - | - | - | delay mulai 40 menit, terjadi crash |
| Multithreading | 3.150 | 31.24 | 112 | Crash terjadi ketika ada banyak thread |
| Multiprocessing | 2.955 | 44.50 | 476 | Stabil |
| Multiprocessing + Multithreading | 4.768 | 62.50 | 600 | Stabil |

Hasil, sebagaimana ditunjukkan pada Tabel 1, menunjukkan perbedaan signifikan antara model eksekusi, dengan metode Sequential dan Multithreading terbukti tidak stabil. Pada model Sequential, sistem mengalami delay startup yang panjang, yang pada akhirnya menyebabkan crash, kemungkinan besar disebabkan oleh ketidakmampuannya menangani tugas secara paralel secara efektif. Demikian pula, pendekatan Multithreading menjadi tidak stabil ketika jumlah thread ditingkatkan. Model shared memory yang digunakan dalam multithreading menyebabkan resource contention, yang mengakibatkan kegagalan sistem, khususnya saat menangani volume thread konkuren yang tinggi. Ketidakstabilan ini dapat dikaitkan dengan keterbatasan eksekusi paralel yang diberlakukan oleh Global Interpreter Lock (GIL), sebuah pembatasan pada banyak bahasa pemrograman yang menghambat paralelisme sejati dalam lingkungan multithreaded.

Di sisi lain, model Multiprocessing menunjukkan peningkatan yang signifikan, menawarkan solusi yang lebih stabil dengan latensi yang lebih rendah (2,955 detik) dan penggunaan sumber daya yang lebih efisien (44,50% CPU dan 476 MB memori). Pendekatan ini mendapat manfaat dari pengisolasian tugas dalam proses-proses terpisah, memungkinkan eksekusi paralel sejati tanpa masalah resource contention yang terjadi pada multithreading. Meskipun menggabungkan Multiprocessing dengan Multithreading semakin meningkatkan paralelisme, hal ini disertai trade-off berupa peningkatan konsumsi sumber daya dan kompleksitas yang lebih tinggi dalam mengelola proses dan thread secara bersamaan. Secara keseluruhan, model Multiprocessing terbukti menjadi pilihan paling stabil dan efisien untuk tugas yang diberikan.

**Tabel 2.** Hasil Eksperimen Message Broker

| **Skenario** | **Keterlambatan Data (detik)** | **Penggunaan CPU (%)** | **Penggunaan Memori (MB)** |
|---|---|---|---|
| Kafka 3 Container | 0.006329 | 27.24 | 3108 |
| Kafka 3 Container + nginx | 0.015902 | 25.68 | 2591 |

Dalam mengevaluasi perbedaan performa antara penggunaan Kafka sebagai message broker sekaligus load balancer versus pengintegrasian Kafka dengan NGINX sebagai load balancer khusus, muncul variasi yang nyata pada keterlambatan data, utilisasi CPU, dan konsumsi memori. Analisis menunjukkan bahwa ketika Kafka bertanggung jawab baik untuk pemesan-brokeran (message brokering) maupun load balancing, keterlambatan data yang teramati tetap lebih rendah, yang menunjukkan bahwa mekanisme partisi internal dan consumer group Kafka secara efisien mengelola distribusi pesan tanpa memerlukan lapisan routing tambahan. Namun, memperkenalkan NGINX sebagai load balancer eksternal menambahkan langkah pemrosesan tambahan, sehingga menyebabkan peningkatan keterlambatan data. Latensi tambahan ini kemungkinan besar muncul dari overhead yang terkait dengan penerusan permintaan, distribusi beban, dan interaksi antara Kafka dan NGINX sebelum pesan mencapai consumer yang dituju. Karakteristik performa ini ditunjukkan pada Tabel 2.

Terlepas dari variasi delay ini, utilisasi CPU tetap relatif stabil di kedua konfigurasi. Temuan ini menunjukkan bahwa load balancing internal Kafka tidak memberikan beban komputasi tambahan dibandingkan dengan setup alternatif menggunakan NGINX. Stabilitas dalam konsumsi CPU ini dapat dikaitkan dengan arsitektur Kafka yang dioptimalkan, yang dirancang untuk menangani pemrosesan pesan dengan throughput tinggi secara efisien. Hasil menunjukkan bahwa bahkan dengan diperkenalkannya load balancer eksternal, penggunaan CPU tidak berfluktuasi secara signifikan, yang memperkuat kemampuan Kafka dalam mengelola distribusi beban tanpa overhead komputasi yang berlebihan.

Namun, penggunaan memori menunjukkan perbedaan yang lebih mencolok antara kedua konfigurasi. Ketika Kafka berfungsi sebagai message broker sekaligus load balancer, konsumsi memori jauh lebih tinggi, yang mencerminkan sumber daya tambahan yang diperlukan untuk mengelola partisi, offset pesan, dan operasi load balancing internal. Sebaliknya, ketika NGINX diperkenalkan sebagai load balancer eksternal, konsumsi memori menurun, yang menunjukkan bahwa mengalihkan sebagian tugas penanganan permintaan klien ke NGINX meringankan beban memori pada Kafka. Redistribusi tugas-tugas yang intensif memori ini memungkinkan alokasi sumber daya sistem yang lebih efisien, khususnya pada skenario di mana keterbatasan memori menjadi pertimbangan kritis.

Temuan-temuan ini menggarisbawahi trade-off yang terkait dengan setiap konfigurasi. Meskipun mengandalkan Kafka saja untuk message brokering dan load balancing menghasilkan keterlambatan data yang lebih rendah, hal ini disertai biaya berupa konsumsi memori yang lebih tinggi. Sebaliknya, mengintegrasikan NGINX sebagai load balancer mengurangi penggunaan memori namun menambah latensi tambahan akibat lapisan pemrosesan tambahan. Pilihan di antara konfigurasi-konfigurasi ini pada akhirnya bergantung pada prioritas performa sistem, apakah mengoptimalkan latensi yang lebih rendah atau mengelola efisiensi sumber daya secara lebih efektif.

**Tabel 3.** Hasil Eksperimen Basis Data

| **Skenario** | **Waktu Proses (detik)** | **Penggunaan CPU (%)** | **Penggunaan Memori (MB)** |
|---|---|---|---|
| InfluxDB | 0.007740 | 32.91 | 433.92 |
| MongoDB | 0.004206 | 20.16 | 1925.22 |
| File Mseed | 0.023825 | None | None |

Analisis ini mengevaluasi efisiensi tiga solusi basis data untuk menyimpan dan mengambil data seismik. MongoDB memberikan performa terbaik dari segi waktu proses (0,0042 detik), sambil tetap mempertahankan penggunaan CPU yang relatif rendah (20,16%). Namun, konsumsi memorinya lebih tinggi (1925 MB), yang mencerminkan biaya dari kueri yang lebih cepat dan penanganan skema yang fleksibel. InfluxDB, meskipun sedikit lebih lambat (0,0077 detik), mengonsumsi lebih sedikit memori (433 MB), menawarkan opsi yang lebih ringan untuk data time-series, meski dengan biaya CPU yang lebih tinggi. File MSEED menunjukkan waktu proses paling lambat (0,0238 detik) dan tidak memiliki pemantauan sumber daya dalam setup ini. Format ini berguna untuk penyimpanan data mentah jangka panjang tetapi tidak efisien untuk tugas EEWS real-time karena kurangnya indexing dan kecepatan pengambilan yang lambat. Hasil ini menyoroti bahwa MongoDB menawarkan trade-off terbaik antara kecepatan dan penggunaan sumber daya untuk kebutuhan pemrosesan real-time, menjadikannya lebih sesuai untuk sistem EEWS yang memprioritaskan akses cepat dan fleksibilitas dalam penyimpanan data seismik. Hasil komparatif ini ditunjukkan pada Tabel 3, yang menyajikan hasil eksperimen Basis Data.

**Tabel 4.** Hasil Eksperimen Data Archiver

| **Skenario** | **Keterlambatan Data (detik)** | **Penggunaan CPU (%)** | **Penggunaan Memori (MB)** |
|---|---|---|---|
| 5 Container | 0.015763 | 197.90 | 518.59 |
| 4 Container | 0.015903 | 185.81 | 418.59 |
| 3 Container | 0.017323 | 173.48 | 321.34 |
| 2 Container | 0.018164 | 160.55 | 242.68 |
| 1 Container | 0.019274 | 150.37 | 151.34 |

Evaluasi performa eksekusi multi-container dalam pengarsipan data dan deteksi seismik menyoroti trade-off antara skalabilitas sistem, keterlambatan data, dan konsumsi sumber daya. Peningkatan jumlah container secara signifikan meningkatkan paralelisme dalam pemrosesan data, mengurangi latensi dan meningkatkan efisiensi sistem secara keseluruhan. Namun, peningkatan kecepatan ini disertai biaya berupa penggunaan CPU dan memori yang lebih tinggi, karena container tambahan memerlukan lebih banyak sumber daya komputasi untuk load balancing, transmisi data, dan penanganan permintaan. Pada sistem Data Archiver, peningkatan jumlah container menyebabkan pengurangan keterlambatan data yang nyata karena distribusi beban kerja yang lebih baik. Namun, penggunaan CPU tetap relatif tinggi, karena setiap container berkontribusi pada overhead pemrosesan. Selain itu, konsumsi memori meningkat seiring bertambahnya jumlah container, mencerminkan sumber daya tambahan yang diperlukan untuk mempertahankan beberapa instance. Meskipun pendekatan multi-container ini mengoptimalkan performa dan skalabilitas, hal ini juga menghadirkan tantangan untuk deployment di lingkungan dengan sumber daya terbatas, di mana menyeimbangkan kecepatan pemrosesan dan efisiensi sumber daya menjadi hal yang esensial. Tren performa ini ditunjukkan pada Tabel 4, yang menyajikan hasil eksperimen Data Archiver.

**Tabel 5.** Hasil Eksperimen P-Wave Detector

| **Skenario** | **Keterlambatan Data (detik)** | **Penggunaan CPU (%)** | **Penggunaan Memori (MB)** |
|---|---|---|---|
| 5 Container + fast API 2 Worker | 0.033676 | 192.14 | 20240 |
| 4 Container + fast API 2 Worker | 0.034843 | 177.18 | 19836 |
| 3 Container + fast API 2 Worker | 0.035214 | 162.55 | 18749 |
| 2 Container + fast API 2 Worker | 0.035951 | 157.21 | 17685 |
| 5 Container | 0.032647 | 280.00 | 16530 |
| 4 Container | 0.033197 | 257.94 | 15528 |
| 3 Container | 0.034010 | 228.17 | 14214 |
| 2 Container | 0.034936 | 195.73 | 13530 |

Tabel 5 menyajikan hasil eksperimen P-Wave Detector. Integrasi FastAPI dalam sistem deteksi P-Wave meningkatkan skalabilitas dengan mendistribusikan beban kerja secara efisien di berbagai container dan worker. Kemampuan pemrosesan asinkronnya memungkinkan sistem menangani banyak permintaan secara bersamaan, meningkatkan responsivitas dan throughput. Namun, pendekatan ini menambahkan lapisan pemrosesan tambahan, yang menyebabkan penggunaan CPU yang lebih tinggi dan keterlambatan data yang meningkat, yang dapat memengaruhi aplikasi yang sensitif terhadap latensi. Sebaliknya, mekanisme partisi internal dan consumer Kafka memungkinkan pemrosesan pesan dengan latensi rendah tanpa memerlukan lapisan routing tambahan. Dengan meminimalkan konsumsi CPU dan memori sambil mempertahankan throughput data yang tinggi, Kafka terbukti menjadi solusi yang lebih efisien untuk deteksi seismik real-time. Kemampuannya untuk memproses pesan dengan delay minimal menjadikannya sangat sesuai untuk aplikasi yang memprioritaskan deteksi kejadian gempa yang cepat dan andal.

Analisis ini menyoroti trade-off yang melekat dalam eksekusi multi-container untuk pengarsipan data dan deteksi seismik. Meskipun peningkatan jumlah instance container meningkatkan paralelisme dan skalabilitas, hal ini menyebabkan konsumsi sumber daya yang lebih tinggi. Pilihan arsitektur sistem bergantung pada kebutuhan performa spesifik, apakah memprioritaskan kecepatan dan efisiensi dengan Kafka atau memaksimalkan skalabilitas dengan FastAPI. Memahami trade-off ini sangat penting untuk mengoptimalkan deployment sistem berdasarkan sumber daya komputasi yang tersedia dan kebutuhan pemrosesan real-time.

**Tabel 6.** Hasil Eksperimen WebSocket

| **Skenario** | **Keterlambatan Data (detik)** | **Penggunaan CPU (%)** | **Penggunaan Memori (MB)** |
|---|---|---|---|
| Express JS 1 Client | 0.001324 | 12.02% | 95.49MB |
| Express JS 5 Client | 0.001452 | 13.38% | 96.05MB |
| Fast API 1 Client | 0.001356 | 17.71% | 72.67MB |
| Fast API 5 Client | 0.001578 | 39.05% | 72.97MB |

Eksperimen WebSocket mengevaluasi performa Express.js dan FastAPI dalam menangani komunikasi real-time pada berbagai beban klien. Hasil menunjukkan bahwa Express.js memberikan keterlambatan data yang lebih rendah dan penggunaan CPU yang lebih rendah dibandingkan FastAPI. Dengan delay 0,001324 detik dan penggunaan CPU 12,02% untuk satu klien, Express.js menangani koneksi WebSocket secara efisien dengan overhead sumber daya yang minimal. Bahkan dengan lima klien, sistem ini mempertahankan delay rendah sebesar 0,001452 detik, dengan hanya sedikit peningkatan penggunaan CPU (13,38%). Namun, penggunaan memori tetap relatif tinggi, berkisar antara 95,49 MB hingga 96,05 MB, yang menunjukkan bahwa Express.js memerlukan lebih banyak memori untuk koneksi konkuren.

Di sisi lain, FastAPI menunjukkan efisiensi memori yang lebih baik, hanya menggunakan 72,67 MB untuk satu klien dan 72,97 MB untuk lima klien. Namun, hal ini disertai biaya berupa penggunaan CPU yang lebih tinggi, khususnya saat menangani banyak klien. Meskipun delay-nya tetap kompetitif (0,001356 detik untuk satu klien dan 0,001578 detik untuk lima klien), penggunaan CPU meningkat secara signifikan, mencapai 39,05% saat menangani lima klien konkuren. Hal ini menunjukkan bahwa FastAPI lebih efisien secara memori tetapi mengonsumsi CPU secara signifikan lebih banyak seiring bertambahnya jumlah koneksi.

Express.js lebih sesuai untuk aplikasi real-time yang memprioritaskan latensi rendah dan konsumsi CPU yang berkurang, menjadikannya pilihan ideal untuk menangani koneksi WebSocket dengan konkurensi tinggi secara efisien [37]. Sebaliknya, FastAPI menawarkan efisiensi memori yang lebih baik namun dengan biaya penggunaan CPU yang jauh lebih tinggi seiring bertambahnya jumlah koneksi. Pemilihan antara kedua kerangka kerja ini harus didasarkan pada batasan sistem, apakah meminimalkan overhead CPU untuk skalabilitas dengan Express.js atau mengoptimalkan penggunaan memori dengan FastAPI untuk lingkungan dengan sumber daya terbatas. Temuan ini diperoleh dari Tabel 6, yang menyajikan hasil eksperimen WebSocket.

5. **Kesimpulan dan Keterbatasan**

Studi ini menyajikan analisis performa yang komprehensif terhadap pemrosesan data paralel, load balancing, eksekusi multi-container, dan implementasi WebSocket dalam lingkungan komputasi terdistribusi. Pendekatan Multiprocessing terbukti paling efisien untuk menangani tugas paralel, mencapai delay 2,955 detik, penggunaan CPU 44,50%, dan konsumsi memori 476 MB, sehingga sangat sesuai untuk pemrosesan real-time dalam Sistem Peringatan Dini Gempa Bumi (EEWS). Dalam message brokering, penggunaan Kafka saja menghasilkan keterlambatan data yang lebih rendah (0,006329 detik) namun dengan biaya penggunaan memori yang lebih tinggi, sementara pengintegrasian NGINX sebagai load balancer meningkatkan efisiensi memori tetapi sedikit meningkatkan latensi. Strategi eksekusi multi-container dalam pengarsipan data dan deteksi seismik meningkatkan skalabilitas sistem namun menimbulkan konsumsi CPU dan memori yang lebih tinggi, menyoroti trade-off antara kecepatan pemrosesan dan pemanfaatan sumber daya.

Untuk komunikasi real-time, Express.js menunjukkan latensi dan penggunaan CPU yang lebih rendah (12,02%), menjadikannya pilihan ideal untuk menangani koneksi WebSocket dalam EEWS, meskipun konsumsi memorinya lebih tinggi. FastAPI, di sisi lain, memberikan efisiensi memori yang lebih baik namun dengan biaya peningkatan penggunaan CPU, menjadikannya sesuai untuk lingkungan dengan keterbatasan memori. Berdasarkan temuan ini, optimisasi EEWS sebaiknya melibatkan pendekatan Multiprocessing untuk pemrosesan data paralel yang efisien, Kafka dengan NGINX untuk message brokering yang dapat diskalakan dan efisien, eksekusi multi-container untuk modularitas sistem yang lebih baik, serta Express.js untuk komunikasi WebSocket dengan latensi rendah, guna memastikan sistem deteksi dan peringatan gempa yang cepat, andal, dan efisien sumber daya, seperti kombinasi phase picking berbasis ML dan lokalisasi cepat yang ditunjukkan oleh Lian dkk. [38].

**Deklarasi Kepentingan yang Bersaing**

Tidak ada konflik kepentingan.

**Pernyataan Kontribusi Kepenulisan CRediT**

**Satriawan Rasyid Purnama**: Konseptualisasi, Analisis formal, Perangkat lunak, Penulisan – tinjauan & penyuntingan. **Adi Wibowo** (penulis korespondensi): Konseptualisasi, Supervisi, Administrasi proyek, Penulisan – tinjauan & penyuntingan, Kurasi data & protokol evaluasi, Validasi, Tinjauan domain. **Arjuna Wahyu Kusuma**: Penulisan – draf awal, Analisis formal, Perangkat lunak, Gambar/Visualisasi. **Liem Roy Marcelino**: Perangkat lunak, Kurasi data, Protokol evaluasi. **Indra Waspada**: Supervisi, Administrasi proyek. **Cecep Pratama**: Supervisi, Administrasi proyek. **Leni Sophia Heliani**: Validasi, Tinjauan domain. **David Prambudi Sahara**: Konseptualisasi. **Sri Widiyantoro**: Validasi, Tinjauan domain. **Shindy Rosalia**: Kurasi data, Protokol evaluasi. **Bondan Febriarta**: Perangkat lunak. **Cahyo Adhi Hartanto**: Perangkat lunak.

**Deklarasi Penggunaan AI Generatif dan Teknologi Berbantuan AI dalam Proses Penulisan**

Selama penyusunan karya ini, penulis menggunakan ChatGPT untuk meningkatkan kualitas bahasa dan keterbacaan. Setelah menggunakan alat/layanan ini, penulis meninjau dan menyunting konten sesuai kebutuhan serta bertanggung jawab penuh atas isi publikasi ini.

**Ucapan Terima Kasih**

Para penulis mengucapkan terima kasih kepada Badan Meteorologi, Klimatologi, dan Geofisika, Jakarta, Indonesia atas Data Seismik yang diberikan, serta kepada Direktorat Jenderal Pendidikan Tinggi, Riset, dan Teknologi dan Dikti AI Centre atas akses NVIDIA DGX A100. Penelitian ini didukung oleh Riset Publikasi Internasional Bereputasi Tinggi (RPIBT), Universitas Diponegoro, Indonesia, dengan Nomor Hibah 222-677/UN7.D2/PP/IV/2025.

**Referensi:**

*(Daftar referensi berikut dipertahankan dalam bahasa aslinya sesuai konvensi penulisan ilmiah, karena merujuk pada judul publikasi asli sumber yang dikutip.)*

[1] Liu M, Tan YJ. Evaluating the performance of machine-learning-based phase pickers when applied to ocean bottom seismic data: Blanco oceanic transform fault as a case study. arXiv preprint arXiv:2410.18041. 2024 Oct 23. <https://doi.org/10.1093/gji/ggaf256>

[2] Tunç S, Tunç B, Çaka D, Budakoğlu E. An Overview of Traditional and Next-Generation Earthquake Early Warning Systems. J Adv Res Nat Appl Sci. 2024;10(3):747–760. <https://doi.org/10.28979/jarnas.1481067>

[3] Kolivand H, Haghi Kashani M, Ekpanyapong M, Aghaei M, Banooni A, Akbarzadeh Khorshidi A, Haryanto H, Tarmizi MA, Shafie AA. A systematic review of Earthquake Early Warning (EEW) systems based on Artificial Intelligence. Sensors. 2024;24(19):6342. <https://doi.org/10.1007/s12145-024-01253-2>

[4] Zhang M, Liu M, Feng T, Wang R, Zhu W. LOC-FLOW: An End-to-End Machine Learning-Based High-Precision Earthquake Location Workflow. Seismol Res Lett. 2022;93(5):2426–2438. <https://doi.org/10.1785/0220220019>

[5] Zhu W, Hou AB, Yang R, Datta A, Mousavi SM, Ellsworth WL, Beroza GC. QuakeFlow: a scalable machine-learning-based earthquake monitoring workflow with cloud computing. Geophys J Int. 2022;232(1):684–693. <https://doi.org/10.1093/gji/ggac355>

[6] Naoi M, Tamaribuchi K, Shimojo K, Katoh S, Ohyanagi S. Neural phase picker trained on the Japan Meteorological Agency unified earthquake catalog. Earth, Planets and Space. 2024;76:150. <https://doi.org/10.1186/s40623-024-02091-8>

[7] Temneanu M.C., Donciu C., Serea E. Self-Contained Earthquake Early Warning System Based on Characteristic Period Computed in the Frequency Domain. Applied Sciences. 2025 Aug 15;15(16):9026. <https://doi.org/10.3390/app15169026>

[8] Carvalho L, Mohammadigheymasi H, Crocker P, Tavakolizadeh N, Moradichaleshtori Y, Fernandes R. Application of the pair-input deep learning model for seismicity reassessment in Cameroon. Acta Geophys. 2024. <https://doi.org/10.1007/s11600-024-01475-4>

[9] Ranasinghe V, Udara N, Mathotaarachchi M, Thenuwara T, Dias D, Prasanna R, Edirisinghe S, Gayan S, Holden C, Punchihewa A, Stephens M, Drummond P. Rapid and Resilient LoRa Leap: A Novel Multi-Hop Architecture for Decentralised Earthquake Early Warning Systems. Sensors. 2024 Sep 13;24(18):5960. <https://doi.org/10.3390/s24185960>

[10] Mousavi, S. M., & Ellsworth, W. L. (2025). Cloud-Native Deep Learning for Global Earthquake Detection. Frontiers in Earth Science, 13:155. <https://doi.org/10.3389/feart.2025.1432012>

[11] Justus D, Brennan J, Bonner S, McGough AS. Predicting the Computational Cost of Deep Learning Models. In: 2018 IEEE International Conference on Big Data (Big Data); 2018. p. 3873–82. <https://doi.org/10.1109/BigData.2018.8622396>

[12] Abdalzaher MS, Krichen M, Yiltas-Kaplan D, Ben Dhaou I, Adoni WYH. Early Detection of Earthquakes Using IoT and Cloud Infrastructure: A Survey. Sustainability. 2023;15(15):11713. <https://doi.org/10.3390/su151511713>

[13] Oluwasakin E, Torku T, Tingting S, Yinusa A, Hamdan S, Poudel S, Hasan N, Vargas J, Poudel K. Minimization of high computational cost in data preprocessing and modeling using MPI4Py. Mach Learn Appl. 2023;13:100483. <https://doi.org/10.1016/j.mlwa.2023.100483>

[14] Hosseini S.E. & Afza R. (2025). Early Warning Systems for Tsunami and Earthquake Disaster Management Using Data Science Techniques. Proc. IEEE Int. Conf. on Applied Electronics (AE 2025). <https://doi.org/10.1109/AE66163.2025.11197771>

[15] Harish M., Hemanth Kumar S., Banupriya S., Gowtham R., Rahul M.V. Enhancing Earthquake Prediction and Early Warning Systems Using CapsNet-BiLSTM Models. In: Proceedings of the 5th International Conference on Trends in Material Science and Inventive Materials (ICTMIM 2025). IEEE; 2025. p. 1734-1739. <https://doi.org/10.1109/ICTMIM65579.2025.10988387>

[16] Aziz ZA, Abdulqader DN, Sallow AB, Omer KH. Python Parallel Processing and Multiprocessing: A Review. Acad J Nawroz Univ. 2021;10(3):345–54. <https://doi.org/10.25007/ajnu.v10n3a1145>

[17] Yao Y, Jin H, Shah AD, Han S, Hu Z, Ran Y, Stripelis D, Xu Z, Avestimehr S, He C. ScaleLLM: A Resource-Frugal LLM Serving Framework by Optimizing End-to-End Efficiency. arXiv preprint arXiv:2408.00008. 2024.

[18] Cara Fabrizio; Cultrera Giovanna; Riccio Gaetano; Amoroso Sara; Bordoni Paola; Bucci Augusto; D'Alema Ezio; D'Amico Maria; Cantore Luciana; Carannante Simona; Cogliano Rocco; Di Giulio Giuseppe; Di Naccio Deborah; Famiani Daniela; Felicetta Chiara; Fodarella Antonio; Franceschina Gianlorenzo; Lanzano Giovanni; Lovati Sara; Luzi Lucia; Mascandola Claudia; Massa Marco; Mercuri Alessia; Milana Giuliano; Pacor Francesca; Piccarreda Davide; Pischiutta Marta; Pucillo Stefania; Puglia Rodolfo; Vassallo Maurizio; Boniolo Graziano; Caielli Grazia; Corsi Adelmo; de Franco Roberto; Tento Alberto; Bongiovanni Giovanni; Hailemikael Salomon; Martini Guido; Paciello Antonella; Peloso Alessandro; Poggi Fabrizio; Verrubbi Vladimiro; Gallipoli Maria Rosaria; Stabile Tony Alfredo; Mancini Marco. Temporary dense seismic network during the 2016 Central Italy seismic emergency for microzonation studies. Scientific Data. 2019; 6(1):182. <https://doi.org/10.1038/s41597-019-0188-1>

[19] Poulter AJ, Johnston SJ, Cox SJ. Using the MEAN stack to implement a RESTful service for an Internet of Things application. In: 2015 IEEE 2nd World Forum on Internet of Things (WF-IoT). 2015. p. 280–5. <https://doi.org/10.1109/WF-IoT.2015.7389066>

[20] Jamshidi P, Pahl C, Mendonça NC, Lewis J, Tilkov S. Microservices: The journey so far and challenges ahead. IEEE Software. 2018 May 4;35(3):24-35. <https://doi.org/10.1109/MS.2018.2141039>

[21] Hannousse A, Yahiouche S. Securing microservices and microservice architectures: A systematic mapping study. Computer Science Review. 2021 Aug 1;41:100415. <https://doi.org/10.1016/j.cosrev.2021.100415>

[22] Elhoseny M., Abdelhamid A. (2024). Microservice-Based Distributed Systems for Real-Time IoT Applications: Challenges and Trends. Future Internet, 16(3):105. <https://doi.org/10.3390/fi16030105>

[23] Beyreuther M, Barsch R, Krischer L, Megies T, Behr Y, Wassermann J. ObsPy: A Python Toolbox for Seismology. Seismol Res Lett. 2010;81(3):530–533. <https://doi.org/10.1785/gssrl.81.3.530>

[24] Krischer L, Megies T, Barsch R, Beyreuther M, Lecocq T, Caudron C, Wassermann J. ObsPy: A Bridge for Seismology into the Scientific Python Ecosystem. Comput Sci Discov. 2015;8(1):014003. <https://doi.org/10.1088/1749-4699/8/1/014003>

[25] Megies T, Beyreuther M, Barsch R, Krischer L, Wassermann J. ObsPy - What can it do for data centers and observatories? Ann Geophys. 2011;54(1):47–58. <https://doi.org/10.4401/ag-4838>

[26] Martín C, Langendoerfer P, Zarrin PS, Díaz M, Rubio B. Kafka-ML: Connecting the data stream with ML/AI frameworks. Future Gener Comput Syst. 2022;126:15–33. <https://doi.org/10.1016/j.future.2021.07.037>

[27] Zhu W, Wang J, Chen Q, Beroza GC. Early Earthquake Warning Using Artificial Intelligence: Recent Advances and Challenges. Geophys J Int. 2022;229(1):19–35. <https://doi.org/10.1093/gji/ggab473>

[28] Syafrudin M, Alfian G, Fitriyani NL, Rhee J. Performance Analysis of IoT-Based Sensor, Big Data Processing, and Machine Learning Model for Real-Time Monitoring System in Automotive Manufacturing. Sensors. 2018;18(9):2946. <https://doi.org/10.3390/s18092946>

[29] Wibowo A., Heliani L.S., Pratama C., Sahara D.P., Widiyantoro S., Ramdani D., Fuady B., Sudrajat A., Wibowo S.T., Rasyid Purnama S. Deep Learning for Real-Time P-Wave Detection: A Case Study in Indonesia's Earthquake Early Warning System. Applied Computing & Geosciences. 2024;24:100194. <https://doi.org/10.1016/j.acags.2024.100194>

[30] Song J, Kook J. Mapping Server Collaboration Architecture Design with OpenVSLAM for Mobile Devices. Appl Sci. 2022;12(7). <https://doi.org/10.3390/app12073653>

[31] Wibisono A, Rahmadika R N. Comparative Evaluation of Database Systems for High-Volume Seismic Prediction Data Management in Real-Time Applications. Jurnal Ilmu Komputer dan Informasi (JIKI). 2025 Jun;18(2):251-259. <https://doi.org/10.21609/jiki.v18i2.1530>

[32] Ma C, Chi Y. Evaluation test and improvement of load balancing algorithms of nginx. Ieee Access. 2022 Jan 26;10:14311-24. <https://doi.org/10.1109/ACCESS.2022.3146422>

[33] Kaviarasan R, Harikrishna P, Arulmurugan A. Load balancing in cloud environment using enhanced migration and adjustment operator based monarch butterfly optimization. Advances in Engineering Software. 2022 Jul 1;169:103128. <https://doi.org/10.1016/j.advengsoft.2022.103128>

[34] Ma L, Chi T. Performance Optimization in Apache Kafka for High-Throughput Event Processing. J Big Data. 2022;9(1):1–15. <https://doi.org/10.1186/s40537-022-00646-6>

[35] Raptis TP, Passarella A. Microservices Architecture Optimization for Real-Time Big Data Stream Analytics. Future Internet. 2022;14(11):333. <https://doi.org/10.3390/fi14110333>

[36] Hlayel M., Mahdin H., Aza Mohd Adam H. Latency Analysis of WebSocket and Industrial Protocols in Real-Time Digital Twin Integration. International Journal of Engineering Trends and Technology (IJETT). 2025 Jan;73(1):469-476. <https://doi.org/10.14445/22315381/IJETT-V73I1P110>

[37] Fernando L., Engel M.M. Comparative Performance Benchmarking of WebSocket Libraries on Node.js and Golang. SINKRON : Jurnal dan Penelitian Teknik Informatika. 2025; 9(4):2051-2060. <https://doi.org/10.33395/sinkron.v9i4.15266>

[38] Lian J-X, Liao W-Y, Lee E-J, Chen D-Y, Chen P. Integration of Machine Learning and Equal Differential Time Method for Enhanced Hypocenter Localization in Earthquake Early Warning Systems: Application to Dense Seismic Arrays in Taiwan. Earth, Planets and Space. 2024; 76:94. <https://doi.org/10.1186/s40623-024-02037-0>
