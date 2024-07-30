import re
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from plot_function import caculate_data, switch_data_record, normalized ,caculate_abort_ratio

x_values = [1,2,4,8,16,32]
STM_labels = ['suicide', 'polka', 'shrink', 'switch_rnd_CI_backoff']

file_list0 = ['data0/suicide_1.stm'
            , 'data0/suicide_2.stm'
            , 'data0/suicide_4.stm'
            , 'data0/suicide_8.stm'
            , 'data0/suicide_16.stm'
            , 'data0/suicide_32.stm'
            ]

file_list1 = ['data0/polka_1.stm'
            , 'data0/polka_2.stm'
            , 'data0/polka_4.stm'
            , 'data0/polka_8.stm'
            , 'data0/polka_16.stm'
            , 'data0/polka_32.stm'
            ]

file_list2 = ['data0/shrink_1.stm'
            , 'data0/shrink_2.stm'
            , 'data0/shrink_4.stm'
            , 'data0/shrink_8.stm'
            , 'data0/shrink_16.stm'
            , 'data0/shrink_32.stm'
            ]

file_list3 = ['data0/suicide_1.stm'
            , 'data0/switch_rnd_CI_2.stm'
            , 'data0/switch_rnd_CI_4.stm'
            , 'data0/switch_rnd_CI_8.stm'
            , 'data0/switch_rnd_CI_16.stm'
            , 'data0/switch_rnd_CI_32.stm'
            ]

datasets0 = [[] for _ in range(10)]
datasets1 = [[] for _ in range(10)]
datasets2 = [[] for _ in range(10)]
datasets3 = [[] for _ in range(10)]

abort_ratios_0 = [[] for _ in range(10)]
abort_ratios_1 = [[] for _ in range(10)]
abort_ratios_2 = [[] for _ in range(10)]
abort_ratios_3 = [[] for _ in range(10)]

# start suicide data
for file_name in file_list0:
    caculate_data(file_name,datasets0)
    caculate_abort_ratio(file_name,abort_ratios_0)
# end suicide data   

# start polka data
for file_name in file_list1:
    caculate_data(file_name,datasets1) 
    caculate_abort_ratio(file_name,abort_ratios_1)
# end polka data    

# start shrink data
for file_name in file_list2:
    caculate_data(file_name,datasets2) 
    caculate_abort_ratio(file_name,abort_ratios_2)
# end switch_rnd data  

# start switch_rnd_CI_backoff data
for file_name in file_list3:
    caculate_data(file_name,datasets3) 
    caculate_abort_ratio(file_name,abort_ratios_3)
# end switch_rnd data  

switch_rnd_CI_backoff_avg_switch_times       = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_run_tx_times       = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_first_stage_times  = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_second_stage_times = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_switch_committed   = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_switch_aborted     = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_total_committed    = [[] for _ in range(10)]
switch_rnd_CI_backoff_avg_total_aborted      = [[] for _ in range(10)]

# record data for switch 
for file_name in file_list3:
    switch_data_record(file_name,
                       switch_rnd_CI_backoff_avg_switch_times,
                       switch_rnd_CI_backoff_avg_run_tx_times,
                       switch_rnd_CI_backoff_avg_first_stage_times,
                       switch_rnd_CI_backoff_avg_second_stage_times,
                       switch_rnd_CI_backoff_avg_switch_committed,
                       switch_rnd_CI_backoff_avg_switch_aborted,
                       switch_rnd_CI_backoff_avg_total_committed,
                       switch_rnd_CI_backoff_avg_total_aborted)
# end recording data

# adjust data
for data1, data2, data3, data0 in zip(datasets1,datasets2, datasets3, datasets0):
    data1[0] = data0[0]
    data2[0] = data0[0]
    data3[0] = data0[0]

normalized_datasets0 = []
normalized_datasets1 = []
normalized_datasets2 = []
normalized_datasets3 = []

normalized (datasets0,normalized_datasets0,datasets0)
normalized (datasets1,normalized_datasets1,datasets0)
normalized (datasets2,normalized_datasets2,datasets0)
normalized (datasets3,normalized_datasets3,datasets0)

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
x_values_uniform = list(range(1, len(x_values) + 1))

