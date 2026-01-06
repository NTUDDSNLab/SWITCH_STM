import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="""Description:
    This script generates stacked bar plots showing time breakdown from STM profile data.
    It creates a 2x5 grid of plots, one for each benchmark, showing the breakdown of 
    execution time into components: Other, Wait, Abort, Switch (for switch_laf_CI only), and Commit.""",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Examples:
    # Generate plot with default settings
    python3 plot/breakdown_plot.py
    
    # Specify custom input and output files
    python3 plot/breakdown_plot.py tables/raw_data/128_prof_bkt_swt.csv -o my_breakdown.png
    
    # Adjust bar width
    python3 plot/breakdown_plot.py -o breakdown.png --width 0.15"""
    )

    parser.add_argument('csv_file', nargs='?', 
                        default='tables/raw_data/128_prof_bkt_swt.csv',
                        help="Path to the CSV file containing profile data.")
    parser.add_argument('-o', '--output', default='time_breakdown_stack.png', 
                        help="Output filename.")
    parser.add_argument('--width', type=float, default=0.5,
                        help="Width of each bar in the grouped bar chart. Default: 0.5")

    args = parser.parse_args()

    csv_file = args.csv_file
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)

    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Clean up column names
    df.columns = df.columns.str.strip()

    # Required columns
    required_columns = ['Benchmark', 'Configuration', 'Threads',
                        'Avg Commit (ms)', 'Avg Abort (ms)', 'Avg Wait (ms)', 
                        'Avg Switch (ms)', 'Avg Other (ms)']

    for col in required_columns:
        if col not in df.columns:
            print(f"Error: Missing column '{col}' in CSV.")
            sys.exit(1)

    # Filter to only keep the 5 configurations we want
    target_configs = ['ats', 'polka', 'shrink', 'suicide', 'switch_laf_CI']
    df = df[df['Configuration'].isin(target_configs)].copy()

    if df.empty:
        print("Error: No data found for target configurations.")
        sys.exit(1)

    # Get unique benchmarks
    benchmarks = sorted(df['Benchmark'].unique())
    num_benchmarks = len(benchmarks)

    # Define colors for each time component
    colors = {
        'Other': '#E8E8E8',    # Light gray
        'Wait': '#FFD700',      # Gold
        'Abort': '#FF6B6B',     # Red
        'Commit': '#4CAF50',    # Green
        'Switch': '#2196F3'     # Blue
    }

    # Fixed 2x5 layout
    cols = 5
    rows = 2
    
    fig, axes = plt.subplots(rows, cols, figsize=(20, 8), sharey=False)
    axes = axes.flatten()

    # Bar width and positions
    bar_width = args.width
    num_configs = len(target_configs)
    
    # Collect handles and labels for the global legend
    legend_handles = []
    legend_labels = []
    seen_labels = set()

    for i in range(len(axes)):
        ax = axes[i]
        
        if i < num_benchmarks:
            benchmark = benchmarks[i]
            bench_data = df[df['Benchmark'] == benchmark].copy()
            
            # Ensure configurations are in the order we want
            bench_data['Config_Order'] = bench_data['Configuration'].map(
                {config: idx for idx, config in enumerate(target_configs)}
            )
            bench_data = bench_data.sort_values('Config_Order')
            
            # Get the configurations present in this benchmark
            configs_present = [c for c in target_configs if c in bench_data['Configuration'].values]
            
            # Calculate x positions for grouped bars
            x_positions = np.arange(len(configs_present))
            
            # Plot stacked bars for each configuration
            for idx, config in enumerate(configs_present):
                config_data = bench_data[bench_data['Configuration'] == config].iloc[0]
                
                x = x_positions[idx]
                
                # Get time components
                other = config_data['Avg Other (ms)']
                wait = config_data['Avg Wait (ms)']
                abort = config_data['Avg Abort (ms)']
                commit = config_data['Avg Commit (ms)']
                switch = config_data['Avg Switch (ms)']
                
                # Stack from bottom to top: Other, Wait, Abort, Commit, (Switch for switch_laf_CI)
                bottom = 0
                
                # Other
                bar_other = ax.bar(x, other, bar_width, bottom=bottom, 
                                   color=colors['Other'], edgecolor='black', linewidth=0.5,
                                   label='Other' if 'Other' not in seen_labels else '')
                if 'Other' not in seen_labels:
                    legend_handles.append(bar_other)
                    legend_labels.append('Other')
                    seen_labels.add('Other')
                bottom += other
                
                # Wait
                bar_wait = ax.bar(x, wait, bar_width, bottom=bottom,
                                  color=colors['Wait'], edgecolor='black', linewidth=0.5,
                                  label='Wait' if 'Wait' not in seen_labels else '')
                if 'Wait' not in seen_labels:
                    legend_handles.append(bar_wait)
                    legend_labels.append('Wait')
                    seen_labels.add('Wait')
                bottom += wait
                
                # Abort
                bar_abort = ax.bar(x, abort, bar_width, bottom=bottom,
                                   color=colors['Abort'], edgecolor='black', linewidth=0.5,
                                   label='Abort' if 'Abort' not in seen_labels else '')
                if 'Abort' not in seen_labels:
                    legend_handles.append(bar_abort)
                    legend_labels.append('Abort')
                    seen_labels.add('Abort')
                bottom += abort
                
                # Switch (only for switch_laf_CI) - placed between Abort and Commit
                if config == 'switch_laf_CI' and switch > 0:
                    bar_switch = ax.bar(x, switch, bar_width, bottom=bottom,
                                        color=colors['Switch'], edgecolor='black', linewidth=0.5,
                                        label='Switch' if 'Switch' not in seen_labels else '')
                    if 'Switch' not in seen_labels:
                        legend_handles.append(bar_switch)
                        legend_labels.append('Switch')
                        seen_labels.add('Switch')
                    bottom += switch
                
                # Commit
                bar_commit = ax.bar(x, commit, bar_width, bottom=bottom,
                                    color=colors['Commit'], edgecolor='black', linewidth=0.5,
                                    label='Commit' if 'Commit' not in seen_labels else '')
                if 'Commit' not in seen_labels:
                    legend_handles.append(bar_commit)
                    legend_labels.append('Commit')
                    seen_labels.add('Commit')
                bottom += commit
            
            # Configure subplot
            ax.set_title(benchmark, fontsize=24)
            ax.set_xticks(x_positions)
            # Replace switch_laf_CI with 'switch' for display
            display_labels = ['switch' if c == 'switch_laf_CI' else c for c in configs_present]
            ax.set_xticklabels(display_labels, rotation=45, ha='right', fontsize=12)
            ax.tick_params(axis='y', which='major', labelsize=16)
            ax.grid(True, axis='y', alpha=0.3)
        else:
            # Hide unused subplots
            fig.delaxes(ax)

    # Unified Legend at the top
    fig.legend(legend_handles, legend_labels, loc='upper center', 
               bbox_to_anchor=(0.5, 1.05), ncol=len(legend_labels), 
               frameon=False, fontsize=20)

    # Unified Axis Labels
    fig.text(0.5, 0.01, 'Configuration', ha='center', va='center', fontsize=24)
    fig.text(0.005, 0.5, 'Time (ms)', ha='center', va='center', rotation='vertical', fontsize=24)

    plt.tight_layout(rect=[0.02, 0.03, 1, 0.95])
    
    output_file = args.output
    plt.savefig(output_file, bbox_inches='tight', dpi=600)
    print(f"Plot saved to '{output_file}'")

if __name__ == "__main__":
    main()

