import sys
import os
import json
import time
from time import sleep
from random import randint
from typing import Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import (
    KAFKA_BROKERS,
    KAFKA_BROKERS_PWAVE,
    KAFKA_TOPIC_TRACE,
    KAFKA_TOPIC_PWAVE
)
from utils.kafka_helper import create_topic_if_not_exists, get_producer
from utils.logger import get_logger

logger = get_logger("DataProviderGenerator")

network = ['GE', 'IA']
station = ['BBJI', 'JAGI', 'SMRI', 'PARI', 'KUJI', 'BKB', 'TNTI', 'KUJI']
location = ''
channel = [
    'BHZ', 'BHN', 'BHE', 'SHZ', 'SHN', 'SHE', 
    'HHZ', 'HHN', 'HHE', 'EHZ', 'EHN', 'EHE'
]
sampling_rate = 100
delta = 0.01
npts = 900
calib = 1.0
data_quality = 'D'
num_samples = 900
sample_cnt = 900
sample_type = 'i'

def generate_waveform() -> Dict[str, Any]:
    starttime = time.time() - 9
    endtime = time.time()

    # generate random waveform
    wave = [randint(-1000, 1000) for i in range(npts)]

    data = {
        'network': network[randint(0, 1)],
        'station': station[randint(0, 7)],
        'location': location,
        'channel': channel[randint(0, 11)],
        'start_time': starttime,
        'end_time': endtime,
        'sampling_rate': sampling_rate,
        'delta': delta,
        'npts': npts,
        'calib': calib,
        'data_quality': data_quality,
        'num_samples': num_samples,
        'sample_cnt': sample_cnt,
        'sample_type': sample_type,
        'data_provider_time': time.time(),
        'data': wave
    }
    return data

if __name__ == '__main__':
    logger.info("Starting Data Provider Generator...")

    # Ensure required topics exist
    create_topic_if_not_exists(
        topic_name=KAFKA_TOPIC_TRACE,
        num_partitions=3,
        replication_factor=2,
        bootstrap_servers=KAFKA_BROKERS
    )
    
    create_topic_if_not_exists(
        topic_name=KAFKA_TOPIC_PWAVE,
        num_partitions=5,
        replication_factor=1,
        bootstrap_servers=KAFKA_BROKERS_PWAVE
    )

    producer = get_producer(KAFKA_BROKERS)
    producer_pwave = get_producer(KAFKA_BROKERS_PWAVE)

    sleep(5)
    throughput = 125
    sleep_time = 1 / throughput

    logger.info("Starting waveform generation loop...")
    while True:
        start_time = time.time()
        data = generate_waveform()
        logger.debug(f"Sending data {data['station']}-{data['channel']}")

        producer.send(KAFKA_TOPIC_TRACE, data, key=f"{data['station']}-{data['channel']}")
        producer.flush()

        if data['channel'].endswith('Z'):
            producer_pwave.send(KAFKA_TOPIC_PWAVE, data, key=f"{data['station']}-{data['channel']}")
            producer_pwave.flush()

        end_time = time.time()
        sleep(max(0.0, sleep_time - (end_time - start_time)))
