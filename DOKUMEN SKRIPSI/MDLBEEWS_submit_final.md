# *MDLBEEWS: Modular Deep Learning Based Earthquake Early Warning System*

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

*^a^Department of Informatics, Universitas Diponegoro, Semarang, Indonesia*

*^b^Department of Geodetic Engineering, Universitas Gadjah Mada, Yogyakarta, Indonesia*

*^c^Global Geophysics Research Group, Faculty of Mining and Petroleum Engineering, Institute of Technology Bandung, Bandung, Indonesia*

*^d^Faculty of Computer Science, Universitas Indonesia, Depok, Indonesia*

^\*^Corresponding author

## Abstract

*MDLBEEWS is an optimized Earthquake Early Warning System (EEWS) that leverages deep learning for accurate and timely earthquake predictions. With a modular architecture and Docker containerization, it ensures easy deployment and scalability. The system integrates multiprocessing for efficient data processing and uses Kafka with NGINX to minimize data delay. WebSocket communication facilitates immediate alert dissemination. Designed for use by geophysics researchers, disaster management agencies, and technology developers, the system delivers improved performance, scalability, and resource efficiency, addressing critical limitations in current EEWS implementations.*

## Keywords

*Earthquake Early Warning System, Deep Learning, Real-time Seismic Data Processing, Containerized Deployment, WebSocket-based Alert Dissemination*

## Code metadata

| **Nr** | **Code metadata description** | **Please fill in this column** |
|---|---|---|
| C1 | Current code version | *v1.0* |
| C2 | Permanent link to code/repository used for this code version | *<https://github.com/ArjunaWahyu/paper-eews.git>* |
| C3 | Permanent link to reproducible capsule | <https://codeocean.com/capsule/xxxxxx/tree/v1> |
| C4 | Legal code license | *MIT License* |
| C5 | Code versioning system used | *git* |
| C6 | Software code languages, tools and services used | *Python and JavaScript* |
| C7 | Compilation requirements, operating environments and dependencies | *Python \>= 3.7,* *TensorFlow \>= 2.10, Docker, ObsPy, Kafka, FastAPI, Websockets* |
| C8 | If available, link to developer documentation/manual | *<https://github.com/ArjunaWahyu/paper-eews/blob/main/README.md>* |
| C9 | Support email for questions | *<bowo.adi@live.undip.ac.id>* |

1. **Introduction**

Providing rapid alerts during the initial moments of an earthquake is critical to reducing potential damage and casualties. Earthquake Early Warning Systems (EEWS) were originally reliant on manual detection of seismic waves but have since evolved recentsuh techniques such as STA/LTA and match filtering [1,2]. Recent systematic reviews also confirm that AI-based models, particularly neural and probabilistic approaches, significantly improve EEW accuracy and responsiveness [3]. However, these methods still face challenges in accuracy and efficiency. Recent innovations include machine learning-based workflows such as PhaseNet, PickNet, and systems like LOC-FLOW and QuakeFlow, which integrate deep learning with cloud computing to enhance speed and detection capabilities [4,5,6]. Recent developments also demonstrate the feasibility of fully self-contained EEW systems using MEMS accelerometers and microcontrollers for spectral-based detection [7].

Several open-source and research-based EEWS software platforms have been developed, such as SeisComP, Earthworm, ElarmS, and PRESTo. While these systems are valuable, most are either designed for centralized infrastructure or lack flexibility for integration with modern cloud-based, deep learning-enabled workflows [8,9].

QuakeFlow exemplifies an advanced EEWS architecture, combining real-time data streaming via Kafka, scalable containerization with Docker and Kubernetes, and internal communication with FastAPI [10]. It supports both archived and real-time seismic data, offering flexibility and scalability [5]. Despite these advances, the use of deep learning and distributed processing introduces high computational costs and latency issues [2,11–13]. Machine learning-based systems, such as decision tree classifiers, have demonstrated high predictive accuracy (up to 95%) for early disaster detection [14], reinforcing the feasibility of integrating lightweight AI components into modular EEWS architectures to balance accuracy and efficiency. Hybrid deep learning models combining CapsNet and LSTM have shown outstanding predictive performance, achieving up to 95.6% accuracy for earthquake prediction tasks [15], which supports the effectiveness of integrating similar AI modules in modular EEWS frameworks.

