import re
import sys
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from plot_function import *


if len(sys.argv) < 4:
    print("Usage: python generate_file_lists.py <base_path> <threads> <STM_labels1> <STM_labels2> ... <STM_labelsN>")
    sys.exit(1)
base_path = sys.argv[1]
threads = sys.argv[2].split()
STM_labels = sys.argv[3:]

file_lists = {}
datasets = {}
abort_ratios = {}
normalized_datasets = {}
for STM in STM_labels:
    file_lists[STM] = generate_file_list(base_path, STM, threads)
    datasets[STM] = [[] for _ in range(10)]
    abort_ratios[STM] = [[] for _ in range(10)]
    normalized_datasets[STM] = []
    for file_name in file_lists[STM]:
        caculate_data(file_name,datasets[STM])
        caculate_abort_ratio(file_name,abort_ratios[STM])
    normalized(datasets[STM],normalized_datasets[STM],datasets['suicide']) 

# for STM, file_list in file_lists.items():
#     print(f'{STM} file list:')
#     print(file_list)

switch_rnd_CI_backoff_avg_switch_times       = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_run_tx_times       = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_first_stage_times  = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_second_stage_times = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_switch_committed   = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_switch_aborted     = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_total_committed    = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_total_aborted      = [[] for _ in range(10)]

labels = [
    'Bayes',
    'Genome',
    'Intruder',
    'KMeans-low',
    'KMeans-high',
    'Labyrinth',
    'SSCA2',
    'Vacation-low',
    'Vacation-high',
    'Yada'
]

#draw original data
fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(15, 8))
axes = axes.flatten()
x_values_uniform = list(range(1, len(threads) + 1))
colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']  # Add more colors if needed
dataset_lists = [datasets[STM] for STM in STM_labels]

for data_group, label, ax in zip(zip(*dataset_lists), labels, axes):
    for data, STM, color in zip(data_group, STM_labels, colors[:len(STM_labels)]):
            ax.plot(x_values_uniform, data, label=STM, marker='.', linewidth=1.5, color=color)
    for tick in ax.get_yticks():
        ax.axhline(y=tick, color='lightgray', linestyle='--', linewidth=0.5)
    ax.set_xlabel('number of threads')
    ax.set_ylabel('times (second)')
    ax.set_title(label)
    ax.set_xticks(x_values_uniform)
    ax.set_xticklabels(threads)

fig.legend(labels=STM_labels,loc='upper center',bbox_to_anchor=(0.5, 1), ncol=3)
plt.tight_layout(rect=(0, 0, 1, 0.95))  # Adjust top space
plt.subplots_adjust()  # Adjust horizontal space
plt.savefig('execution_time.png',dpi=300)

#draw speed up data
fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(15, 8))
axes = axes.flatten()

normalized_datasets = [normalized_datasets[STM] for STM in STM_labels]

for data_group, label, ax in zip(zip(*normalized_datasets), labels, axes):
    for data, STM, color in zip(data_group, STM_labels, colors[:len(STM_labels)]):
        ax.plot(x_values_uniform, data, label=STM, marker='.', linewidth=1.5, color=color)
    for tick in ax.get_yticks():
        ax.axhline(y=tick, color='lightgray', linestyle='--', linewidth=0.5)
    ax.set_xlabel('number of threads')
    ax.set_ylabel('speed up')
    ax.set_title(label)
    ax.set_xticks(x_values_uniform)
    ax.set_xticklabels(threads)

fig.legend(labels=STM_labels,loc='upper center',bbox_to_anchor=(0.5, 1), ncol=3)
plt.tight_layout(rect=(0, 0, 1, 0.95))  # Adjust top space
plt.subplots_adjust()  # Adjust horizontal space
plt.savefig('speed_up.png',dpi=300)

#draw abort ratio
fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(15, 8))
axes = axes.flatten()

abort_ratios = [abort_ratios[STM] for STM in STM_labels]

for data_group, label, ax in zip(zip(*abort_ratios), labels, axes):
    for data, STM, color in zip(data_group, STM_labels, colors[:len(STM_labels)]):
        ax.plot(x_values_uniform, data, label=STM, marker='.', linewidth=1.5, color=color)
    for tick in ax.get_yticks():
        ax.axhline(y=tick, color='lightgray', linestyle='--', linewidth=0.5)
    ax.set_xlabel('number of threads')
    ax.set_ylabel('abort ratio')
    ax.set_title(label)
    ax.set_xticks(x_values_uniform)
    ax.set_xticklabels(threads)

fig.legend(labels=STM_labels,loc='upper center',bbox_to_anchor=(0.5, 1), ncol=3)
plt.tight_layout(rect=(0, 0, 1, 0.95))  # Adjust top space
plt.subplots_adjust()  # Adjust horizontal space
plt.savefig('abort_ratio.png',dpi=300)