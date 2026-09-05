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
    if not values:
        return {'mean': 'N/A', 'p95': 'N/A', 'max': 'N/A'}
    valid_values = [v for v in values if v is not None]
    if not valid_values:
        return {'mean': 'N/A', 'p95': 'N/A', 'max': 'N/A'}
    
    mean_val = statistics.mean(valid_values)
    max_val = max(valid_values)
    
    ordered = sorted(valid_values)
    idx = int(0.95 * len(ordered))
    p95_val = ordered[idx] if idx < len(ordered) else ordered[-1]
    
    return {
        'mean': round(mean_val, 2),
        'p95': round(p95_val, 2),
        'max': round(max_val, 2)
    }

def calc_latency_stats(values):
    if not values:
        return {'mean': 'N/A', 'p95': 'N/A', 'max': 'N/A'}
    valid_values = [v for v in values if v is not None]
    if not valid_values:
        return {'mean': 'N/A', 'p95': 'N/A', 'max': 'N/A'}
    
    valid_values = [v * 1000 for v in valid_values]
    
    mean_val = statistics.mean(valid_values)
    max_val = max(valid_values)
    
    ordered = sorted(valid_values)
    idx = int(0.95 * len(ordered))
    p95_val = ordered[idx] if idx < len(ordered) else ordered[-1]
    
    return {
        'mean': round(mean_val, 2),
        'p95': round(p95_val, 2),
        'max': round(max_val, 2)
    }

def save_and_print_table(title, headers, data_rows, csv_filename):
    print(f"=== {title} ===")
    if not data_rows:
        print("Data tidak tersedia.\n")
        return

    # 1. Print formatted markdown-like table to console
    col_widths = [max(len(str(item)) for item in col) for col in zip(*([headers] + data_rows))]
    format_row = " | ".join(["{:<" + str(width) + "}" for width in col_widths])
    
    print(format_row.format(*headers))
    print("-|-".join(["-" * width for width in col_widths]))
    for row in data_rows:
        print(format_row.format(*row))
    print("\n")

    # 2. Save summary to CSV file
    os.makedirs(RESULTS_DIR, exist_ok=True)
    csv_path = os.path.join(RESULTS_DIR, csv_filename)
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data_rows)
    print(f"[SAVED] Summary tersimpan di: {csv_path}\n")

def analyze_s1():
    scenarios = ["s1_sequential", "s1_multithread", "s1_multiprocess", "s1_mp_mt"]
    headers = ["Arsitektur", "Throughput (Trace/s)", "CPU Mean (%)", "CPU Max (%)", "RAM Mean (MB)"]
    table_data = []
    
    for prefix in scenarios:
        metrics = read_csv(os.path.join(RESULTS_DIR, f"{prefix}_metrics.csv"))
        stats = read_csv(os.path.join(RESULTS_DIR, f"{prefix}_stats.csv"))
        if not stats and metrics:
            stats = metrics
        mode_name = prefix.replace("s1_", "").upper()
        
        if not stats:
            table_data.append([mode_name, "N/A", "N/A", "N/A", "N/A"])
            continue
            
        cpu = calc_stats(stats.get("aggregate_cpu_percent", []))
        mem = calc_stats(stats.get("aggregate_mem_mb", []))
        tp = calc_stats(metrics.get("dp_throughput_traces_per_sec", [])) if metrics else {'mean': 'N/A'}
        
        table_data.append([mode_name, tp['mean'], cpu['mean'], cpu['max'], mem['mean']])
    
    save_and_print_table("ANALISIS SKENARIO 1 (Konkurensi Data Provider)", headers, table_data, "summary_s1_concurrency.csv")

def analyze_s2():
    scenarios = [("Tanpa Metrics", "s2_overhead_no_metrics"), ("Dengan Metrics", "s2_overhead_with_metrics")]
    headers = ["Kondisi", "CPU Mean (%)", "CPU P95 (%)", "RAM Mean (MB)", "RAM Max (MB)"]
    table_data = []
    
    for label, prefix in scenarios:
        stats = read_csv(os.path.join(RESULTS_DIR, f"{prefix}_stats.csv"))
        if not stats:
            table_data.append([label, "N/A", "N/A", "N/A", "N/A"])
            continue
        cpu = calc_stats(stats.get("aggregate_cpu_percent", []))
        mem = calc_stats(stats.get("aggregate_mem_mb", []))
        table_data.append([label, cpu['mean'], cpu['p95'], mem['mean'], mem['max']])
    
    save_and_print_table("ANALISIS SKENARIO 2 (Overhead Observabilitas)", headers, table_data, "summary_s2_overhead.csv")