In this study, we develop a cloud-based EEWS software prototype aimed at optimizing real-time seismic data processing and alert dissemination. The system integrates multiprocessing for parallel data ingestion [16,17], NGINX-based load balancing for efficient distribution [18], modular multi-container execution for scalability, and Express.js for low-latency WebSocket communication [19]. This work contributes a modular, efficient, and scalable EEWS software architecture that addresses existing performance limitations and offers compatibility with current and future machine learning-based detection models.

2. **Software Description**

**[Gambar: Diagram Arsitektur EEWS yang Diusulkan]** — Deskripsi gambar: Diagram alur sistem berjudul "Earthquake Early Warning System" berbentuk kotak besar dengan rounded corner berisi enam modul: Data Provider, Message Broker, Data Archiver, Database (silinder), P Wave Detector, Location Magnitude Detector, dan WebSocket. Di luar kotak besar, sebuah ikon awan bertuliskan "Seedlink" mengalir masuk ke Data Provider, dan sebuah kotak "Frontend" berada di sisi kanan yang terhubung dengan WebSocket. Panah-panah berwarna menunjukkan jenis aliran data: merah untuk "Waveform Data", biru untuk "P Wave Data", hijau untuk "Location Magnitude Data", garis putus-putus hitam untuk "Request", dan garis hitam penuh untuk "Response". Data Provider mengalir ke Message Broker; Message Broker terhubung ke Data Archiver (yang mengalir ke Database), ke P Wave Detector, ke Location Magnitude Detector, dan ke WebSocket; WebSocket saling bertukar data dengan Database serta dengan Frontend.

> **Fig 1.** Proposed EEWS Architecture

**2.1. EEWS Architecture**

In this study, an Earthquake Early Warning System (EEWS) is developed using a modular and independent framework as illustrated in Fig. 1. receopts a microservices architecture, in which each module, data ingestion, real-time detection, message handling, storage, and notification operates as an independent service with defined network interfaces, enhancing system flexibility and scalability [20,21,22]. This architectural pattern supports efficient development and maintenance of distributed and complex applications, particularly suited for real-time seismic processing. Key technologies include ObsPy for seismic data processing [23–25], Apache Kafka for message streaming [26], TensorFlow for deploying deep learning models [27], and MongoDB as a backend database solution [28]. This architecture aims to reduce earthquake alert latency and ensure timely, reliable warnings [21].

**2.2. EEWS Modules**

The proposed Earthquake Early Warning System (EEWS) is architecturally organized into several specialized modules that communicate via Kafka, allowing for flexible scaling and efficient real-time processing. Each module fulfills a critical role in the end-to-end detection and alert pipeline.

- **Data Provider**, the system begins with the Data Provider module, which is responsible for ingesting real-time seismic data streams via SeedLink using ObsPy. This component emphasizes low-latency and low-resource data flow by immediately converting incoming seismic traces into standardized JSON format. These are then published to specific Kafka topics, such as trace_topic, enabling consistent and uniform data availability for downstream modules. This standardization is a crucial requirement for real-time EEWS performance [11].

- **P-Wave Detector**, this module applies a deep learning model with multiple convolutional layers to detect the onset of P-waves [29]. Implemented with TensorFlow and served through FastAPI, this module offers high-speed inference with minimal delay. FastAPI is selected for its asynchronous request handling and seamless integration with machine learning frameworks, facilitating fast and reliable phase detection—an essential capability for issuing timely warnings [30].

- **Message Broker**, a central component in the architecture which functions as a distributed message broker utilizing a publish/subscribe pattern. Kafka handles real-time data transmission between containers by organizing information into topics, trace_topic for waveform data, p_wave_topic for pick detections, and result_topic for output from the location-magnitude detector. This approach supports parallel processing by multiple consumers and ensures robust data distribution throughout the EEWS pipeline [26].

- **Data Archiver and Databases**, to ensure long-term data availability, a Data Archiver module subscribes to waveform streams and stores them in a persistent backend. The system employs MongoDB, a flexible NoSQL document database, which excels at storing unstructured seismic data and supporting high-speed I/O operations. Its dynamic schema and advanced indexing capabilities make it ideal for storing and retrieving waveform information in time-critical environments [28, 31].

