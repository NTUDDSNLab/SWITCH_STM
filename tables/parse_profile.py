import os
import sys
import csv
import re
import statistics
import argparse

def parse_filename(filename):
    """
    Parses the filename to extract configuration and threads.
    Expected format: <config>_TP_<threads>.stm or <config>_<threads>.stm
    """
    # Remove .stm extension
    name = os.path.splitext(filename)[0]
    
    # Check for TP suffix and remove it for config name extraction if needed
    # But usually we want to know if it's TP. The user asked for parsing execution time breakdown,
    # which implies TP is enabled.
    
    parts = name.split('_')
    
    # Try to find the number at the end which is threads
    try:
        threads = int(parts[-1])
    except ValueError:
        return None, None

    # Config is everything before the last part
    # If '_TP_' is in the name, we might want to clean it up or keep it.
    # consistently with stm_results_runA.csv, configs are like 'ats', 'polka', 'suicide'.
    # So we should probably remove '_TP' from the config name if present.
    
    config_parts = parts[:-1]
    if config_parts and config_parts[-1] == 'TP':
         config_parts = config_parts[:-1]
         
    configuration = "_".join(config_parts)
    
    return configuration, threads

def get_benchmark_name(command_line):
    """
    Identifies the benchmark name from the execution command line.
    Handles variants like vacation -n2 (vacation_high).
    """
    # Example: Executing: ./vacation/vacation -n2 -q90 -u98 -r1048576 -t4194304 -c 8
    
    if "vacation" in command_line:
        if "-n2" in command_line:
            return "vacation_high"
        elif "-n4" in command_line:
            return "vacation_low"
        else:
            return "vacation" # Should not happen based on known tests
            
    elif "kmeans" in command_line:
        if "-m40" in command_line:
            return "kmeans_high"
        elif "-m15" in command_line:
            return "kmeans_low"
        else:
            return "kmeans"
            
    elif "yada" in command_line:
        return "yada"
    elif "intruder" in command_line:
        return "intruder"
    elif "bayes" in command_line:
        return "bayes"
    elif "genome" in command_line:
        return "genome"
    elif "labyrinth" in command_line:
        return "labyrinth"
    elif "ssca2" in command_line:
        return "ssca2"
        
    return None

def parse_log_file(filepath):
    """
    Parses a single log file and returns a list of dictionaries with parsed data.
    """
    filename = os.path.basename(filepath)
    config_from_file, threads_from_file = parse_filename(filename)
    
    if config_from_file is None:
        print(f"Skipping file {filename}: Could not parse filename.")
        return []

    data = []
    current_benchmark = None
    
    # Breakdown metrics
    current_breakdown = {}
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith("Executing:"):
            # New benchmark run starts
            current_benchmark = get_benchmark_name(line)
            current_breakdown = {}
        
        elif line == "-----------<< PROFILE >>-----------":
            # Breakdown section follows
            # Expecting 5 lines
            try:
                # Initialize defaults in case of parsing error
                commit = 0
                abort = 0
                wait = 0
                switch = 0
                other = 0
                switch_count = 0
                commit_after_switch = 0
                pscr = 0.0
                
                # Look ahead for the next lines
                # We expect the next 8 lines to contain the data (5 time metrics + 3 PSCR metrics)
                
                for _ in range(8):
                    i += 1
                    if i >= len(lines): break
                    b_line = lines[i].strip()
                    if "Total Commit Time:" in b_line:
                        commit = int(b_line.split(":")[1].strip().split()[0])
                    elif "Total Abort Time:" in b_line:
                        abort = int(b_line.split(":")[1].strip().split()[0])
                    elif "Total Wait Time:" in b_line:
                        wait = int(b_line.split(":")[1].strip().split()[0])
                    elif "Total Switch Time:" in b_line:
                        switch = int(b_line.split(":")[1].strip().split()[0])
                    elif "Total Other Time:" in b_line:
                        other = int(b_line.split(":")[1].strip().split()[0])
                    elif "Total Switch Count:" in b_line:
                        switch_count = int(b_line.split(":")[1].strip().split()[0])
                    elif "Total Commit After Switch:" in b_line:
                        commit_after_switch = int(b_line.split(":")[1].strip().split()[0])
                    elif "PSCR:" in b_line:
                        pscr = float(b_line.split(":")[1].strip())
                
                if current_benchmark:
                    entry = {
                        'Benchmark': current_benchmark,
                        'Configuration': config_from_file,
                        'Threads': threads_from_file,
                        'Commit': commit,
                        'Abort': abort,
                        'Wait': wait,
                        'Switch': switch,
                        'Other': other,
                        'SwitchCount': switch_count,
                        'CommitAfterSwitch': commit_after_switch,
                        'PSCR': pscr
                    }
                    data.append(entry)
                    
            except (ValueError, IndexError) as e:
                print(f"Error parsing breakdown in {filename} for {current_benchmark}: {e}")
        
        i += 1
        
    return data

