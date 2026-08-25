import requests
import csv
import time
import argparse
import os

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

# Define the PromQL queries we want to run and record
QUERIES = {
    "cpu_usage_percent": '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)',
    "memory_used_mb": '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / 1024 / 1024',
    "pwave_inference_latency_p95": 'histogram_quantile(0.95, rate(pwave_inference_latency_seconds_bucket[1m]))',
    "pwave_lb_inference_latency_p95": 'histogram_quantile(0.95, rate(pwave_lb_inference_latency_seconds_bucket[1m]))',
    "lb_forward_latency_p95": 'histogram_quantile(0.95, rate(lb_forward_latency_seconds_bucket[1m]))',
    "locmag_inference_latency_p95": 'histogram_quantile(0.95, rate(locmag_inference_latency_seconds_bucket[1m]))',
    "e2e_delay_pwave_p95": 'histogram_quantile(0.95, rate(pwave_end_to_end_latency_seconds_bucket[1m]))',
    "e2e_delay_locmag_p95": 'histogram_quantile(0.95, rate(locmag_end_to_end_latency_seconds_bucket[1m]))',
    "active_ws_clients_express": 'ws_active_clients',
    "active_ws_clients_fastapi": 'fastapi_ws_active_clients'
}

def fetch_metric(query):
    try:
        response = requests.get(PROMETHEUS_URL, params={'query': query})
        response.raise_for_status()
        results = response.json()['data']['result']
        if results:
            # For simplicity, returning the first result's value
            return round(float(results[0]['value'][1]), 4)
        return 0.0
    except Exception as e:
        print(f"Error fetching query '{query}': {e}")
        return 0.0

def collect_metrics(duration_sec, interval_sec, output_file):
    print(f"Starting metrics collection for {duration_sec} seconds (interval: {interval_sec}s).")
    print(f"Output will be saved to: {output_file}")
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    headers = ["timestamp"] + list(QUERIES.keys())
    
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        start_time = time.time()
        while time.time() - start_time < duration_sec:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            row = [current_time]
            
            for name, query in QUERIES.items():
                val = fetch_metric(query)
                row.append(val)
                
            writer.writerow(row)
            print(f"Collected at {current_time}: {row}")
            time.sleep(interval_sec)
            
    print(f"Metrics collection completed. Data saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect Prometheus metrics to CSV")
    parser.add_argument("--duration", type=int, default=60, help="Duration to collect metrics in seconds")
    parser.add_argument("--interval", type=int, default=5, help="Interval between scrapes in seconds")
    parser.add_argument("--output", type=str, default="results/metrics_output.csv", help="Output CSV file path")
    args = parser.parse_args()

    collect_metrics(args.duration, args.interval, args.output)
