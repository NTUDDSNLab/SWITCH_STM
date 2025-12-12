try:
    import sys
except ImportError:
    print("Error: Package 'sys' not found or failed to import.")

import os

if not os.path.exists('tinySTM'):
    print("Error: tinySTM directory not found")
    # Handle the error appropriately

if not os.path.exists('stamp-master'):
    print("Error: stamp-master directory not found")
    # Handle the error appropriately


import argparse

from simulation_function import simulate_suicide
from simulation_function import simulate_polka
from simulation_function import simulate_shrink
from simulation_function import simulate_switch_stm
from simulation_function import simulate_ats

# Function to check if a number is a power of 2
def is_power_of_two(n):
    return (n != 0) and (n & (n - 1)) == 0

# Function to validate the threads list input
def validate_threads_list(threads):
    for thread in threads:
        if not is_power_of_two(thread):
            raise ValueError(f"Invalid thread count: {thread}. Must be a power of 2.")
    return threads

# Use argparse to parse the arguments
parser = argparse.ArgumentParser(description="Run simulations for different configurations of tinySTM.")

# Add argument to parse the simulation times - the default value is 1
parser.add_argument('-simulation_times', type=int, default=1, help='Number of times to run the simulation (default: 1). \nFormat: integer')

# Add argument to parse the threads list - the default value is [1,2,4,8,16]
parser.add_argument('-threads_list', type=lambda s: list(map(int, s.split())), default=[1], help='List of threads to run the simulation (default: "1"). \nFormat: space-separated integers\ne.g. -threads_list "1 2 4 8 16"')

# Add argument for the path of the directory of the log files
parser.add_argument('-log_path', type=str, default='./log', help='Path of the directory to store the log files (default: "./log"). \nFormat: string')

# Add arguments - the default value is False
parser.add_argument('-suicide', action='store_true', help='[Configuration] Run suicide simulation')
parser.add_argument('-polka', action='store_true', help='[Configuration] Run polka simulation')
parser.add_argument('-shrink', action='store_true', help='[Configuration] Run shrink simulation')
parser.add_argument('-ats', action='store_true', help='[Configuration] Run ats simulation')
parser.add_argument('-switch_rnd', action='store_true', help='[Configuration] Run switch_rnd simulation')
parser.add_argument('-switch_rnd_CI', action='store_true', help='[Configuration] Run switch_rnd_CI simulation')
parser.add_argument('-switch_rnd_CI_TP', action='store_true', help='[Configuration] Run switch_rnd_CI_TP simulation')
parser.add_argument('-switch_rnd_TP', action='store_true', help='[Configuration] Run switch_rnd_TP simulation')
parser.add_argument('-switch_seq', action='store_true', help='[Configuration] Run switch_seq simulation')
parser.add_argument('-switch_laf', action='store_true', help='[Configuration] Run switch_laf simulation')
parser.add_argument('-switch_laf_CI', action='store_true', help='[Configuration] Run switch_laf_CI simulation')
parser.add_argument('-switch_laf_CI_TP', action='store_true', help='[Configuration] Run switch_laf_CI_TP simulation')
parser.add_argument('-switch_laf_TP', action='store_true', help='[Configuration] Run switch_laf_TP simulation')
parser.add_argument('-time_profile', action='store_true', help='[Configuration] Enable SWITCH_STM time profile')
parser.add_argument('-profile', action='store_true', help='[Configuration] Enable both time breakdown and PSCR profiling')




simulation_times = parser.parse_args().simulation_times
threads_list = parser.parse_args().threads_list
log_path = parser.parse_args().log_path
validate_threads_list(threads_list)

# Ensure the log directory exists
os.makedirs(log_path, exist_ok=True)

# simulation_times =parse_simulation_times()
# threads_list = parse_threads_list()

print(f"simulation_times = {simulation_times}, threads_list = {threads_list}, log_path = {log_path}")


