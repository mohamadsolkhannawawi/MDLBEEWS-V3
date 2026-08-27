# Roadmap Ekstraksi Pustaka — Urutan Prioritas untuk BAB II

> **Fungsi dokumen:** Daftar **39 pustaka** (27 paper empiris + 12 buku/paper teoretis) di BAB II, diurutkan dari **paling penting ke paling pelengkap**, sebagai panduan urutan menjalankan `prompt-ekstraksi-paper-sitasi.md`. Setiap pustaka yang sudah diekstrak disarankan disimpan sebagai `ekstraksi-[nama-penulis]-[tahun].md`, sesuai instruksi di prompt tersebut.
> **Cara pakai checklist:** centang `[x]` setelah file ekstraksi untuk pustaka itu selesai dibuat, supaya progres mudah dilacak.

---

## Fase 1 — Paling Kritis (5 pustaka)

Menentukan fondasi argumentasi utama skripsi: definisi observabilitas, pembanding empiris terdekat, metodologi pengujian, dan metodologi perancangan arsitektur. **Kerjakan ini lebih dulu sebelum yang lain**, karena hampir seluruh bab lain (I, III, IV, V) akan merujuk balik ke lima pustaka ini berulang kali.

- [ ] 1. Faseeha dkk. (2025) — *Observability in Microservices: An In-Depth Exploration of Frameworks, Challenges, and Deployment Paradigms* — paper
- [ ] 2. Wang dkk. (2025) — *Research on the Development of a Building Model Management System Integrating MQTT Sensing* — paper
- [ ] 3. Henning & Hasselbring (2024) — *Benchmarking Scalability of Stream Processing Frameworks Deployed as Microservices in the Cloud* — paper
- [ ] 4. Newman, S. (2021) — *Building Microservices: Designing Fine-Grained Systems* (2nd ed.) — **buku**
- [ ] 5. Sommerville, I. (2016) — *Software Engineering* (10th ed.) — **buku**

---

## Fase 2 — Pilar Teknis Inti (10 pustaka)

Menopang tiap sub bab teknis Dasar Teori (Kafka, WebSocket, NGINX, Microservices/Docker) secara langsung. Urutan mengikuti urutan kemunculan subbab di BAB II (2.2.2 → 2.2.5) agar sekalian bisa dipakai untuk mengecek/memperkaya draf yang sudah ada.

- [ ] 6. Al Qassem dkk. (2024) — *Containerized Microservices: A Survey of Resource Management Frameworks* — paper
- [ ] 7. Song & Kook (2022) — *Mapping Server Collaboration Architecture Design with OpenVSLAM for Mobile Devices* — paper
- [ ] 8. Raptis & Passarella (2023) — *A Survey on Networked Data Streaming with Apache Kafka* — paper
- [ ] 9. Raptis dkk. (2024) — *Efficient Topic Partitioning of Apache Kafka for High-Reliability Real-Time Data Streaming Applications* — paper
- [ ] 10. Martín dkk. (2022) — *Kafka-ML: Connecting the Data Stream with ML/AI Frameworks* — paper
- [ ] 11. Chodorek & Chodorek (2025) — *Web Real-Time Communications-Based Unmanned-Aerial-Vehicle-Borne Internet of Things and Stringent Time Sensitivity: A Case Study* — paper
- [ ] 12. Ma & Chi (2022) — *Evaluation Test and Improvement of Load Balancing Algorithms of Nginx* — paper
- [ ] 13. Nguyen dkk. (2022) — *Load-Balancing of Kubernetes-Based Edge Computing Infrastructure Using Resource Adaptive Proxy* — paper
- [ ] 14. Usman dkk. (2022) — *A Survey on Observability of Distributed Edge & Container-Based Microservices* — paper
- [ ] 15. Tzanettis dkk. (2022) — *Data Fusion of Observability Signals for Assisting Orchestration of Distributed Applications* — paper

---

## Fase 3 — Buku Notasi Pemodelan dan Rekayasa Perangkat Lunak (5 buku)

Baru dibutuhkan mendalam saat mulai menulis **Bab III** (diagram arsitektur, *sequence diagram*, *flowchart*, DFD) — boleh dikerjakan belakangan setelah Fase 1–2, tapi tetap sebelum mulai menggambar diagram Bab III supaya ada pedoman visual yang benar.

- [ ] 16. Fowler, M. (2004) — *UML Distilled: A Brief Guide to the Standard Object Modeling Language* (3rd ed.) — **buku**
- [ ] 17. Booch, G., Rumbaugh, J., & Jacobson, I. (2005) — *The Unified Modeling Language User Guide* (2nd ed.) — **buku**
- [ ] 18. Brown, S. (2022) — *The C4 Model for Visualising Software Architecture* — **buku** (Leanpub)
- [ ] 19. Kendall, K. E., & Kendall, J. E. (2011) — *Systems Analysis and Design* (8th ed.) — **buku**
- [ ] 20. Pressman, R. S., & Maxim, B. R. (2014) — *Software Engineering: A Practitioner's Approach* (8th ed.) — **buku**

---

## Fase 4 — Buku Framework & Teknologi Implementasi (5 buku + 1 paper)

Mendukung Sub Bab 2.2.7 yang isinya sudah tertulis di draf — ekstraksi di fase ini sifatnya **verifikasi dan pengayaan**, bukan kebutuhan mendesak, karena kontennya sudah cukup lengkap. Prioritas rendah dibanding Fase 1–3.