- **Location and Magnitude Detector**, this module estimates key earthquake parameters namely the hypocenter and magnitude based on the detected P-waves. It also leverages TensorFlow and outputs results to the result_topic in Kafka. Its modular design supports later integration of alternative algorithms or more complex models for enhanced precision, offering flexibility for continuous system evolution.

- **WebSocket and Frontend**, the system includes a WebSocket service that listens to Kafka topics and relays real-time data to the frontend. This allows for instant updates of seismic waveforms, detection outputs, and earthquake parameters in client interfaces. Whether built with Express.js, FastAPI, or other frameworks, the frontend can dynamically render seismograms and display warning messages, ensuring users receive immediate situational awareness [19].

**[Gambar: Arsitektur Data Provider yang Diusulkan]** — Deskripsi gambar: Diagram terdiri dari empat panel berlabel a) Sequential, b) Multithreading, c) Multiprocessing, dan d) Multiprocessing + Multithreading, yang membandingkan empat strategi eksekusi modul Data Provider. Panel (a) menunjukkan alur sederhana Seedlink → Data Provider (Main Process, ObsPy) → Kafka. Panel (b) menunjukkan Data Provider dengan Main Process yang men-spawn beberapa Thread (Thread 1, Thread 2, Thread 3, ..., Thread n) yang masing-masing menerima data dari Seedlink dan mengirim ke Kafka. Panel (c) serupa dengan (b) tetapi Main Process men-spawn beberapa Process (Process 1, Process 2, Process 3, ..., Process n) alih-alih thread. Panel (d) menggabungkan keduanya: Main Process men-spawn beberapa Process, dan setiap Process kembali men-spawn beberapa Thread, seluruhnya menerima data dari Seedlink dan mengalirkan hasilnya ke Kafka.

> **Figure 2.** Proposed Data Provider Architecture
>
> **[Gambar: Arsitektur Message Broker yang Diusulkan dengan NGINX]** — Deskripsi gambar: Diagram menunjukkan Data Provider yang mengirim data ke sebuah "Kafka Cluster" berisi tiga node (Kafka 1, Kafka 2, Kafka 3). Kafka 1 terhubung ke Load Balancer yang meneruskan data ke beberapa instance Data Archiver (Data Archiver 1, Data Archiver 2, ..., Data Archiver N). Kafka 2 terhubung ke WebSocket. Kafka 3 terhubung ke Location Magnitude Detector serta ke Load Balancer lain yang mendistribusikan data ke beberapa instance P Wave Detector (P Wave Detector 1, P Wave Detector 2, ..., P Wave Detector N). Legenda menunjukkan tiga jenis garis: garis merah penuh untuk "All Chennel Waveform Data", garis merah putus-putus untuk "Z Chennel Waveform Data", dan garis biru untuk "P Wave Data".
>
> **Figure 3.** Proposed Message Broker Architecture with NGINX.

**2.3. Optimization**

The performance evaluation of the proposed Earthquake Early Warning System (EEWS) focuses on identifying the most effective technological combination to optimize real-time data processing and reduce system latency. Several optimization components were developed and tested under various scenarios to assess their impact on key performance metrics: CPU usage, memory usage, and data delay. The evaluation was conducted using 500-sample trials for each test case, with resource monitoring via Docker Desktop. The experimental modules are as follows:

- **Multithreaded and Multiprocessing**, The Data Provider module was tested using four execution strategies: sequential, multithreaded, multiprocessing, and a hybrid of multithreaded + multiprocessing. The baseline sequential mode processes seismic waveform data one-by-one on a single thread, often resulting in high latency and instability under load. The multithreaded approach increases throughput by enabling concurrent operations within a single process [17]. Multiprocessing leverages multiple independent processes distributed across CPU cores to improve scalability and performance [16]. The hybrid model combines both techniques, distributing tasks across multiple threads and processes, offering optimized resource utilization across CPU, memory, and delay. The architectural details of each approach are illustrated in Fig. 2.