# For all true-false arguments, if the argument is not provided, the corresponding simulation will not be run
# Check all true arguments and run the corresponding simulations
args = parser.parse_args()

if args.suicide:
    simulate_suicide(simulation_times, threads_list, log_path, TP=args.time_profile)
if args.polka:
    simulate_polka(simulation_times, threads_list, log_path, TP=args.time_profile)
if args.shrink:
    simulate_shrink(simulation_times, threads_list, log_path, TP=args.time_profile)
if args.ats:
    simulate_ats(simulation_times, threads_list, log_path, TP=args.time_profile)
if args.switch_rnd:
    simulate_switch_stm(simulation_times, threads_list, schedule_policy='rnd', CI=False, TP=args.time_profile or args.profile, PROFILE=args.profile, log_path=log_path)
if args.switch_rnd_CI:
    simulate_switch_stm(simulation_times, threads_list, schedule_policy='rnd', CI=True, TP=args.time_profile or args.profile, PROFILE=args.profile, log_path=log_path)
if args.switch_rnd_CI_TP:
    simulate_switch_stm(simulation_times, threads_list, schedule_policy='rnd', CI=True, TP=True, PROFILE=args.profile, log_path=log_path)
if args.switch_rnd_TP:
    simulate_switch_stm(simulation_times, threads_list, schedule_policy='rnd', CI=False, TP=True, PROFILE=args.profile, log_path=log_path)
if args.switch_seq:
    simulate_switch_stm(simulation_times, threads_list, schedule_policy='seq', CI=False, TP=args.time_profile or args.profile, PROFILE=args.profile, log_path=log_path)
if args.switch_laf:
    simulate_switch_stm(simulation_times, threads_list, schedule_policy='laf', CI=False, TP=args.time_profile or args.profile, PROFILE=args.profile, log_path=log_path)
if args.switch_laf_CI:
    simulate_switch_stm(simulation_times, threads_list, schedule_policy='laf', CI=True, TP=args.time_profile or args.profile, PROFILE=args.profile, log_path=log_path)
if args.switch_laf_CI_TP:
    simulate_switch_stm(simulation_times, threads_list, schedule_policy='laf', CI=True, TP=True, PROFILE=args.profile, log_path=log_path)
if args.switch_laf_TP:
    simulate_switch_stm(simulation_times, threads_list, schedule_policy='laf', CI=False, TP=True, PROFILE=args.profile, log_path=log_path)



# for i in range(len(sys.argv)):
#         arg = sys.argv[i]
#         if arg == '-suicide':
#             simulate_suicide(simulation_times,threads_list)
#         if arg == '-polka':
#             simulate_polka(simulation_times,threads_list)
#         if arg == '-shrink':
#             simulate_shrink(simulation_times,threads_list)
#         if arg == '-ats':
#             simulate_ats(simulation_times, threads_list)

#         if arg == '-switch_rnd':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'rnd',CI = False ,TP = False)
#         if arg == '-switch_rnd_CI':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'rnd',CI = True ,TP = False)
#         if arg == '-switch_rnd_CI_TP':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'rnd',CI = True ,TP = True)
#         if arg == '-switch_rnd_TP':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'rnd',CI = False ,TP = True)
        
#         if arg == '-switch_seq':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'seq',CI = False ,TP = False)
#         if arg == '-switch_seq_CI':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'seq',CI = True ,TP = False)
#         if arg == '-switch_seq_CI_TP':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'seq',CI = True ,TP = True)
#         if arg == '-switch_seq_TP':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'seq',CI = False ,TP = True)
        
#         if arg == '-switch_laf':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'laf',CI = False ,TP = False)
#         if arg == '-switch_laf_CI':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'laf',CI = True ,TP = False)
#         if arg == '-switch_laf_CI_TP':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'laf',CI = True ,TP = True)
#         if arg == '-switch_laf_TP':
#             simulate_switch_stm(simulation_times,threads_list,schedule_policy = 'laf',CI = False ,TP = True)
        
