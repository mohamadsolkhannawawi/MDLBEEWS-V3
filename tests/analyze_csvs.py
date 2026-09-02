import os
import glob
import csv
import json

results_dir = r"e:\Documents\Bahan Skripsi\Program EEWS\MDLBEEWS\tests\results"
csv_files = glob.glob(os.path.join(results_dir, "*.csv"))

report = {}

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

for f in csv_files:
    basename = os.path.basename(f)
    try:
        with open(f, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            
            if not rows:
                report[basename] = {"status": "empty file"}
                continue
                
            headers = rows[0]
            data_rows = rows[1:]
            
            empty_rows = sum(1 for row in data_rows if all(not cell.strip() for cell in row))
            missing_values = sum(1 for row in data_rows for cell in row if not cell.strip())
            
            summary = {
                "rows": len(data_rows),
                "columns": len(headers),
                "col_names": headers,
                "missing_values_count": missing_values,
                "empty_rows": empty_rows,
                "status": "valid"
            }
            
            # For each column, if it contains numeric data, check if there are any valid values
            for idx, col_name in enumerate(headers):
                if col_name in ['cpu_usage_percent', 'memory_used_mb', 'e2e_delay_pwave_p95', 'e2e_delay_locmag_p95']:
                    valid_values = [float(row[idx]) for row in data_rows if len(row) > idx and is_float(row[idx])]
                    if valid_values:
                        summary[f"mean_{col_name}"] = sum(valid_values) / len(valid_values)
                        summary[f"min_{col_name}"] = min(valid_values)
                        summary[f"max_{col_name}"] = max(valid_values)
                    else:
                        summary[f"mean_{col_name}"] = None
                        
            report[basename] = summary
    except Exception as e:
        report[basename] = {"error": str(e), "status": "error"}

with open(os.path.join(results_dir, "analysis_report.json"), "w") as f:
    json.dump(report, f, indent=2)

print(f"Processed {len(csv_files)} files. Report saved to analysis_report.json")
