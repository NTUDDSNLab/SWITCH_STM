try:
    import sys
except ImportError:
    print("Error: Package 'sys' not found or failed to import.")

from simulation_function import parse_threads_list
from simulation_function import parse_simulation_times
from simulation_function import simulate_suicide
from simulation_function import simulate_polka
from simulation_function import simulate_shrink
from simulation_function import simulate_switch_stm

simulation_times = parse_simulation_times()
threads_list = parse_threads_list()

print(f"simulation_times = {simulation_times}, threads_list = {threads_list}")

for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg == '-suicide':
            simulate_suicide(simulation_times,threads_list)
        if arg == '-polka':
            simulate_polka(simulation_times,threads_list)
        if arg == '-shrink':
            simulate_shrink(simulation_times,threads_list)

        if arg == '-switch_rnd':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'rnd',CI = False ,TP = False)
        if arg == '-switch_rnd_CI':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'rnd',CI = True ,TP = False)
        if arg == '-switch_rnd_CI_TP':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'rnd',CI = True ,TP = True)
        if arg == '-switch_rnd_TP':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'rnd',CI = False ,TP = True)
        
        if arg == '-switch_seq':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'seq',CI = False ,TP = False)
        if arg == '-switch_seq_CI':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'seq',CI = True ,TP = False)
        if arg == '-switch_seq_CI_TP':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'seq',CI = True ,TP = True)
        if arg == '-switch_seq_TP':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'seq',CI = False ,TP = True)
        
        if arg == '-switch_laf':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'laf',CI = False ,TP = False)
        if arg == '-switch_laf_CI':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'laf',CI = True ,TP = False)
        if arg == '-switch_laf_CI_TP':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'laf',CI = True ,TP = True)
        if arg == '-switch_laf_TP':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'laf',CI = False ,TP = True)
        
