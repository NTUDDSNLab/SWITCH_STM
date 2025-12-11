import os
import re
import csv
import glob
import statistics

def parse_log_files(log_dir, output_csv='stm_results.csv'):
    # Patterns
    exec_patterns = {
        'yada': r'Executing: ./yada/yada',
        'intruder': r'Executing: ./intruder/intruder',
        'kmeans_high': r'Executing: ./kmeans/kmeans -m40 -n40',
        'kmeans_low': r'Executing: ./kmeans/kmeans -m15 -n15',
        'bayes': r'Executing: ./bayes/bayes',
        'vacation_high': r'Executing: ./vacation/vacation -n2 -q90 -u98',
        'vacation_low': r'Executing: ./vacation/vacation -n4 -q60 -u90',
        'genome': r'Executing: ./genome/genome',
        'labyrinth': r'Executing: ./labyrinth/labyrinth',
        'ssca2': r'Executing: ./ssca2/ssca2'
    }
    
    time_patterns = {
        'yada': r'Elapsed time\s+=\s+(\d+\.\d+)',
        'intruder': r'Elapsed time\s+=\s+(\d+\.\d+)',
        'kmeans_high': r'Time:\s+(\d+\.\d+)',
        'kmeans_low': r'Time:\s+(\d+\.\d+)',
        'bayes': r'Learn time\s+=\s+(\d+\.\d+)',
        'vacation_high': r'Time\s+=\s+(\d+\.\d+)',
        'vacation_low': r'Time\s+=\s+(\d+\.\d+)',
        'genome': r'Time\s+=\s+(\d+\.\d+)',
        'labyrinth': r'Elapsed time\s+=\s+(\d+\.\d+)',
        'ssca2': r'Time taken for all is\s+(\d+\.\d+)'
    }

    results = {}

    log_files = glob.glob(os.path.join(log_dir, "*.stm"))
    if not log_files:
        print(f"No .stm files found in {log_dir}")
        return

    print(f"Found {len(log_files)} log files.")

    for log_file in log_files:
        filename = os.path.basename(log_file)
        # Parse config and threads from filename: e.g., suicide_16.stm
        # Assuming format: config_threads.stm
        try:
            base_name = filename.replace('.stm', '')
            parts = base_name.split('_')
            # Attempt to find the last part that is a number
            if parts[-1].isdigit():
                threads = int(parts[-1])
                config = "_".join(parts[:-1])
            else:
                # Fallback if naming convention differs
                threads = -1
                config = base_name
        except Exception as e:
            print(f"Skipping malformed filename: {filename} ({e})")
            continue

        try:
            with open(log_file, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {log_file}: {e}")
            continue
        
        # Find all benchmark starts
        starts = []
        for name, pattern in exec_patterns.items():
            for match in re.finditer(pattern, content):
                starts.append((match.start(), name))
        
        starts.sort()
        
        for i in range(len(starts)):
            start_idx, benchmark_name = starts[i]
            # End of this chunk is the start of next benchmark or EOF
            end_idx = starts[i+1][0] if i + 1 < len(starts) else len(content)
            chunk = content[start_idx:end_idx]
            
            # Extract Time
            time_match = re.search(time_patterns[benchmark_name], chunk)
            if not time_match:
                # Might be an error or interrupted run
                continue 
            
            exe_time = float(time_match.group(1))
            
            # Extract Commits/Aborts
            commits = 0
            aborts = 0
            
            # Method 1: TM_STATISTICS (Thread ... | commits: ... aborts: ...)
            thread_stats = re.findall(r'Thread\s+\w+\s*\|\s*commits:\s*(\d+)\s+aborts:\s*(\d+)', chunk)
            
            if thread_stats:
                for c, a in thread_stats:
                    commits += int(c)
                    aborts += int(a)
            else:
                # Method 2: TM_STATISTICS3 (committed:..., aborted:...)
                global_stats = re.findall(r'committed:\s*(\d+),\s*aborted:\s*(\d+)', chunk)
                if global_stats:
                    for c, a in global_stats:
                        commits += int(c)
                        aborts += int(a)
            
            # Store result
            if benchmark_name not in results: results[benchmark_name] = {}
            if config not in results[benchmark_name]: results[benchmark_name][config] = {}
            if threads not in results[benchmark_name][config]: results[benchmark_name][config][threads] = []
            
            results[benchmark_name][config][threads].append({
                'time': exe_time,
                'commits': commits,
                'aborts': aborts
            })

    # Write CSV
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Header
            writer.writerow(['Benchmark', 'Configuration', 'Threads', 'Avg Execution Time (s)', 'Time Std Dev', 'Abort Rate', 'Avg Commits', 'Avg Aborts', 'Samples'])
            
            # Sort keys for consistent output
            for bench in sorted(results.keys()):
                bench_data = results[bench]
                for conf in sorted(bench_data.keys()):
                    conf_data = bench_data[conf]
                    for thr in sorted(conf_data.keys()):
                        runs = conf_data[thr]
                        
                        times = [r['time'] for r in runs]
                        avg_time = statistics.mean(times)
                        std_time = statistics.stdev(times) if len(times) > 1 else 0.0
                        
                        avg_commits = statistics.mean([r['commits'] for r in runs])
                        avg_aborts = statistics.mean([r['aborts'] for r in runs])
                        
                        total_events = avg_commits + avg_aborts
                        abort_rate = avg_aborts / total_events if total_events > 0 else 0.0
                        
                        writer.writerow([bench, conf, thr, f"{avg_time:.4f}", f"{std_time:.4f}", f"{abort_rate:.4f}", f"{avg_commits:.1f}", f"{avg_aborts:.1f}", len(runs)])
        
        print(f"Successfully wrote results to {output_csv}")
        
    except Exception as e:
        print(f"Error writing CSV: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parse STM log files and generate a CSV report.")
    parser.add_argument("log_dir", nargs='?', default="./log", help="Directory containing .stm log files")
    parser.add_argument("--output", default="stm_results.csv", help="Output CSV filename")
    args = parser.parse_args()

    # Pass output filename to parse_log_files if we were to refactor it to accept it, 
    # but the current function hardcodes it. 
    # Let's verify if parse_log_files needs modification for output file.
    # It does: output_csv = 'stm_results.csv' is inside the function.
    # So I should also modify the function signature or just let it be if I can't change the function signature easily in this Replace block.
    # However, for a good CLI, I should probably pass it.
    
    # Wait, I can't change the function signature and the main block in one Replace call if they are far apart.
    # The prompt asks me to replace the main block. 
    # I will modify the function to accept output_csv argument in a separate call or just hack it here if I were lazy, but I will do it properly.
    
    # First, let's just make the main block call parse_log_files with the dir.
    # But wait, `parse_log_files` as defined in the file DOES NOT accept output_csv. 
    # It hardcodes `output_csv = 'stm_results.csv'`.
    
    # So I will just update the main block to call it with the directory for now.
    parse_log_files(args.log_dir, args.output)
