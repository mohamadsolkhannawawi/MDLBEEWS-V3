from SeedlinkClient import run_client
from utils.util import get_station_configs, get_station_by_network
import multiprocessing
import threading
from time import sleep

def process_worker(server, configs, process_id):
    num_threads = 2
    if len(configs) < num_threads:
        num_threads = len(configs)
        
    if num_threads == 0:
        return
        
    chunk_size = len(configs) // num_threads
    threads = []
    
    for i in range(num_threads):
        start_idx = i * chunk_size
        # Give remaining configs to the last thread
        end_idx = (i + 1) * chunk_size if i < num_threads - 1 else len(configs)
        chunk = configs[start_idx:end_idx]
        
        if chunk:
            t = threading.Thread(target=run_client, args=(server, chunk, f"{process_id}-{i}"))
            threads.append(t)
            
    for t in threads:
        t.start()
        sleep(0.2)
        
    for t in threads:
        t.join()

def main(server='geofon.gfz-potsdam.de:18000', station_path = 'data_provider/data/stations.json', num_processes=24, num_station_configs=6000):
    station_configs = get_station_configs(station_path, num_station_configs)

    print('Running with', len(station_configs), 'station configs')
    print('Running with', num_processes, 'processes')

    processes = []
    num_configs = len(station_configs) // num_processes
    
    # Fallback if there are fewer configs than processes
    if num_configs == 0:
        num_configs = 1
        num_processes = len(station_configs)

    for i in range(num_processes):
        start_idx = num_configs * i
        end_idx = num_configs * (i + 1) if i < num_processes - 1 else len(station_configs)
        chunk = station_configs[start_idx:end_idx]
        
        if chunk:
            p = multiprocessing.Process(target=process_worker, args=(server, chunk, i))
            processes.append(p)

    # start all processes
    for p in processes:
        p.start()
        sleep(0.2)

    print('All processes started')