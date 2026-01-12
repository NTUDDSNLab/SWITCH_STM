# SwitchSTM: Enabling Transaction Switch in Loop-based Software Transactional Memory Applications via Coroutines

SwitchSTM enables **transaction switch** built on the top of [TinySTM](https://github.com/patrickmarlier/tinystm). 
SwitchSTM aims to address the furtile stall issue with lightweight coroutine switching.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Running Simulations](#running-simulations)
    - [Command Syntax](#command-syntax)
    - [Available STM Labels](#available-stm-labels)
    - [Examples](#examples)
- [Switch Strategies](#switch-strategies)
    - [Base Strategies](#base-strategies)
    - [Additional Configurations](#additional-configurations)
    - [Recommended Flags](#recommended-flags)
- [Analysis and Plotting](#analysis-and-plotting)
    - [Plotting Comparison Results (plot.py)](#plotting-comparison-results-plotpy)
    - [Analyzing Benchmark Results (parse_stm.py)](#analyzing-benchmark-results-parsestmpy)
    - [Profiling Execution Time Breakdown](#profiling-execution-time-breakdown)
    - [Generating and Plotting CSV Data](#generating-and-plotting-csv-data)
- [Development Guide](#development-guide)
    - [Project Structure](#project-structure)
    - [Makefile Configuration](#makefile-configuration)
    - [Adding a New Strategy](#adding-a-new-strategy)

---

## Requirements
- GNU gcc/g++ version >= 9.4.0
- make
- [libaco](https://github.com/hnes/libaco)

## Installation
Clone this repository with all submodules:
```bash
git clone --recurse-submodules https://github.com/NTUDDSNLab/SWITCH_STM.git
```

## Running Simulations

The primary entry point is `simulation.py`, which automates the build and execution process.

### Command Syntax

```bash
python3 simulation.py -simulation_times <N> -threads_list "<threads>" -log_path <path> <STM_labels>
```

| Argument | Description | Default |
|:---|:---|:---|
| `-simulation_times` | Number of times to run the simulation. | 1 |
| `-threads_list` | Space-separated list of thread counts (e.g., "1 2 4"). | "1" |
| `-log_path` | Directory to store log files. | "./log" |
| `<STM_labels>` | List of STM strategies to simulate (see below). | |

### Available STM Labels
**Baselines:**
- `-suicide`
- `-polka`
- `-shrink`
- `-ats`

**SWITCH_STM Variants:**
- `switch_rnd`: Random switch
- `switch_seq`: Sequential switch
- `switch_laf`: Less Abort First
- *Suffixes*: `_CI` (Contention Intensity), `_TP` (Time Profiling)
  - e.g., `-switch_rnd_CI`, `-switch_seq_TP`, `-switch_laf_CI_TP`

### Examples

**1. Basic Run:**
Run suicide, polka, and random switch strategies with 1 simulated run.
```bash
python3 simulation.py -suicide -polka -switch_rnd
```

**2. Comprehensive Simulation:**
Run 10 iterations, identifying thread scaling (1, 2, 4, 8, 16), with profiling enabled.
```bash
python3 simulation.py -simulation_times 10 -thread "1 2 4 8 16" -suicide -polka -shrink -switch_rnd_TP -switch_seq_TP
```

---

## Switch Strategies

### Base Strategies
1. **switch_rnd** ("Random"): The switcher randomly selects a coroutine to switch to.
2. **switch_seq** ("Sequential"): Coroutines are selected in specific order based on unique identifiers.
3. **switch_laf** ("Less Abort First"): Selects the coroutine with the lowest current abort count.

### Additional Configurations
Append these suffixes to the base strategy (e.g., `-switch_rnd_CI_TP`).

1. **_CI** (Contention Intensity):
   - Calculates current conflict level.
   - Switching only occurs if conflicts exceed a threshold.
   - Low contention -> direct restart (avoids switch overhead).
   
2. **_TP** (Time Profile):
   - Enables detailed time profiling (commit, abort, wait, switch time).
   - *Note: If combining with CI, place TP after CI (e.g., `_CI_TP`).*

### Recommended Flags
When compiling/running SWITCH_STM manually or verifying configuration:
- `CM=CM_SUICIDE`
- `IRREVOCABLE_ENABLED`
- `EPOCH_GC`

---

## Analysis and Plotting

### Plotting Comparison Results (`plot.py`)
Generates plots from raw log data.

**1. Prepare Data:**
Create a subfolder inside `plot/` and place your raw `.stm` log files there.

<!-- **2. Run Plotter:**
```bash
python3 plot.py <base_path> <threads_list> <STM_labels...>
```

**Example:**
```bash
python3 plot.py data0 "1 2 4 8 16 32" suicide polka shrink switch_rnd_CI
```

**Outputs (saved in `plot/`):**
- `execution_time.png`: Absolute execution time.
- `speed_up.png`: Speedup relative to the `suicide` baseline.
- `abort_ratio.png`: Abort ratio.

**Note:** The `suicide` label is required in the arguments for normalization.

### Analyzing Benchmark Results (`parse_stm.py`)
Extracts statistics (avg time, error counts) from a single `.stm` file.

```bash
python parse_stm.py path/to/your/stm_file.stm
``` -->

### Profiling Execution Time Breakdown
When `SWITCH_STM_TIME_PROFILE` is enabled (e.g., `-switch_rnd_TP`):

**1. Parse Logs:**
Use `tables/parse_profile.py` to generate a CSV summary of breakdown metrics (Commit, Abort, Wait, Switch, Other).

```bash
python3 tables/parse_profile.py --log_dir ./log --output profile_results.csv
```

### Generating and Plotting CSV Data

**1. Generate CSV from Logs:**
Convert all `.stm` logs in a directory to a single CSV file.
```bash
python3 tables/generate_csv.py [log_dir] --output stm_results.csv
```

**2. Plot from CSV:**
Use `plot/plot_csv.py` to plot data from the CSV.

```bash
# Plot execution time (default)
python3 plot/plot_csv.py stm_results.csv suicide switch_rnd

# Plot abort ratio
python3 plot/plot_csv.py stm_results.csv suicide switch_rnd -m abort
```

---

## Development Guide

### Project Structure
- **include/param.h**: Parameters for Switch_STM.
- **include/switch_table.h**: Header for switch table management.
- **src/switch_table.c**: Functions for creating/deleting switch tables and switching coroutines.
- **src/switcher.h**: Algorithm flow, initialization, and strategy logic.

### Makefile Configuration
The `simulation.py` script automatically handles these flags:
- `SWITCH_STM`: Enables SWITCH_STM functionality.
- `CONTENTION_INTENSITY`: Enables CI detection.
- `SWITCH_STM_TIME_PROFILE`: Enables detailed timing collectors.

### Adding a New Strategy
1.  **Modify `src/switcher.h`**:
    - In `switcher_decide()`, add a new `case` for your strategy.
    - Return the integer decision for the chosen coroutine.
2.  **Update `simulation_function.py`**:
    - Update `simulate_switch_stm()` to handle the new flag and map it to the code added in `switcher.h`.



