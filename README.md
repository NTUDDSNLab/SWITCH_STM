# Switch Configuration Options
Three switch configurations are provided for selection:

1. **switch_rnd**: "rnd" stand for "random". The switcher will randomly select a coroutine to execute tasks.
2. **switch_seq**: "seq" stands for sequence. Each coroutine has a unique identifier. The switcher will sequentially select coroutines to execute tasks, where the coroutine following the one with the highest identifier will be the first coroutine to execute next.
3. **switch_laf**: "laf" stands for less abort first. Each coroutine has an independent abort counter. The switcher will select the coroutine with the lowest current abort count to execute tasks.

# Additional Configuration for Each Switch Configuration
For each switch configuration, the following additional configurations can be added(added directly after the specified switch_STM configuration without spacing):

1. **_CI**: Utilizes Contention Intensity to calculate the current conflict level. Switching will only be executed if the conflicts exceed a threshold. When the Contention Intensity (CI) is low, the system will directly restart the transaction, avoiding the overhead associated with switching. This ensures that in low-contention scenarios, the system can maintain high efficiency by minimizing unnecessary switching operations.


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
```bash
-suicide
-polka
-shrink
-switch_rnd
-switch_rnd_CI
-switch_seq
-switch_seq_CI
-switch_laf
-switch_laf_CI
```
For example: 
```bash
python3 simulation.py -suicide -polka -switch_rnd
```

## Example:
Suppose you want to simulate all STM ten times, each with 1, 2, 4, 8, and 16 threads. Enter the following command in the terminal:
```bash
python3 simulation.py -simulation_times 10 -thread 1 2 4 8 16 -suicide -polka -shrink -switch_rnd -switch_seq -switch_laf -switch_rnd_CI -switch_seq_CI -switch_laf_CI 
```