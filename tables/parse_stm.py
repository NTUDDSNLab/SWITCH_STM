import re
import sys
import statistics

def parse_stm_file(file_path):
    benchmarks = {
        'yada': r'Executing: ./yada/yada.*?Elapsed time\s+=\s+(\d+\.\d+)',
        'intruder': r'Executing: ./intruder/intruder.*?Elapsed time\s+=\s+(\d+\.\d+)',
        'kmeans_high': r'Executing: ./kmeans/kmeans -m40 -n40.*?Time:\s+(\d+\.\d+)',
        'kmeans_low': r'Executing: ./kmeans/kmeans -m15 -n15.*?Time:\s+(\d+\.\d+)',
        'bayes': r'Executing: ./bayes/bayes.*?Learn time\s+=\s+(\d+\.\d+)',
        'vacation_high': r'Executing: ./vacation/vacation -n2 -q90 -u98.*?Time\s+=\s+(\d+\.\d+)',
        'vacation_low': r'Executing: ./vacation/vacation -n4 -q60 -u90.*?Time\s+=\s+(\d+\.\d+)',
        'genome': r'Executing: ./genome/genome.*?Time\s+=\s+(\d+\.\d+)',
        'labyrinth': r'Executing: ./labyrinth/labyrinth.*?Elapsed time\s+=\s+(\d+\.\d+)',
        'ssca2': r'Executing: ./ssca2/ssca2.*?Time taken for all is\s+(\d+\.\d+)'
    }

    error_patterns = {
        'timeout': r'Timeout',
        'segfault': r'Segmentation fault',
        'assertion': r'Assertion.*failed',
        'other_error': r'Error:|Exception:'
    }

    results = {}

    with open(file_path, 'r') as file:
        content = file.read()

        for benchmark, pattern in benchmarks.items():
            times = []
            errors = []

            # Find all occurrences of the benchmark
            matches = re.finditer(pattern, content, re.DOTALL)
            
            for match in matches:
                occurrence_text = match.group(0)
                
                # Check for errors
                error_found = False
                for error_type, error_pattern in error_patterns.items():
                    if re.search(error_pattern, occurrence_text, re.IGNORECASE):
                        errors.append(error_type)
                        error_found = True
                        break
                
                if not error_found:
                    # If no error, extract the time
                    time_match = re.search(r'\d+\.\d+', match.group(1))
                    if time_match:
                        times.append(float(time_match.group()))
                    else:
                        errors.append('no_time_found')

            # Calculate time statistics
            time_stats = {}
            if times:
                time_stats = {
                    'avg': statistics.mean(times),
                    'std': statistics.stdev(times) if len(times) > 1 else 0,
                    'max': max(times),
                    'min': min(times),
                    'count': len(times)
                }

            # Calculate error statistics
            error_counts = {}
            for error in errors:
                error_counts[error] = error_counts.get(error, 0) + 1

            error_stats = {
                'total': len(errors),
                'types': error_counts
            }

            results[benchmark] = {
                'time_stats': time_stats,
                'error_stats': error_stats
            }

    return results

def print_results(results):
    for benchmark, data in results.items():
        print(f"{benchmark}:")
        
        time_stats = data['time_stats']
        error_stats = data['error_stats']
        
        print(f"  Time Statistics:")
        if time_stats:
            print(f"    Count: {time_stats['count']}")
            print(f"    Average: {time_stats['avg']:.6f} seconds")
            print(f"    Std Dev: {time_stats['std']:.6f} seconds")
            print(f"    Max: {time_stats['max']:.6f} seconds")
            print(f"    Min: {time_stats['min']:.6f} seconds")
        else:
            print("    No successful executions")
        
        print(f"  Error Statistics:")
        print(f"    Total Errors: {error_stats['total']}")
        if error_stats['types']:
            print(f"    Error Types:")
            for error_type, count in error_stats['types'].items():
                print(f"      - {error_type}: {count}")
        else:
            print("    No errors encountered")
        
        print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_stm.py <path_to_stm_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    results = parse_stm_file(file_path)
    print_results(results)