for data0, data1, data2, data3, label, ax in zip(datasets0, datasets1, datasets2, datasets3, labels, axes):
    ax.plot(x_values_uniform, data0,label='suicide'                 ,marker='.',linewidth=1.5,color='blue'  )
    ax.plot(x_values_uniform, data1,label='polka'                   ,marker='.',linewidth=1.5,color='orange')
    ax.plot(x_values_uniform, data2,label='shrink'                  ,marker='.',linewidth=1.5,color='green' )
    ax.plot(x_values_uniform, data3,label='switch_rnd_CI_backoff'   ,marker='.',linewidth=1.5,color='red'   )
    for tick in ax.get_yticks():
        ax.axhline(y=tick, color='lightgray', linestyle='--', linewidth=0.5)
    ax.set_xlabel('number of threads')
    ax.set_ylabel('times (second)')
    ax.set_title(label)
    ax.set_xticks(x_values_uniform)
    ax.set_xticklabels(x_values)

fig.legend(labels=STM_labels,loc='upper center',bbox_to_anchor=(0.5, 1), ncol=3)
plt.tight_layout(rect=(0, 0, 1, 0.95))  # Adjust top space
plt.subplots_adjust()  # Adjust horizontal space
plt.savefig('execution_time.png',dpi=300)

#draw speed up data
fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(15, 8))
axes = axes.flatten()

for data0, data1, data2, data3, label, ax in zip(normalized_datasets0,  normalized_datasets1, normalized_datasets2, normalized_datasets3, labels, axes):
    ax.plot(x_values_uniform, data0,label='suicide'                 ,marker='.',linewidth=1.5,color='blue'  )
    ax.plot(x_values_uniform, data1,label='polka'                   ,marker='.',linewidth=1.5,color='orange')
    ax.plot(x_values_uniform, data2,label='shrink'                  ,marker='.',linewidth=1.5,color='green' )
    ax.plot(x_values_uniform, data3,label='switch_rnd_CI_backoff'   ,marker='.',linewidth=1.5,color='red'   )
    for tick in ax.get_yticks():
        ax.axhline(y=tick, color='lightgray', linestyle='--', linewidth=0.5)
    ax.set_xlabel('number of threads')
    ax.set_ylabel('speed up')
    ax.set_title(label)
    ax.set_xticks(x_values_uniform)
    ax.set_xticklabels(x_values)

fig.legend(labels=STM_labels,loc='upper center',bbox_to_anchor=(0.5, 1), ncol=3)
plt.tight_layout(rect=(0, 0, 1, 0.95))  # Adjust top space
plt.subplots_adjust()  # Adjust horizontal space
plt.savefig('speed_up.png',dpi=300)

#draw abort ratio
fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(15, 8))
axes = axes.flatten()

for data0, data1, data2, data3, label, ax in zip(abort_ratios_0,  abort_ratios_1, abort_ratios_2, abort_ratios_3, labels, axes):
    ax.plot(x_values_uniform, data0,label='suicide'                 ,marker='.',linewidth=1.5,color='blue'  )
    ax.plot(x_values_uniform, data1,label='polka'                   ,marker='.',linewidth=1.5,color='orange')
    ax.plot(x_values_uniform, data2,label='shrink'                  ,marker='.',linewidth=1.5,color='green' )
    ax.plot(x_values_uniform, data3,label='switch_rnd_CI_backoff'   ,marker='.',linewidth=1.5,color='red'   )
    for tick in ax.get_yticks():
        ax.axhline(y=tick, color='lightgray', linestyle='--', linewidth=0.5)
    ax.set_xlabel('number of threads')
    ax.set_ylabel('abort ratio')
    ax.set_title(label)
    ax.set_xticks(x_values_uniform)
    ax.set_xticklabels(x_values)

fig.legend(labels=STM_labels,loc='upper center',bbox_to_anchor=(0.5, 1), ncol=3)
plt.tight_layout(rect=(0, 0, 1, 0.95))  # Adjust top space
plt.subplots_adjust()  # Adjust horizontal space
plt.savefig('abort_ratio.png',dpi=300)