def analyze_s3():
    # Part A: Archiver
    headers_a = ["Replika", "CPU Mean (%)", "CPU Max (%)", "RAM Mean (MB)"]
    table_data_a = []
    for i in range(1, 6):
        stats = read_csv(os.path.join(RESULTS_DIR, f"s3_archiver_{i}_container_stats.csv"))
        if stats:
            cpu = calc_stats(stats.get("aggregate_cpu_percent", []))
            mem = calc_stats(stats.get("aggregate_mem_mb", []))
            table_data_a.append([f"{i} Container", cpu['mean'], cpu['max'], mem['mean']])
        else:
            table_data_a.append([f"{i} Container", "N/A", "N/A", "N/A"])
    save_and_print_table("ANALISIS SKENARIO 3A (Skalabilitas Data Archiver)", headers_a, table_data_a, "summary_s3a_archiver.csv")

    # Part B: P-Wave Detector
    headers_b = ["Arsitektur", "Replika", "E2E P-Wave P95 (ms)", "CPU Mean (%)", "RAM Mean (MB)"]
    table_data_b = []
    for mode in [("Native Kafka", "s3_pwave_kafka"), ("Kafka+NGINX", "s3_pwave_kafka_nginx")]:
        for i in range(2, 6):
            metrics = read_csv(os.path.join(RESULTS_DIR, f"{mode[1]}_{i}c_metrics.csv"))
            stats = read_csv(os.path.join(RESULTS_DIR, f"{mode[1]}_{i}c_stats.csv"))
            if not metrics or not stats:
                table_data_b.append([mode[0], f"{i}c", "N/A (MISSING)", "N/A", "N/A"])
                continue
            lat = calc_latency_stats(metrics.get("e2e_delay_pwave_p95", []))
            cpu = calc_stats(stats.get("aggregate_cpu_percent", []))
            mem = calc_stats(stats.get("aggregate_mem_mb", []))
            table_data_b.append([mode[0], f"{i}c", lat['p95'], cpu['mean'], mem['mean']])
    save_and_print_table("ANALISIS SKENARIO 3B (Skalabilitas P-Wave Detector)", headers_b, table_data_b, "summary_s3b_pwave.csv")

def analyze_s4():
    headers = ["Server", "Klien Aktif", "Broadcast P95 (ms)", "CPU Mean (%)", "RAM Mean (MB)"]
    table_data = []
    for mode in [("FastAPI", "s4_websocket_fastapi"), ("Express.js", "s4_websocket_express")]:
        for c in [1, 5]:
            metrics = read_csv(os.path.join(RESULTS_DIR, f"{mode[1]}_{c}c_metrics.csv"))
            stats = read_csv(os.path.join(RESULTS_DIR, f"{mode[1]}_{c}c_stats.csv"))
            if not metrics or not stats:
                table_data.append([mode[0], f"{c} Klien", "N/A (MISSING)", "N/A", "N/A"])
                continue
            
            if "fastapi" in mode[1]:
                lat = calc_latency_stats(metrics.get("fastapi_ws_broadcast_latency_p95", []))
            else:
                lat = calc_latency_stats(metrics.get("ws_broadcast_latency_p95", []))
            cpu = calc_stats(stats.get("aggregate_cpu_percent", []))
            mem = calc_stats(stats.get("aggregate_mem_mb", []))
            table_data.append([mode[0], f"{c} Klien", lat['p95'], cpu['mean'], mem['mean']])
    save_and_print_table("ANALISIS SKENARIO 4 (WebSocket Server)", headers, table_data, "summary_s4_websocket.csv")

def analyze_s5():
    headers = ["Broker", "E2E P-Wave Mean (ms)", "E2E P-Wave P95 (ms)", "CPU Mean (%)", "RAM Mean (MB)"]
    table_data = []
    for mode in [("Kafka Native", "s5_broker_kafka"), ("Kafka + NGINX", "s5_broker_nginx")]:
        metrics = read_csv(os.path.join(RESULTS_DIR, f"{mode[1]}_metrics.csv"))
        stats = read_csv(os.path.join(RESULTS_DIR, f"{mode[1]}_stats.csv"))
        if not metrics or not stats:
            table_data.append([mode[0], "N/A", "N/A", "N/A", "N/A"])
            continue
            
        lat = calc_latency_stats(metrics.get("e2e_delay_pwave_p95", []))
        cpu = calc_stats(stats.get("aggregate_cpu_percent", []))
        mem = calc_stats(stats.get("aggregate_mem_mb", []))
        table_data.append([mode[0], lat['mean'], lat['p95'], cpu['mean'], mem['mean']])
    save_and_print_table("ANALISIS SKENARIO 5 (Message Broker Load Balancer)", headers, table_data, "summary_s5_broker.csv")

def analyze_all():
    analyze_s1()
    analyze_s2()
    analyze_s3()
    analyze_s4()
    analyze_s5()
    print("Semua skenario berhasil dianalisis dan disimpan ke CSV!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EEWS Test Result Analyzer")
    parser.add_argument('--scenario', choices=['1', '2', '3', '4', '5', 'all'], default='all')
    args = parser.parse_args()
    
    if args.scenario == '1': analyze_s1()
    elif args.scenario == '2': analyze_s2()
    elif args.scenario == '3': analyze_s3()
    elif args.scenario == '4': analyze_s4()
    elif args.scenario == '5': analyze_s5()
    else: analyze_all()
