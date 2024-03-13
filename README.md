# Switch Configuration Options
Three switch configurations are provided for selection:

1. switch_rnd: "rnd" stand for "random". The scheduler will randomly select a coroutine to execute tasks.
2. switch_seq: "seq" stands for sequence. Each coroutine has a unique identifier. The scheduler will sequentially select coroutines to execute tasks, where the coroutine following the one with the highest identifier will be the first coroutine to execute next.
3. switch_laf: "laf" stands for less abort first. Each coroutine has an independent abort counter. The scheduler will select the coroutine with the lowest current abort count to execute tasks.

# Additional Configuration for Each Switch Configuration (switch_STM)
For each switch configuration, the following additional configurations can be added:

1. CI: Utilizes Contention Intensity to calculate the current conflict level. If the conflicts exceed a threshold, the scheduler will temporarily pause switching until the Contention Intensity drops below the threshold.
2. CI_backoff: In addition to pausing switching when conflicts are too high, this configuration also involves a random backoff period when an abort occurs. The maximum duration of this random backoff is proportional to the number of threads.

This heuristic is devised because when there are too many conflicts, executing transactions may result in aborts not only due to conflicts within the transaction itself but also due to causing other transactions to abort, leading to an increase in the abort ratio. The random backoff mechanism is implemented to avoid encountering the same transaction repeatedly, which could lead to cyclic aborts.

# Usage:
To execute the STM simulation tests in the terminal, use the following command:
```bash
python3 simulation.py"
```
Use the -simulation_times flag to specify the number of simulation tests:
For example: 
```bash 
python3 simulation.py -simulation_times 10
```

Use the -thread flag to specify the number of threads to simulate:
For example: 
```bash
python3 simulation.py -thread 1 2 4 8 16
```
Use the STM flag to specify the STM to simulate.
Available flags include:
'-suicide'
'-polka'
'-shrink'
'-switch_rnd'
'-switch_rnd_CI'
'-switch_rnd_CI_backoff'
'-switch_seq'
'-switch_seq_CI'
'-switch_seq_CI_backoff'
'-switch_laf'
'-switch_laf_CI'
'-switch_laf_CI_backoff'

For example: 
```bash
python3 simulation.py -suicide -polka -switch_rnd
```

## Example:
Suppose you want to simulate all STM ten times, each with 1, 2, 4, 8, and 16 threads. Enter the following command in the terminal:
```bash
python3 simulation.py -simulation_times 10 -thread 1 2 4 8 16 -suicide -polka -shrink -switch_rnd -switch_seq -switch_laf -switch_rnd_CI -switch_seq_CI -switch_laf_CI -switch_rnd_CI_backoff -switch_seq_CI_backoff -switch_laf_CI_backoff
```