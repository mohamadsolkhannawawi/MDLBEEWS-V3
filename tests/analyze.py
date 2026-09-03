import argparse
import csv
import math
import os
import statistics
import glob
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

def parse_value(value):
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except (TypeError, ValueError):
        return None

def read_csv(path):
    if not os.path.exists(path):
        return None
    with open(path, newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))
        
    columns = defaultdict(list)
    for row in rows:
        for name, value in row.items():
            if name == "timestamp":
                continue
            columns[name].append(parse_value(value))
    return columns

def calc_stats(values):
    valid_values = [v for v in values if v is not None]
    if not valid_values:
        return {'mean': 'N/A', 'p95': 'N/A', 'max': 'N/A'}
    
    mean_val = statistics.mean(valid_values)
    max_val = max(valid_values)
    
    # Calculate P95
    ordered = sorted(valid_values)
    idx = int(0.95 * len(ordered))
    p95_val = ordered[idx] if idx < len(ordered) else ordered[-1]
    
    return {
        'mean': round(mean_val, 2),
        'p95': round(p95_val, 2),
        'max': round(max_val, 2)
    }

def print_table(headers, data_rows):
    if not data_rows:
        print("Data tidak tersedia.\n")
        return

    col_widths = [max(len(str(item)) for item in col) for col in zip(*([headers] + data_rows))]
    format_row = " | ".join(["{:<" + str(width) + "}" for width in col_widths])
    
    print(format_row.format(*headers))
    print("-|-".join(["-" * width for width in col_widths]))
    for row in data_rows:
        print(format_row.format(*row))
    print("\n")

def analyze_s1():
    print("=== ANALISIS SKENARIO 1 (Pengolahan Konkurensi) ===")
    scenarios = ["s1_sequential_stats.csv", "s1_multithread_stats.csv", "s1_multiprocess_stats.csv", "s1_mp_mt_stats.csv"]
    
    headers = ["Mode Konkurensi", "CPU Mean (%)", "CPU Max (%)", "RAM Mean (MB)", "RAM Max (MB)"]
    table_data = []
    
    for filename in scenarios:
        path = os.path.join(RESULTS_DIR, filename)
        cols = read_csv(path)
        mode_name = filename.replace("_stats.csv", "").replace("s1_", "").upper()
        
        if not cols:
            table_data.append([mode_name, "N/A", "N/A", "N/A", "N/A"])
            continue
            
        cpu_stats = calc_stats(cols.get("aggregate_cpu_percent", []))
        mem_stats = calc_stats(cols.get("aggregate_mem_mb", []))
        
        table_data.append([
            mode_name, 
            cpu_stats['mean'], cpu_stats['max'], 
            mem_stats['mean'], mem_stats['max']
        ])
        
    print_table(headers, table_data)

def analyze_s2():
    print("=== ANALISIS SKENARIO 2 (Overhead Observabilitas) ===")
    scenarios = [("Tanpa Metrics", "s2_overhead_no_metrics_stats.csv"), ("Dengan Metrics", "s2_overhead_with_metrics_stats.csv")]
    
    headers = ["Kondisi", "CPU Mean (%)", "CPU P95 (%)", "RAM Mean (MB)", "RAM P95 (MB)"]
    table_data = []
    
    for label, filename in scenarios:
        path = os.path.join(RESULTS_DIR, filename)
        cols = read_csv(path)
        
        if not cols:
            table_data.append([label, "N/A", "N/A", "N/A", "N/A"])
            continue
            
        cpu = calc_stats(cols.get("aggregate_cpu_percent", []))
        mem = calc_stats(cols.get("aggregate_mem_mb", []))
        table_data.append([label, cpu['mean'], cpu['p95'], mem['mean'], mem['p95']])
        
    print_table(headers, table_data)

def analyze_s3():
    print("=== ANALISIS SKENARIO 3 (Load Balancer NGINX vs Native) ===")
    scenarios = [("Native Kafka", "s3_pwave_kafka_stats.csv"), ("NGINX LB", "s3_pwave_kafka_nginx_stats.csv")]
    
    headers = ["Arsitektur", "P-Wave Latency Mean (ms)", "P-Wave Latency P95 (ms)", "CPU Mean (%)", "RAM Mean (MB)"]
    table_data = []
    
    for label, filename in scenarios:
        path = os.path.join(RESULTS_DIR, filename)
        cols = read_csv(path)
        
        if not cols:
            table_data.append([label, "N/A", "N/A", "N/A", "N/A"])
            continue
            
        lat = calc_stats(cols.get("e2e_delay_pwave_p95", []))
        cpu = calc_stats(cols.get("aggregate_cpu_percent", []))
        mem = calc_stats(cols.get("aggregate_mem_mb", []))
        
        table_data.append([label, lat['mean'], lat['p95'], cpu['mean'], mem['mean']])
        
    print_table(headers, table_data)

def analyze_s4():
    print("=== ANALISIS SKENARIO 4 (WebSocket FastAPI vs Express.js) ===")
    scenarios = [("FastAPI", "s4_fastapi_stats.csv"), ("Express.js", "s4_express_stats.csv")]
    
    headers = ["Server", "Broadcast Latency Mean", "Broadcast Latency P95", "CPU Mean (%)", "RAM Mean (MB)"]
    table_data = []
    
    for label, filename in scenarios:
        path = os.path.join(RESULTS_DIR, filename)
        cols = read_csv(path)
        
        if not cols:
            table_data.append([label, "N/A", "N/A", "N/A", "N/A"])
            continue
            
        # Assuming e2e_delay is recorded, fallback if not
        lat = calc_stats(cols.get("e2e_delay_locmag_p95", cols.get("e2e_delay_pwave_p95", [])))
        cpu = calc_stats(cols.get("aggregate_cpu_percent", []))
        mem = calc_stats(cols.get("aggregate_mem_mb", []))
        
        table_data.append([label, lat['mean'], lat['p95'], cpu['mean'], mem['mean']])
        
    print_table(headers, table_data)

def analyze_all():
    analyze_s1()
    analyze_s2()
    analyze_s3()
    analyze_s4()
    print("Semua skenario berhasil dianalisis!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EEWS Test Result Analyzer")
    parser.add_argument('--scenario', choices=['1', '2', '3', '4', 'all'], default='all', help="Pilih Skenario (1-4) atau 'all'")
    
    args = parser.parse_args()
    
    if args.scenario == '1': analyze_s1()
    elif args.scenario == '2': analyze_s2()
    elif args.scenario == '3': analyze_s3()
    elif args.scenario == '4': analyze_s4()
    else: analyze_all()
