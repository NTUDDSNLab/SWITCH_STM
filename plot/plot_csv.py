import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def print_help():
    help_text = """
Usage: python3 plot_csv.py <csv_file> [config1 config2 ...]

Description:
    This script generates execution time plots from a CSV file containing benchmark results.
    It creates a 2x5 grid of plots, one for each benchmark, showing execution time vs threads.

Arguments:
    <csv_file>      Path to the CSV file containing the data.
                    The CSV must have the following columns:
                    - 'Benchmark'
                    - 'Configuration'
                    - 'Threads'
                    - 'Avg Execution Time (s)'
    
    [config1 ...]   Optional list of configurations to plot.
                    If provided, only these configurations will be included in the plots.
                    If omitted, all configurations found in the CSV will be plotted.

Output:
    Saves the plot as 'execution_time_results.png' in the current directory.

Examples:
    # Plot all configurations from data.csv
    python3 plot/plot_csv.py data.csv

    # Plot only 'suicide' and 'switch_rnd' configurations
    python3 plot/plot_csv.py data.csv suicide switch_rnd
"""
    print(help_text)

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        print_help()
        sys.exit(0 if len(sys.argv) > 1 else 1)

    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)

    target_configs = []
    if len(sys.argv) > 2:
        target_configs = sys.argv[2:]

    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Clean up column names
    df.columns = df.columns.str.strip()

    # Required columns
    required_columns = ['Benchmark', 'Configuration', 'Threads', 'Avg Execution Time (s)']
    for col in required_columns:
        if col not in df.columns:
            print(f"Error: Missing column '{col}' in CSV.")
            sys.exit(1)

    # Unique benchmarks
    benchmarks = sorted(df['Benchmark'].unique())
    num_benchmarks = len(benchmarks)

    # Get all unique thread counts across the entire dataset to ensure consistent x-axis
    global_threads = sorted(df['Threads'].unique())
    thread_map = {t: i for i, t in enumerate(global_threads)}

    # Fixed 2x5 layout
    cols = 5
    rows = 2
    
    # Adjust figure size for 5 columns
    fig, axes = plt.subplots(rows, cols, figsize=(20, 8), sharex=True, sharey=False)
    axes = axes.flatten()

    # Collect handles and labels for the global legend
    handles = []
    labels = []
    seen_labels = set()

    for i in range(len(axes)):
        ax = axes[i]
        
        if i < num_benchmarks:
            benchmark = benchmarks[i]
            bench_data = df[df['Benchmark'] == benchmark]
            
            # Unique configurations for this benchmark
            configs = sorted(bench_data['Configuration'].unique())
            
            # Filter specific configs if requested
            if target_configs:
                configs = [c for c in configs if c in target_configs]
            
            for config in configs:
                config_data = bench_data[bench_data['Configuration'] == config].sort_values('Threads')
                threads = config_data['Threads']
                # Map threads to indices for equidistant plotting
                x_vals = threads.map(thread_map)
                exec_time_ms = config_data['Avg Execution Time (s)'] * 1000
                
                line, = ax.plot(x_vals, exec_time_ms, marker='o', label=config)
                
                if config not in seen_labels:
                    handles.append(line)
                    labels.append(config)
                    seen_labels.add(config)

            ax.set_title(benchmark, fontsize=24)
            ax.grid(True)
            ax.tick_params(axis='both', which='major', labelsize=16)
            ax.set_xticks(range(len(global_threads)))
            ax.set_xticklabels(global_threads)
        else:
            # Hide unused subplots
            fig.delaxes(ax)

    # Unified Legend at the top
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=len(labels), frameon=False, fontsize=20)

    # Unified Axis Labels
    fig.text(0.5, 0.01, 'Threads', ha='center', va='center', fontsize=24)
    fig.text(0.005, 0.5, 'Execution Time (ms)', ha='center', va='center', rotation='vertical', fontsize=24)

    plt.tight_layout(rect=[0.02, 0.03, 1, 0.95]) # Adjust rect to make room for labels
    
    output_file = 'execution_time_results.png'
    plt.savefig(output_file, bbox_inches='tight')
    print(f"Plot saved to '{output_file}'")

if __name__ == "__main__":
    main()