- **Configurated Kafka with NGINX**, In this configuration, as shown in Fig. 3, Kafka serves as the message broker for real-time waveform distribution. To enhance data throughput and support scalable processing, Kafka is deployed with three brokers and partitioned topics (trace_topic, p_wave_topic, result_topic), enabling parallel consumption by components such as Data Archivers and P-Wave Detectors. To bolster throughput and high availability, the system may employ three Kafka brokers alongside NGINX, which can function as a reverse proxy and load balancer [32]. By incorporating NGINX as a load balancer, the system can effectively distribute client requests, reducing bottlenecks and improving the efficiency of the data flow [33]. This configuration maximizes throughput, minimizes delay, and reduces performance bottlenecks under high traffic [34–36].

- **Multicontainer**, To further improve system responsiveness, the Data Archiver and P-Wave Detector modules were scaled using multi-container setups. In the test, the Data Archiver was deployed using 1 to 5 containers. This allowed parallel storage operations, reducing bottlenecks and increasing system throughput. The multi-container design improves both the speed and scalability of seismic data handling, ensuring rapid availability of waveforms for further processing.

- **Express.js**, The WebSocket module is responsible for relaying real-time seismic data including waveforms, location, and magnitude to the frontend interface. Two frameworks were evaluated: FastAPI and Express.js. While FastAPI offers tight integration with Python-based inference pipelines and efficient async handling [30], Express.js, built on Node.js's event-driven architecture, demonstrates superior performance in managing high volumes of simultaneous WebSocket connections. Express.js reduces CPU usage while maintaining responsiveness in data broadcasting [19]. Each framework has trade-offs depending on the expected traffic and ecosystem alignment.

3. **Example**

To execute the system, users are advised to utilize Docker Compose, which facilitates container orchestration in a streamlined and reproducible manner. The system can be initiated in detached mode using the command "docker-compose up -d", enabling background execution. Alternatively, a specific configuration file can be specified with "docker-compose -f \<configuration file\> up -d", allowing for customized setups. This flexibility supports systematic testing across multiple scenarios. The test cases are defined through various Docker Compose configuration files, each tailored to evaluate particular aspects of the system, such as parallel data processing methods, load balancing mechanisms, multi-container orchestration, and WebSocket-based communication. In particular, the test cases targeting parallel data processing on the data provider component are structured to assess the system's capacity to simultaneously manage diverse data handling strategies. These scenarios offer a controlled environment for comparative analysis and performance evaluation of the system under different architectural and operational conditions. The complete source code and configuration files are available at the official GitHub repository: <https://github.com/ArjunaWahyu/MDLBEEWS>.

4. **Impact**

In this section, we describe the optimization goal and experimental setup designed to evaluate the performance of each component in our EEWS. Our goal is to identify the most effective combination of technologies for enhancing the speed and reliability of EEWS. By evaluating various data storage methods, real-time communication frameworks, and data management solutions, we aim to optimize the system's performance to ensure timely and accurate seismic warnings.

**Table 1.** Data Provider Experiment Result

| **Scenario** | **Data Delay (seconds)** | **CPU Usage (%)** | **Memory Usage (MB)** | **Note** |
|---|---|---|---|---|
| Sequential | - | - | - | 40 minutes delay start, crash occurs |
| Multithreading | 3.150 | 31.24 | 112 | Crash occurs when there are many threads |
| Multiprocessing | 2.955 | 44.50 | 476 | Stable |
| Multiprocessing + Multithreading | 4.768 | 62.50 | 600 | Stable |

The results, as shown in Table 1, indicate significant differences between the execution models, with Sequential and Multithreading methods proving unstable. In the Sequential model, the system faces a long startup delay, ultimately leading to a crash, likely due to its inability to handle tasks in parallel effectively. Similarly, the Multithreading approach becomes unstable when scaling up the number of threads. The shared memory model used in multithreading causes resource contention, resulting in system failure, particularly when handling a high volume of concurrent threads. This instability can be attributed to limitations in parallel execution imposed by the Global Interpreter Lock (GIL), a restriction in many programming languages that hinders true parallelism in multithreaded environments.

