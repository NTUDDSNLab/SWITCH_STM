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
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'rnd',CI = False,backoff = False)
        if arg == '-switch_rnd_CI':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'rnd',CI = True, backoff = False)
        if arg == '-switch_rnd_CI_backoff':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'rnd',CI = True, backoff = True)
        if arg == '-switch_seq':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'seq',CI = False,backoff = False)
        if arg == '-switch_seq_CI':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'seq',CI = True, backoff = False)
        if arg == '-switch_seq_CI_backoff':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'seq',CI = True, backoff = True)
        if arg == '-switch_laf':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'laf',CI = False,backoff = False)
        if arg == '-switch_laf_CI':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'laf',CI = True, backoff = False)
        if arg == '-switch_laf_CI_backoff':
            simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'laf',CI = True, backoff = True)