def main():
    parser = argparse.ArgumentParser(description="Parse STM time breakdown logs.")
    parser.add_argument("--log_dir", default="../log/time_breakdown", help="Directory containing .stm log files")
    parser.add_argument("--output", default="stm_time_breakdown.csv", help="Output CSV file")
    
    args = parser.parse_args()
    
    all_data = []
    
    if not os.path.exists(args.log_dir):
        print(f"Error: Directory {args.log_dir} does not exist.")
        return

    files = [f for f in os.listdir(args.log_dir) if f.endswith(".stm")]
    
    print(f"Found {len(files)} log files in {args.log_dir}")
    
    for f in files:
        filepath = os.path.join(args.log_dir, f)
        parsed_data = parse_log_file(filepath)
        all_data.extend(parsed_data)
        
    if not all_data:
        print("No data parsed.")
        return

    # Aggregate data
    # Key: (Benchmark, Configuration, Threads)
    # Value: lists of metrics
    aggregated = {}
    
    for entry in all_data:
        key = (entry['Benchmark'], entry['Configuration'], entry['Threads'])
        if key not in aggregated:
            aggregated[key] = {
                'Commit': [], 'Abort': [], 'Wait': [], 'Switch': [], 'Other': [],
                'SwitchCount': [], 'CommitAfterSwitch': [], 'PSCR': []
            }
        
        aggregated[key]['Commit'].append(entry['Commit'])
        aggregated[key]['Abort'].append(entry['Abort'])
        aggregated[key]['Wait'].append(entry['Wait'])
        aggregated[key]['Switch'].append(entry['Switch'])
        aggregated[key]['Other'].append(entry['Other'])
        aggregated[key]['SwitchCount'].append(entry['SwitchCount'])
        aggregated[key]['CommitAfterSwitch'].append(entry['CommitAfterSwitch'])
        aggregated[key]['PSCR'].append(entry['PSCR'])
        
    # Prepare CSV rows
    csv_rows = []
    header = [
        "Benchmark", "Configuration", "Threads", 
        "Avg Commit (ms)", "Std Commit", 
        "Avg Abort (ms)", "Std Abort", 
        "Avg Wait (ms)", "Std Wait", 
        "Avg Switch (ms)", "Std Switch", 
        "Avg Other (ms)", "Std Other", 
        "Avg Switch Count", "Std Switch Count",
        "Avg Commit After Switch", "Std Commit After Switch",
        "Avg PSCR", "Std PSCR",
        "Samples"
    ]
    
    for key, metrics in aggregated.items():
        benchmark, config, threads = key
        
        row = [benchmark, config, threads]
        
        samples = len(metrics['Commit'])
        
        for metric_name in ['Commit', 'Abort', 'Wait', 'Switch', 'Other', 'SwitchCount', 'CommitAfterSwitch', 'PSCR']:
            values = metrics[metric_name]
            avg = statistics.mean(values)
            std = statistics.stdev(values) if len(values) > 1 else 0.0
            
            if metric_name in ['PSCR']:
                 row.append(f"{avg:.6f}")
                 row.append(f"{std:.6f}")
            else:
                 row.append(f"{avg:.2f}")
                 row.append(f"{std:.2f}")
            
        row.append(samples)
        csv_rows.append(row)
        
    # Sort rows: Benchmark -> Config -> Threads
    csv_rows.sort(key=lambda x: (x[0], x[1], x[2]))
    
    with open(args.output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(csv_rows)
        
    print(f"Successfully wrote {len(csv_rows)} rows to {args.output}")

if __name__ == "__main__":
    main()