On the other hand, the Multiprocessing model shows a marked improvement, offering a more stable solution with lower latency (2.955 seconds) and more efficient resource usage (44.50% CPU and 476 MB of memory). This approach benefits from isolating tasks in separate processes, allowing for true parallel execution without the resource contention issues seen in multithreading. Although combining Multiprocessing with Multithreading further enhances parallelism, it comes with the trade-off of increased resource consumption and higher complexity in managing both processes and threads. Overall, the Multiprocessing model proves to be the most stable and efficient choice for the given task.

**Table 2.** Message Broker Experiment Result

| **Scenario** | **Data Delay (seconds)** | **CPU Usage (%)** | **Memory Usage (MB)** |
|---|---|---|---|
| Kafka 3 Container | 0.006329 | 27.24 | 3108 |
| Kafka 3 Container + nginx | 0.015902 | 25.68 | 2591 |

In evaluating the performance differences between using Kafka as both a message broker and load balancer versus integrating Kafka with NGINX as a dedicated load balancer, notable variations emerge across data delay, CPU utilization, and memory consumption. The analysis indicates that when Kafka is responsible for both message brokering and load balancing, the observed data delay remains lower, suggesting that Kafka's internal partitioning and consumer group mechanisms efficiently manage message distribution without the need for additional routing layers. However, introducing NGINX as an external load balancer introduces additional processing steps, leading to an increase in data delay. This additional latency likely arises from the overhead associated with request forwarding, load distribution, and interaction between Kafka and NGINX before messages reach their designated consumers. These performance characteristics are shown in Table 2.

Despite these variations in delay, CPU utilization remains relatively stable across both configurations. The findings suggest that Kafka's internal load balancing does not impose additional computational strain compared to the alternative setup with NGINX. This stability in CPU consumption can be attributed to Kafka's optimized architecture, which is designed to handle high-throughput message processing efficiently. The results indicate that even with the introduction of an external load balancer, CPU usage does not fluctuate significantly, reinforcing Kafka's ability to manage load distribution without excessive computational overhead.

However, memory usage exhibits a more pronounced difference between the two configurations. When Kafka functions as both the message broker and load balancer, memory consumption is notably higher, reflecting the additional resources required to manage partitioning, message offsets, and internal load balancing operations. In contrast, when NGINX is introduced as an external load balancer, memory consumption decreases, suggesting that offloading certain client request handling tasks to NGINX alleviates the memory burden on Kafka. This redistribution of memory-intensive tasks allows for a more efficient allocation of system resources, particularly in scenarios where memory constraints are a critical consideration.

These findings underscore the trade-offs associated with each configuration. While relying solely on Kafka for both message brokering and load balancing results in lower data delay, it comes at the cost of higher memory consumption. Conversely, integrating NGINX as a load balancer reduces memory usage but introduces additional latency due to the added processing layer. The choice between these configurations ultimately depends on the system's performance priorities, whether optimizing for lower latency or managing resource efficiency more effectively.

**Table 3.** Databases Experiment Result

| **Scenario** | **Process Time (seconds)** | **CPU Usage (%)** | **Memory Usage (MB)** |
|---|---|---|---|
| InfluxDB | 0.007740 | 32.91 | 433.92 |
| MongoDB | 0.004206 | 20.16 | 1925.22 |
| File Mseed | 0.023825 | None | None |

This analysis evaluates the efficiency of three database solutions for storing and retrieving seismic data. MongoDB delivers the best performance in terms of process time (0.0042s), while also maintaining relatively low CPU usage (20.16%). However, its memory consumption is higher (1925 MB), reflecting the cost of faster querying and flexible schema handling. InfluxDB, while slightly slower (0.0077s), consumes less memory (433 MB), offering a more lightweight option for time-series data, albeit with a higher CPU cost. File MSEED shows the slowest process time (0.0238s) and lacks resource monitoring in this setup. This format is useful for long-term raw data storage but is inefficient for real-time EEWS tasks due to lack of indexing and slow retrieval speed. These results highlight that MongoDB offers the best trade-off between speed and resource usage for real-time processing needs, making it more suitable for EEWS systems that prioritize rapid access and flexibility in seismic data storage. These comparative outcomes are shown in Table 3, which presents the Databases experiment results.

**Table 4.** Data Archiver Experiment Result

