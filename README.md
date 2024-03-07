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