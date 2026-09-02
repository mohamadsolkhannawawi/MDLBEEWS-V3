import argparse
import csv
import math
import os
import statistics

BASELINE_COLUMNS = {
    "aggregate_cpu_percent": "aggregate_cpu_percent",
    "aggregate_mem_mb": "aggregate_mem_mb",
}


def parse_value(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def read_csv_values(path):
    with open(path, newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))
    columns = {}
    for row in rows:
        for name, value in row.items():
            if name == "timestamp":
                continue
            columns.setdefault(name, []).append(parse_value(value))
    return rows, columns


def percentile(values, percentile_rank):
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * percentile_rank / 100
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def summarize(values, total_count):
    valid_values = [value for value in values if value is not None]
    missing_count = total_count - len(valid_values)
    if not valid_values:
        return {
            "samples": total_count,
            "valid": 0,
            "missing": missing_count,
            "missing_percent": 100.0 if total_count else 0.0,
            "mean": None,
            "median": None,
            "stdev": None,
            "p95": None,
        }
    return {
        "samples": total_count,
        "valid": len(valid_values),
        "missing": missing_count,
        "missing_percent": round(missing_count / total_count * 100, 2) if total_count else 0.0,
        "mean": round(statistics.mean(valid_values), 4),
        "median": round(statistics.median(valid_values), 4),
        "stdev": round(statistics.stdev(valid_values), 4) if len(valid_values) > 1 else 0.0,
        "p95": round(percentile(valid_values, 95), 4),
    }


def calculate_comparison(baseline, observed):
    baseline_mean = baseline["mean"]
    observed_mean = observed["mean"]
    if baseline_mean is None or observed_mean is None or baseline_mean == 0:
        return {
            "status": "not_comparable",
            "absolute_change": None,
            "percent_change": None,
        }
    absolute_change = observed_mean - baseline_mean
    return {
        "status": "comparable",
        "absolute_change": round(absolute_change, 4),
        "percent_change": round(absolute_change / baseline_mean * 100, 4),
    }


def write_summary(path, baseline_path, observed_path, baseline_columns, observed_columns):
    fields = [
        "metric", "baseline_file", "observed_file", "baseline_mean", "observed_mean",
        "absolute_change", "percent_change", "status", "baseline_valid", "baseline_missing",
        "observed_valid", "observed_missing", "observed_missing_percent", "rule",
    ]
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for metric in sorted(set(baseline_columns) | set(observed_columns)):
            baseline = baseline_columns.get(metric)
            observed = observed_columns.get(metric)
            comparison = calculate_comparison(baseline, observed) if baseline and observed else {
                "status": "no_baseline" if observed else "no_observed_data",
                "absolute_change": None,
                "percent_change": None,
            }
            writer.writerow({
                "metric": metric,
                "baseline_file": baseline_path,
                "observed_file": observed_path,
                "baseline_mean": baseline["mean"] if baseline else "",
                "observed_mean": observed["mean"] if observed else "",
                "absolute_change": comparison["absolute_change"] if comparison["absolute_change"] is not None else "",
                "percent_change": comparison["percent_change"] if comparison["percent_change"] is not None else "",
                "status": comparison["status"],
                "baseline_valid": baseline["valid"] if baseline else "",
                "baseline_missing": baseline["missing"] if baseline else "",
                "observed_valid": observed["valid"] if observed else "",
                "observed_missing": observed["missing"] if observed else "",
                "observed_missing_percent": observed["missing_percent"] if observed else "",
                "rule": "Compare means only when both files have valid numeric data; blanks are excluded, never zero-filled",
            })


def main():
    parser = argparse.ArgumentParser(description="Analyze S2 overhead baseline versus metrics")
    parser.add_argument("--s1a", default="tests/results/s2_overhead_no_metrics_stats.csv", help="S2 without metrics CSV")
    parser.add_argument("--s1b", default="tests/results/s2_overhead_with_metrics_stats.csv", help="S2 with metrics CSV")
    parser.add_argument("--output", default="tests/results/s2_comparison.csv", help="Comparison output CSV")
    args = parser.parse_args()

    for path in (args.s1a, args.s1b):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Input CSV not found: {path}")

    s1a_rows, s1a_columns = read_csv_values(args.s1a)
    s1b_rows, s1b_columns = read_csv_values(args.s1b)
    s1a_summary = {name: summarize(values, len(s1a_rows)) for name, values in s1a_columns.items()}
    s1b_summary = {name: summarize(values, len(s1b_rows)) for name, values in s1b_columns.items()}

    output_directory = os.path.dirname(args.output)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    write_summary(args.output, args.s1a, args.s1b, s1a_summary, s1b_summary)

    print(f"S1a samples: {len(s1a_rows)}")
    print(f"S1b samples: {len(s1b_rows)}")
    print(f"Comparison saved to: {args.output}")
    print("\nMetric comparison:")
    for metric in sorted(set(s1a_summary) | set(s1b_summary)):
        baseline = s1a_summary.get(metric)
        observed = s1b_summary.get(metric)
        if baseline and observed:
            comparison = calculate_comparison(baseline, observed)
            print(
                f"- {metric}: status={comparison['status']}, "
                f"S1a mean={baseline['mean']}, S1b mean={observed['mean']}, "
                f"change={comparison['absolute_change']}, "
                f"change_percent={comparison['percent_change']}, "
                f"S1b missing={observed['missing_percent']}%"
            )
        elif observed:
            print(f"- {metric}: status=no_baseline, S1b valid={observed['valid']}, S1b missing={observed['missing_percent']}%")


if __name__ == "__main__":
    main()