| **Scenario** | **Data Delay (seconds)** | **CPU Usage (%)** | **Memory Usage (MB)** |
|---|---|---|---|
| 5 Container | 0.015763 | 197.90 | 518.59 |
| 4 Container | 0.015903 | 185.81 | 418.59 |
| 3 Container | 0.017323 | 173.48 | 321.34 |
| 2 Container | 0.018164 | 160.55 | 242.68 |
| 1 Container | 0.019274 | 150.37 | 151.34 |

The performance evaluation of multi-container execution in data archiving and seismic detection highlights the trade-offs between system scalability, data delay, and resource consumption. Increasing the number of containers significantly enhances parallelism in data processing, reducing latency and improving overall system efficiency. However, this improvement in speed comes at the cost of higher CPU and memory usage, as additional containers require more computational resources for load balancing, data transmission, and request handling. In the Data Archiver system, increasing the number of containers leads to a noticeable reduction in data delay due to improved workload distribution. However, CPU usage remains relatively high, as each container contributes to processing overhead. Additionally, memory consumption increases with the number of containers, reflecting the additional resources required to maintain multiple instances. While this multi-container approach optimizes performance and scalability, it also presents challenges for deployment in resource-constrained environments where balancing processing speed and resource efficiency is essential. These performance trends are shown in Table 4, which presents the Data Archiver experiment results.

**Table 5.** P-Wave Detector Experiment Result

| **Scenario** | **Data Delay (seconds)** | **CPU Usage (%)** | **Memory Usage (MB)** |
|---|---|---|---|
| 5 Container + fast API 2 Worker | 0.033676 | 192.14 | 20240 |
| 4 Container + fast API 2 Worker | 0.034843 | 177.18 | 19836 |
| 3 Container + fast API 2 Worker | 0.035214 | 162.55 | 18749 |
| 2 Container + fast API 2 Worker | 0.035951 | 157.21 | 17685 |
| 5 Container | 0.032647 | 280.00 | 16530 |
| 4 Container | 0.033197 | 257.94 | 15528 |
| 3 Container | 0.034010 | 228.17 | 14214 |
| 2 Container | 0.034936 | 195.73 | 13530 |

Table 5 presents the P-Wave Detector experiment results. The integration of FastAPI in the P-Wave detection system enhances scalability by efficiently distributing workloads across multiple containers and workers. Its asynchronous processing capabilities allow the system to handle numerous requests simultaneously, improving responsiveness and throughput. However, this approach introduces additional processing layers, leading to higher CPU usage and increased data delay, which may impact latency-sensitive applications. In contrast, Kafka's internal partitioning and consumer mechanisms enable low-latency message processing without the need for additional routing layers. By minimizing CPU and memory consumption while maintaining high data throughput, Kafka proves to be a more efficient solution for real-time seismic detection. Its ability to process messages with minimal delay makes it particularly suitable for applications that prioritize rapid and reliable earthquake event detection.

This analysis highlights the inherent trade-offs in multi-container execution for data archiving and seismic detection. While increasing container instances enhances parallelism and scalability, it leads to higher resource consumption. The choice of system architecture depends on the specific performance requirements, whether prioritizing speed and efficiency with Kafka or maximizing scalability with FastAPI. Understanding these trade-offs is essential for optimizing system deployment based on the available computational resources and real-time processing needs.

**Table 6.** WebSocket Experiment Result

| **Scenario** | **Data Delay (seconds)** | **CPU Usage (%)** | **Memory Usage (MB)** |
|---|---|---|---|
| Express JS 1 Client | 0.001324 | 12.02% | 95.49MB |
| Express JS 5 Client | 0.001452 | 13.38% | 96.05MB |
| Fast API 1 Client | 0.001356 | 17.71% | 72.67MB |
| Fast API 5 Client | 0.001578 | 39.05% | 72.97MB |

The WebSocket experiment evaluates the performance of Express.js and FastAPI in handling real-time communication across different client loads. The results indicate that Express.js provides lower data delay and lower CPU usage compared to FastAPI. With a delay of 0.001324 seconds and 12.02% CPU usage for a single client, Express.js efficiently handles WebSocket connections with minimal resource overhead. Even with five clients, it maintains a low delay of 0.001452 seconds, with only a slight increase in CPU usage (13.38%). However, memory usage remains relatively high, ranging from 95.49 MB to 96.05 MB, suggesting that Express.js requires more memory for concurrent connections.

