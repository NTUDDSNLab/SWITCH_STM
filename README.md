# The following files have been added to TinySTM to implement SWITCH_STM:

**include/param.h**
Some parameters for Switch_STM.

**include/switch_table.h:**
This is the header file for switch_table.c.

**src/switch_table.c:**
Contains functions for creating and deleting the switch table, includes functions used for switching coroutines.

**src/switcher.h:**
Contains the algorithm flow of the switcher entity, includes functions for initializing the switcher and constructing and executing the switch strategy.

Additionally, by searching for the 'SWITCH_STM' flag, you can find all the modifications made to the original TinySTM source files to incorporate the new functionality.

# Makefile Configuration for SWITCH_STM

We have introduced the following flags to configure the Makefile for compiling the TinySTM system with the SWITCH_STM setup:

`SWITCH_STM:`
Enables the compilation of TinySTM with the SWITCH_STM functionality.

`CONTENTION_INTENSITY:`
Enables contention intensity detection for SWITCH_STM, switching occurs only when the contention intensity exceeds a certain threshold, related parameters can be configured in include/param.h.

`SWITCH_STM_TIME_PROFILE:`
Provides additional time-related information during SWITCH_STM operations when enabled.

# Recommended Flags for Using SWITCH_STM
When using SWITCH_STM, it is recommended to include the following flags in the compilation options:

`CM=CM_SUICIDE`
`IRREVOCABLE_ENABLED`
`EPOCH_GC`

Avoid including other flags to achieve better performance with SWITCH_STM.

# To add a new switch strategy
You need to modify **src/switcher.h** and update **simulation_function.py** to incorporate the selection of the new switch strategy.

**Update src/switcher.h:**
In the switcher_decide function, add a new case for the switch strategy.
This case must return an integer decision that corresponds to the chosen coroutine.

**Modify simulation_function.py:**
Update the simulate_switch_stm function to select the newly added case code as the switch strategy.

By following these steps, you will successfully integrate a new switch strategy into the simulation framework.

# Switch Configuration Options
Three switch configurations are provided for selection:

1. **switch_rnd**: "rnd" stand for "random". The switcher will randomly select a coroutine to execute tasks.
2. **switch_seq**: "seq" stands for sequence. Each coroutine has a unique identifier. The switcher will sequentially select coroutines to execute tasks, where the coroutine following the one with the highest identifier will be the first coroutine to execute next.
3. **switch_laf**: "laf" stands for less abort first. Each coroutine has an independent abort counter. The switcher will select the coroutine with the lowest current abort count to execute tasks.

# Additional Configuration for Each Switch Configuration
For each switch configuration, the following additional configurations can be added(added directly after the specified switch_STM configuration without spacing):

1. **_CI**: Utilizes Contention Intensity to calculate the current conflict level. Switching will only be executed if the conflicts exceed a threshold. When the Contention Intensity (CI) is low, the system will directly restart the transaction, avoiding the overhead associated with switching. This ensures that in low-contention scenarios, the system can maintain high efficiency by minimizing unnecessary switching operations.

2. **_TP**: Add this to enable the time profile functionality, which provides more detailed information about the SWITCH_STM computation process. If adding this configuration also using _CI, ensure it is placed after _CI.


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
-switch_rnd_TP
-switch_rnd_CI
-switch_rnd_CI_TP
-switch_seq
-switch_seq_TP
-switch_seq_CI
-switch_seq_CI_TP
-switch_laf
-switch_laf_TP
-switch_laf_CI
-switch_laf_CI_TP
```
For example: 
```bash
python3 simulation.py -suicide -polka -switch_rnd
```

## Example:
Suppose you want to simulate all STM ten times, each with 1, 2, 4, 8, and 16 threads, and for SWITCH_STM, show more time profiles. Enter the following command in the terminal:
```bash
python3 simulation.py -simulation_times 10 -thread 1 2 4 8 16 -suicide -polka -shrink -switch_rnd_TP -switch_seq_TP -switch_laf_TP -switch_rnd_CI_TP -switch_seq_CI_TP -switch_laf_CI_TP 
```

# Plotting Comparison Results
Follow these steps to plot comparison results:

**1.Create a New Folder for Raw Data:**
In the plot folder, create a new subfolder.
Place your raw data files into this subfolder.

**2.Modify plot.py:**
Open plot.py and make the following modifications to customize the data you want to plot:

i. Modify x_values Array:
Set this array to the number of threads you want to plot. Example: from 1 to 32 threads.

ii. Modify labels Array:
Set this array to the STM configurations you want to plot. Example: there are 4 configurations.

iii. Modify file_list Array:
Set this array to the paths of the raw data files. Each STM system's data should be placed in the same file list. Example: there are 4 STM systems, each containing raw data paths for 6 different thread counts.

iv. Add or Modify Configurations:
To compare more system configurations or to plot different graphs, refer to the code and add or modify as needed.

**3.Run plot.py:**
Execute plot.py.
The generated images will be saved in the plot folder.