- [ ] 21. Abadi dkk. (2016) — *TensorFlow: A System for Large-Scale Machine Learning* — paper
- [ ] 22. Beyreuther dkk. (2010) — *ObsPy: A Python Toolbox for Seismology* — paper
- [ ] 23. Lubanovic, B. (2024) — *FastAPI: Modern Python Web Development* — **buku**
- [ ] 24. Casciaro, M., & Mammino, L. (2020) — *Node.js Design Patterns* (3rd ed.) — **buku**
- [ ] 25. Chodorow, K. (2013) — *MongoDB: The Definitive Guide* (2nd ed.) — **buku**

---

## Fase 5 — Anchor Domain EEWS (6 pustaka)

Menopang Latar Belakang Bab I dan Sub Bab 2.2.1 (definisi & prinsip kerja EEWS). Penting untuk kelengkapan argumentasi domain, tetapi tidak menyentuh kontribusi utama (observabilitas) secara langsung, sehingga prioritasnya di bawah Fase 1–3.

- [ ] 26. Kolivand dkk. (2024) — *A Systematic Review of Earthquake Early Warning (EEW) Systems Based on Artificial Intelligence* — paper
- [ ] 27. Zhu dkk. (2023) — *QuakeFlow: A Scalable Machine-Learning-Based Earthquake Monitoring Workflow with Cloud Computing* — paper
- [ ] 28. Wibowo dkk. (2024) — *Deep Learning for Real-Time P-Wave Detection: A Case Study in Indonesia's Earthquake Early Warning System* — paper
- [ ] 29. M. Zhang dkk. (2022) — *LOC-FLOW: An End-to-End Machine Learning-Based High-Precision Earthquake Location Workflow* — paper
- [ ] 30. Ranasinghe dkk. (2024) — *Rapid and Resilient LoRa Leap: A Novel Multi-Hop Architecture for Decentralised Earthquake Early Warning Systems* — paper
- [ ] 31. Melgarejo-Hernández dkk. (2026) — *Near-Real-Time Integration of Multi-Source Seismic Data* — paper

---

## Fase 6 — Pelengkap/Tangensial (8 paper, opsional)

Cukup disebut sekilas di narasi (lihat `daftar-paper-wajib-dibahas.md` Bagian 3) — **ekstraksi lengkap opsional**. Jika waktu terbatas, cukup jalankan Bagian I (sitasi) dan II (ringkasan) dari prompt, lewati Bagian VI (gambar) karena tidak direncanakan sebagai basis diagram.

- [ ] 32. Liu & Tan (2025) — *Evaluating the Performance of Machine-Learning-Based Phase Pickers When Applied to Ocean Bottom Seismic Data* — paper
- [ ] 33. Carvalho dkk. (2025) — *Application of the Pair-Input Deep Learning Model for Seismicity Reassessment in Cameroon* — paper
- [ ] 34. Temneanu dkk. (2025) — *Self-Contained Earthquake Early Warning System Based on Characteristic Period Computed in the Frequency Domain* — paper
- [ ] 35. Naoi dkk. (2024) — *Neural Phase Picker Trained on the Japan Meteorological Agency Unified Earthquake Catalog* — paper
- [ ] 36. Lian dkk. (2024) — *Integration of Machine Learning and Equal Differential Time Method for Enhanced Hypocenter Localization in Earthquake Early Warning Systems: Application to Dense Seismic Arrays in Taiwan* — paper
- [ ] 37. Oluwasakin dkk. (2023) — *Minimization of High Computational Cost in Data Preprocessing and Modeling Using MPI4Py* — paper
- [ ] 38. Abdalzaher dkk. (2023) — *Early Detection of Earthquakes Using IoT and Cloud Infrastructure: A Survey* — paper
- [ ] 39. Häusler dkk. (2022) — *Monitoring the Changing Seismic Site Response of a Fast-Moving Rockslide (Brienz/Brinzauls, Switzerland)* — paper

---

## Ringkasan

| Fase | Isi | Jumlah | Prioritas |
|---|---|---|---|
| 1 | Paling kritis (observabilitas, pembanding, metodologi) | 5 | 🔴 Tertinggi — kerjakan lebih dulu |
| 2 | Pilar teknis inti (Kafka, WebSocket, NGINX, Microservices) | 10 | 🟠 Tinggi |
| 3 | Buku notasi pemodelan (dibutuhkan saat mulai Bab III) | 5 | 🟡 Sedang, tapi sebelum menggambar diagram |
| 4 | Buku framework implementasi (verifikasi/pengayaan) | 6 | 🟢 Rendah, konten sudah ada |
| 5 | Anchor domain EEWS | 6 | 🟢 Rendah–sedang |
| 6 | Pelengkap/tangensial | 8 | ⚪ Opsional |
| **Total** | | **39** | |

**Catatan penting soal buku (Fase 1, 3, 4):** untuk pustaka berformat **buku** (bukan paper jurnal/prosiding), file yang dilampirkan ke prompt biasanya berupa **bab/chapter relevan saja** (mis. Bab "Splitting the Monolith" dari buku Newman, atau Bab "Sequence Diagram" dari Fowler) — bukan seluruh buku sekaligus, karena satu buku bisa ratusan halaman dan tidak semuanya relevan. Pilih bab yang isinya paling langsung menopang subbab yang bersangkutan sebelum menjalankan prompt ekstraksi.
