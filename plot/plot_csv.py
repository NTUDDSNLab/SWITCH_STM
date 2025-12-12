import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="""Description:
    This script generates execution time plots from a CSV file containing benchmark results.
    It creates a 2x5 grid of plots, one for each benchmark, showing execution time vs threads.""",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Examples:
    # Plot all configurations from data.csv
    python3 plot/plot_csv.py data.csv

    # Plot only 'suicide' and 'switch_rnd' configurations
    python3 plot/plot_csv.py data.csv suicide switch_rnd
    
    # Save to custom file
    python3 plot/plot_csv.py data.csv -o my_plot.png"""
    )

    parser.add_argument('csv_file', help="Path to the CSV file containing the data.")
    parser.add_argument('configs', nargs='*', help="Optional list of configurations to plot.")
    parser.add_argument('-o', '--output', default='execution_time_results.png', help="Output filename.")
    parser.add_argument('-m', '--metric', choices=['time', 'abort'], default='time', help="Metric to plot: 'time' (Execution Time) or 'abort' (Abort Ratio). Default is 'time'.")

    args = parser.parse_args()

    csv_file = args.csv_file
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)

    target_configs = args.configs

    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Clean up column names
    df.columns = df.columns.str.strip()

    # Required columns
    common_columns = ['Benchmark', 'Configuration', 'Threads']
    if args.metric == 'time':
        required_columns = common_columns + ['Avg Execution Time (s)']
    elif args.metric == 'abort':
        required_columns = common_columns + ['Avg Commits', 'Avg Aborts']

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
                
                if args.metric == 'time':
                    y_vals = config_data['Avg Execution Time (s)'] * 1000
                elif args.metric == 'abort':
                    commits = config_data['Avg Commits']
                    aborts = config_data['Avg Aborts']
                    # Calculate Abort Ratio: #abort / (#abort + #commit)
                    y_vals = aborts / (aborts + commits)
                
                line, = ax.plot(x_vals, y_vals, marker='o', label=config)
                
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
    if args.metric == 'time':
        y_label = 'Execution Time (ms)'
    elif args.metric == 'abort':
        y_label = 'Abort Ratio'
    fig.text(0.005, 0.5, y_label, ha='center', va='center', rotation='vertical', fontsize=24)

    plt.tight_layout(rect=[0.02, 0.03, 1, 0.95]) # Adjust rect to make room for labels
    
    output_file = args.output
    plt.savefig(output_file, bbox_inches='tight')
    print(f"Plot saved to '{output_file}'")

if __name__ == "__main__":
    main()
