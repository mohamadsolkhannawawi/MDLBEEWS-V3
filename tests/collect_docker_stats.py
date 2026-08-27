import subprocess
import csv
import time
import argparse
import os

def parse_docker_stats():
    # runs: docker stats --no-stream --format "{{.Name}},{{.CPUPerc}},{{.MemUsage}}"
    try:
        result = subprocess.run(['docker', 'stats', '--no-stream', '--format', '{{.Name}},{{.CPUPerc}},{{.MemUsage}}'], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running docker stats: {e.stderr}")
        return {}
        
    stats = {}
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split(',')
        if len(parts) == 3:
            name = parts[0]
            # e.g., "0.01%"
            cpu_str = parts[1].replace('%', '')
            cpu = 0.0
            try:
                cpu = float(cpu_str) if cpu_str else 0.0
            except ValueError:
                pass
            
            # e.g., "5.688MiB / 15.42GiB"
            mem_str = parts[2].split('/')[0].strip()
            mem_val = 0.0
            try:
                if mem_str.endswith('MiB'):
                    mem_val = float(mem_str.replace('MiB', ''))
                elif mem_str.endswith('GiB'):
                    mem_val = float(mem_str.replace('GiB', '')) * 1024
                elif mem_str.endswith('KiB'):
                    mem_val = float(mem_str.replace('KiB', '')) / 1024
                elif mem_str.endswith('B'):
                    mem_val = float(mem_str.replace('B', '')) / (1024*1024)
            except ValueError:
                pass
                
            stats[name] = {
                'cpu': cpu,
                'mem_mb': mem_val
            }
    return stats

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', type=int, default=120)
    parser.add_argument('--interval', type=int, default=5)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--target-substring', type=str, required=True, help="Substring of the container name to aggregate (e.g. 'data_archiver')")
    args = parser.parse_args()
    
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    with open(args.output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'aggregate_cpu_percent', 'aggregate_mem_mb'])
        
        start_time = time.time()
        while time.time() - start_time < args.duration:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            stats = parse_docker_stats()
            
            agg_cpu = 0.0
            agg_mem = 0.0
            
            for name, data in stats.items():
                if args.target_substring in name:
                    agg_cpu += data['cpu']
                    agg_mem += data['mem_mb']
                    
            writer.writerow([current_time, round(agg_cpu, 2), round(agg_mem, 2)])
            f.flush()
            print(f"[{current_time}] Aggregate for '{args.target_substring}': CPU={agg_cpu:.2f}%, Mem={agg_mem:.2f}MB")
            
            time.sleep(args.interval)

if __name__ == '__main__':
    main()