On the other hand, FastAPI demonstrates better memory efficiency, using only 72.67 MB for one client and 72.97 MB for five clients. However, this comes at the cost of higher CPU usage, particularly when handling multiple clients. While the delay remains competitive (0.001356 seconds for one client and 0.001578 seconds for five clients), CPU usage increases significantly, reaching 39.05% when handling five concurrent clients. This suggests that FastAPI is more memory-efficient but consumes significantly more CPU as the number of connections grows.

Express.js is more suitable for real-time applications that prioritize low latency and reduced CPU consumption, making it an ideal choice for handling high-concurrency WebSocket connections efficiently [37]. In contrast, FastAPI offers better memory efficiency but at the cost of significantly higher CPU usage as the number of connections increases. The selection between these frameworks should be based on system constraints whether minimizing CPU overhead for scalability with Express.js or optimizing memory usage with FastAPI for resource-limited environments. These findings are derived from Table 6, which presents the WebSocket experiment results.

5. **Conclusion and Limitation**

This study presents a comprehensive performance analysis of parallel data processing, load balancing, multi-container execution, and WebSocket implementation in a distributed computing environment. The Multiprocessing approach proved to be the most efficient for handling parallel tasks, achieving 2.955 seconds delay, 44.50% CPU usage, and 476 MB memory consumption, making it highly suitable for real-time processing in Earthquake Early Warning Systems (EEWS). In message brokering, using Kafka alone resulted in lower data delay (0.006329 seconds) but at the cost of higher memory usage, while integrating NGINX as a load balancer improved memory efficiency but slightly increased latency. The multi-container execution strategy in data archiving and seismic detection enhanced system scalability but introduced higher CPU and memory consumption, highlighting the trade-off between processing speed and resource utilization.

For real-time communication, Express.js demonstrated lower latency and CPU usage (12.02%), making it an ideal choice for handling WebSocket connections in EEWS, though its memory consumption was higher. FastAPI, on the other hand, provided better memory efficiency but at the cost of increased CPU usage, making it suitable for environments with memory constraints. Based on these findings, optimizing EEWS should involve a Multiprocessing approach for efficient parallel data processing, Kafka with NGINX for scalable and efficient message brokering, multi-container execution for improved system modularity, and Express.js for low-latency WebSocket communication, ensuring a fast, reliable, and resource-efficient earthquake detection and alert system, such as the combination of ML-based phase picking and rapid localization demonstrated by Lian et al. [38].

**Declaration of competing interest**

There is no conflict of Interest.

**CRediT authorship contribution statement**

**Satriawan Rasyid Purnama**: Conceptualization, Formal analysis, Software, Writing – review & editing. **Adi Wibowo** (corresponding author): Conceptualization, Supervision, Project administration, Writing – review & editing, Data curation & evaluation protocols, Validation, Domain review. **Arjuna Wahyu Kusuma**: Writing – original draft, Formal analysis, Software, Figures/Visualization. **Liem Roy Marcelino**: Software, Data curation, Evaluation protocols. **Indra Waspada**: Supervision, Project administration. **Cecep Pratama**: Supervision, Project administration. **Leni Sophia Heliani**: Validation, Domain review. **David Prambudi Sahara**: Conceptualization. **Sri Widiyantoro**: Validation, Domain review. **Shindy Rosalia**: Data curation, Evaluation protocols. **Bondan Febriarta**: Software. **Cahyo Adhi Hartanto**: Software.

**Declaration of generative AI and AI-assisted technologies in the writing process**

During the preparation of this work the author(s) used ChatGPT to improve language and readability. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication.

**Acknowledgements**

The authors would like to acknowledge to Badan Meteorologi, Klimatologi, dan Geofisika, Jakarta, Indonesia for the Seismic Data and the Directorate General of Higher Education Research and Technology and Dikti AI Centre for the NVIDA DGX A100 access. This work was supported by Riset Publikasi Internasional Bereputasi Tinggi (RPIBT), Universitas Diponegoro, Indonesia, under Grant No. 222-677/UN7.D2/PP/IV/2025.

**References:**

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
