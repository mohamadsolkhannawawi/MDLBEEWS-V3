import subprocess
import time
import csv
import argparse
import os

def get_docker_stats():
    # Run docker stats to get CPU and Mem usage for all running containers
    try:
        result = subprocess.run(
            ['docker', 'stats', '--no-stream', '--format', '{{.Name}},{{.CPUPerc}},{{.MemUsage}}'],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running docker stats: {e}")
        return 0.0, 0.0

    total_cpu = 0.0
    total_mem_mb = 0.0

    lines = result.stdout.strip().split('\n')
    for line in lines:
        if not line:
            continue
        parts = line.split(',')
        if len(parts) == 3:
            name, cpu_str, mem_str = parts
            
            # We only track p_wave_detector containers to be consistent with Prometheus metrics
            if "p_wave_detector" not in name:
                continue

            # Parse CPU %
            cpu_val = cpu_str.replace('%', '')
            try:
                total_cpu += float(cpu_val)
            except ValueError:
                pass

            # Parse Memory Usage (e.g., "15.5MiB / 16GiB")
            mem_usage_str = mem_str.split('/')[0].strip()
            mem_val = 0.0
            try:
                if 'GiB' in mem_usage_str:
                    mem_val = float(mem_usage_str.replace('GiB', '')) * 1024
                elif 'MiB' in mem_usage_str:
                    mem_val = float(mem_usage_str.replace('MiB', ''))
                elif 'KiB' in mem_usage_str:
                    mem_val = float(mem_usage_str.replace('KiB', '')) / 1024
                elif 'B' in mem_usage_str:
                    mem_val = float(mem_usage_str.replace('B', '')) / (1024 * 1024)
                total_mem_mb += mem_val
            except ValueError:
                pass

    return total_cpu, total_mem_mb

def main():
    parser = argparse.ArgumentParser(description="Collect Docker Stats")
    parser.add_argument("--duration", type=int, default=60, help="Duration to collect in seconds")
    parser.add_argument("--output", type=str, required=True, help="Output CSV path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    headers = ["timestamp", "pwave_aggregate_cpu_percent", "pwave_aggregate_mem_mb"]
    
    start_time = time.time()
    
    try:
        with open(args.output, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            while time.time() - start_time < args.duration:
                ts = time.strftime("%Y-%m-%d %H:%M:%S")
                cpu, mem = get_docker_stats()
                
                row = [ts, round(cpu, 4), round(mem, 4)]
                writer.writerow(row)
                f.flush()
                print(f"Collected at {ts}: {row}")
                
                # Sleep for roughly 5 seconds, minus the time it took to run docker stats
                time.sleep(5)
                
    except PermissionError:
        print(f"Permission denied writing to {args.output}")

if __name__ == "__main__":
    main()
