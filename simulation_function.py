try:
    import sys
except ImportError:
    print("Error: Package 'sys' not found or failed to import.")
try:
    import subprocess
except ImportError:
    print("Error: Package 'subprocess' not found or failed to import.")
import os
import signal
import psutil
import re

directories = [
    'stamp-master/bayes',
    'stamp-master/yada',
    'stamp-master/intruder',
    'stamp-master/vacation',
    'stamp-master/kmeans',
    'stamp-master/labyrinth',
    'stamp-master/genome',
    'stamp-master/ssca2'
]

def parse_simulation_times():
    i = 0
    simulation_times = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-simulation_times":
            i += 1
            simulation_times = int(sys.argv[i])
            break
        i += 1
    return simulation_times if (simulation_times != 1) else 1

def parse_threads_list():
    threads = []
    i = 0
    while i < len(sys.argv):
        if sys.argv[i] == "-thread":
            i += 1
            while i < len(sys.argv) and not sys.argv[i].startswith("-"):
                threads.append(int(sys.argv[i]))
                i += 1
            threads = [thread for thread in threads if (thread & (thread - 1)) == 0]
            break
        i += 1
    return threads if threads else [16]

def reset_makefile_config_to_suicide():
    with open('tinySTM/Makefile', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('# DEFINES += -DCM=CM_SUICIDE','DEFINES += -DCM=CM_SUICIDE') \
                                                .replace('# DEFINES += -DCM=CM_MODULAR','DEFINES += -DCM=CM_MODULAR') \
                                                .replace('# DEFINES += -DSWITCH_STM','DEFINES += -DSWITCH_STM') \
                                                .replace('# DEFINES += -USWITCH_STM','DEFINES += -USWITCH_STM') \
                                                .replace('# DEFINES += -DCONTENTION_INTENSITY','DEFINES += -DCONTENTION_INTENSITY') \
                                                .replace('# DEFINES += -UCONTENTION_INTENSITY','DEFINES += -UCONTENTION_INTENSITY') \
                                                .replace('# DEFINES += -DCM_POLKA','DEFINES += -DCM_POLKA') \
                                                .replace('# DEFINES += -UCM_POLKA','DEFINES += -UCM_POLKA') \
                                                .replace('# DEFINES += -DSHRINK_ENABLE','DEFINES += -DSHRINK_ENABLE') \
                                                .replace('# DEFINES += -USHRINK_ENABLE','DEFINES += -USHRINK_ENABLE') \
                                                .replace('# DEFINES += -DATS_ENABLE','DEFINES += -DATS_ENABLE') \
                                                .replace('# DEFINES += -UATS_ENABLE','DEFINES += -UATS_ENABLE')
    with open('tinySTM/Makefile', 'w') as f:
        f.write(modified_makefile_content)

    with open('tinySTM/Makefile', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('DEFINES += -DCM=CM_SUICIDE','# DEFINES += -DCM=CM_SUICIDE') \
                                                .replace('DEFINES += -DSWITCH_STM','# DEFINES += -DSWITCH_STM') \
                                                .replace('DEFINES += -DCONTENTION_INTENSITY','# DEFINES += -DCONTENTION_INTENSITY') \
                                                .replace('DEFINES += -DCM_POLKA','# DEFINES += -DCM_POLKA') \
                                                .replace('DEFINES += -DSHRINK_ENABLE','# DEFINES += -DSHRINK_ENABLE') \
                                                .replace('DEFINES += -DATS_ENABLE','# DEFINES += -DATS_ENABLE')
    with open('tinySTM/Makefile', 'w') as f:
        f.write(modified_makefile_content)

def reset_makefile_stm_config_to_suicide():
    with open('stamp-master/common/Makefile.stm', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('# CFLAGS   += -I$(STM)/libaco -I$(STM)/src -I$(STM)/src/atomic_ops -DSWITCH_STM','CFLAGS   += -I$(STM)/libaco -I$(STM)/src -I$(STM)/src/atomic_ops -DSWITCH_STM') \
                                                .replace('# CFLAGS   += -DCONTENTION_INTENSITY','CFLAGS   += -DCONTENTION_INTENSITY') \
                                                .replace('# CFLAGS	 += -DSWITCH_STM_TIME_PROFILE','CFLAGS	 += -DSWITCH_STM_TIME_PROFILE') \
                                                .replace('# CFLAGS   += -DSHRINK_ENABLE','CFLAGS   += -DSHRINK_ENABLE') \
                                                .replace('# CFLAGS   += -DATS_ENABLE','CFLAGS   += -DATS_ENABLE')
    with open('stamp-master/common/Makefile.stm', 'w') as f:
        f.write(modified_makefile_content)

    with open('stamp-master/common/Makefile.stm', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('CFLAGS   += -I$(STM)/libaco -I$(STM)/src -I$(STM)/src/atomic_ops -DSWITCH_STM','# CFLAGS   += -I$(STM)/libaco -I$(STM)/src -I$(STM)/src/atomic_ops -DSWITCH_STM') \
                                                .replace('CFLAGS   += -DCONTENTION_INTENSITY','# CFLAGS   += -DCONTENTION_INTENSITY') \
                                                .replace('CFLAGS	 += -DSWITCH_STM_TIME_PROFILE','# CFLAGS	 += -DSWITCH_STM_TIME_PROFILE') \
                                                .replace('CFLAGS   += -DSHRINK_ENABLE','# CFLAGS   += -DSHRINK_ENABLE') \
                                                .replace('CFLAGS   += -DATS_ENABLE','# CFLAGS   += -DATS_ENABLE')
    with open('stamp-master/common/Makefile.stm', 'w') as f:
        f.write(modified_makefile_content)

def run_tests(log_file="output.stm", threads=16):
    tests = [
        "./yada/yada -a15 -i yada/inputs/ttimeu1000000.2 -t",
        "./intruder/intruder -a10 -l128 -n262144 -s1 -t",
        "./kmeans/kmeans -m40 -n40 -t0.00001 -i kmeans/inputs/random-n65536-d32-c16.txt -p",
        "./kmeans/kmeans -m15 -n15 -t0.00001 -i kmeans/inputs/random-n65536-d32-c16.txt -p",
        "./bayes/bayes -v32 -r4096 -n10 -p40 -i2 -e8 -s1 -t",
        "./vacation/vacation -n2 -q90 -u98 -r1048576 -t4194304 -c",
        "./vacation/vacation -n4 -q60 -u90 -r1048576 -t4194304 -c",
        "./genome/genome -g16384 -s64 -n16777216 -t",
        "./labyrinth/labyrinth -i labyrinth/inputs/random-x512-y512-z7-n512.txt -t",
        "./ssca2/ssca2 -s20 -i1.0 -u1.0 -l3 -p3 -t"
    ]

    for test in tests:
        timeout = 600
        print(f"Executing: {test} {threads}")
        with open(log_file, "a") as f:
            f.write(f"Executing: {test} {threads}\n")
        try:
            process = subprocess.Popen(f"{test} {threads}", cwd="stamp-master/", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid)
            stdout, _ = process.communicate(timeout=timeout)
            with open(log_file, "a") as f:
                f.write(stdout)
            print(stdout)
        except subprocess.TimeoutExpired:
            # Kill the entire process group
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            
            # Wait for a short time to allow for graceful termination
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # If the process is still running, force kill it and its children
                try:
                    parent = psutil.Process(process.pid)
                    for child in parent.children(recursive=True):
                        child.terminate()
                    parent.terminate()
                    gone, alive = psutil.wait_procs([parent] + parent.children(recursive=True), timeout=3)
                    for p in alive:
                        p.kill()
                except psutil.NoSuchProcess:
                    pass
            
            stdout, _ = process.communicate()  # Collect any remaining output
            with open(log_file, "a") as f:
                f.write(f"Timeout occurred after {timeout} seconds.\n")
                f.write(stdout)  # Write any output that was produced before the timeout
            print(f"Timeout occurred after {timeout} seconds.")
        except Exception as e:
            with open(log_file, "a") as f:
                f.write(f"An error occurred: {str(e)}\n")
            print(f"An error occurred: {str(e)}")
        finally:
            # Ensure all related processes are terminated
            try:
                parent = psutil.Process(process.pid)
                children = parent.children(recursive=True)
                for child in children:
                    child.terminate()
                parent.terminate()
                gone, alive = psutil.wait_procs([parent] + children, timeout=3)
                for p in alive:
                    p.kill()
            except psutil.NoSuchProcess:
                pass  # Process already terminated

    # After all tests, clean up any remaining zombie processes
    try:
        current_process = psutil.Process()
        children = current_process.children(recursive=True)
        for child in children:
            if child.status() == psutil.STATUS_ZOMBIE:
                child.wait()
    except psutil.NoSuchProcess:
        pass

def simulate_suicide(simulation_times=1, threads_list=[16], log_path="./log", TP=False):
    ###############SUICIDE###############
    print("###############SUICIDE###############")
    print("###############SUICIDE###############")
    print("###############SUICIDE###############")
    print("###############SUICIDE###############")
    print("###############SUICIDE###############")
    print("###############SUICIDE###############")
    print("###############SUICIDE###############")
    print("###############SUICIDE###############")
    print("###############SUICIDE###############")
    print("###############SUICIDE###############")
    #reset the configuration to suicide
    reset_makefile_config_to_suicide()
    reset_makefile_stm_config_to_suicide()

    # If TP is true ,emable SWITCH_STM time profile
    if (TP == True):
        with open('tinySTM/Makefile', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-DSWITCH_STM_TIME_PROFILE', 'DEFINES += -DSWITCH_STM_TIME_PROFILE', makefile_content, flags=re.MULTILINE)
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-USWITCH_STM_TIME_PROFILE', '# DEFINES += -USWITCH_STM_TIME_PROFILE', modified_makefile_content, flags=re.MULTILINE)
        with open('tinySTM/Makefile', 'w') as f:
            f.write(modified_makefile_content)

        with open('stamp-master/common/Makefile.stm', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('# CFLAGS	 += -DSWITCH_STM_TIME_PROFILE','CFLAGS	 += -DSWITCH_STM_TIME_PROFILE')
        with open('stamp-master/common/Makefile.stm', 'w') as f:
            f.write(modified_makefile_content)

    #Compile tinySTM
    subprocess.run(['make'],cwd='tinySTM')

    #Compile STAMP
    for directory in directories:
        subprocess.run(["make", "-f", f"Makefile.stm", "clean"], cwd=directory)
        subprocess.run(["make", "-f", f"Makefile.stm"], cwd=directory)

    #Run the test
    for i in range(simulation_times):
        for threads in threads_list:
            log_name = f"suicide_{threads}.stm"
            if TP:
                log_name = f"suicide_TP_{threads}.stm"
            log_file = os.path.join(log_path, log_name)
            run_tests(log_file=log_file, threads=threads)
        current_time = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip()
        print(f"Done the iteration {i} - Current time: {current_time}")

    #Print current time
    current_time = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip()
    print(f"Done all the iterations of suicide! - Current time: {current_time}")

def simulate_polka(simulation_times=1, threads_list=[16], log_path="./log", TP=False):
    ###############POLKA###############
    print("###############POLKA###############")
    print("###############POLKA###############")
    print("###############POLKA###############")
    print("###############POLKA###############")
    print("###############POLKA###############")
    print("###############POLKA###############")
    print("###############POLKA###############")
    print("###############POLKA###############")
    print("###############POLKA###############")
    print("###############POLKA###############")

    #reset the configuration to suicide
    reset_makefile_config_to_suicide()
    reset_makefile_stm_config_to_suicide()

    # Modify the configuration of tinySTM to POLKA
    with open('tinySTM/Makefile', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('# DEFINES += -DCM_POLKA','DEFINES += -DCM_POLKA') \
                                                .replace('DEFINES += -UCM_POLKA','# DEFINES += -UCM_POLKA')
    with open('tinySTM/Makefile', 'w') as f:
        f.write(modified_makefile_content)

    # If TP is true ,emable SWITCH_STM time profile
    if (TP == True):
        with open('tinySTM/Makefile', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-DSWITCH_STM_TIME_PROFILE', 'DEFINES += -DSWITCH_STM_TIME_PROFILE', makefile_content, flags=re.MULTILINE)
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-USWITCH_STM_TIME_PROFILE', '# DEFINES += -USWITCH_STM_TIME_PROFILE', modified_makefile_content, flags=re.MULTILINE)
        with open('tinySTM/Makefile', 'w') as f:
            f.write(modified_makefile_content)

        with open('stamp-master/common/Makefile.stm', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('# CFLAGS	 += -DSWITCH_STM_TIME_PROFILE','CFLAGS	 += -DSWITCH_STM_TIME_PROFILE')
        with open('stamp-master/common/Makefile.stm', 'w') as f:
            f.write(modified_makefile_content)

    #Compile tinySTM
    subprocess.run(['make'],cwd='tinySTM')

    #Compile STAMP
    for directory in directories:
        subprocess.run(["make", "-f", f"Makefile.stm", "clean"], cwd=directory)
        subprocess.run(["make", "-f", f"Makefile.stm"], cwd=directory)

    #Run the test
    for i in range(simulation_times):
        for threads in threads_list:
            log_name = f"polka_{threads}.stm"
            if TP:
                log_name = f"polka_TP_{threads}.stm"
            log_file = os.path.join(log_path, log_name)
            run_tests(log_file=log_file, threads=threads)
        current_time = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip()
        print(f"Done the iteration {i} - Current time: {current_time}")

    #Print current time
    current_time = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip()
    print(f"Done all the iterations of polka! - Current time: {current_time}")

def simulate_ats(simulation_times=1, threads_list=[16], log_path="./log", TP=False):
    ###############ATS#################
    print("#################ATS#################")
    print("#################ATS#################")
    print("#################ATS#################")
    print("#################ATS#################")
    print("#################ATS#################")
    print("#################ATS#################")
    print("#################ATS#################")
    print("#################ATS#################")
    print("#################ATS#################")

    #reset the configuration to suicide
    reset_makefile_config_to_suicide()
    reset_makefile_stm_config_to_suicide()

    # Modify the configuration of tinySTM to ATS
    with open('tinySTM/Makefile', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('# DEFINES += -DCM=CM_SUICIDE','DEFINES += -DCM=CM_SUICIDE') \
                                                .replace('DEFINES += -DCM=CM_MODULAR','# DEFINES += -DCM=CM_MODULAR') \
                                                .replace('# DEFINES += -DATS_ENABLE','DEFINES += -DATS_ENABLE') \
                                                .replace('DEFINES += -UATS_ENABLE','# DEFINES += -UATS_ENABLE')
    with open('tinySTM/Makefile', 'w') as f:
        f.write(modified_makefile_content)

    # If TP is true ,emable SWITCH_STM time profile
    if (TP == True):
        with open('tinySTM/Makefile', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-DSWITCH_STM_TIME_PROFILE', 'DEFINES += -DSWITCH_STM_TIME_PROFILE', makefile_content, flags=re.MULTILINE)
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-USWITCH_STM_TIME_PROFILE', '# DEFINES += -USWITCH_STM_TIME_PROFILE', modified_makefile_content, flags=re.MULTILINE)
        with open('tinySTM/Makefile', 'w') as f:
            f.write(modified_makefile_content)

        with open('stamp-master/common/Makefile.stm', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('# CFLAGS	 += -DSWITCH_STM_TIME_PROFILE','CFLAGS	 += -DSWITCH_STM_TIME_PROFILE')
        with open('stamp-master/common/Makefile.stm', 'w') as f:
            f.write(modified_makefile_content)

    #Compile tinySTM
    subprocess.run(['make'],cwd='tinySTM')

    #Compile STAMP
    for directory in directories:
        subprocess.run(["make", "-f", f"Makefile.stm", "clean"], cwd=directory)
        subprocess.run(["make", "-f", f"Makefile.stm"], cwd=directory)
    
    #Run the test
    for i in range(simulation_times):
        for threads in threads_list:
            log_name = f"ats_{threads}.stm"
            if TP:
                log_name = f"ats_TP_{threads}.stm"
            log_file = os.path.join(log_path, log_name)
            run_tests(log_file=log_file, threads=threads)
        current_time = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip()
        print(f"Done the iteration {i} - Current time: {current_time}")

    #Print current time
    current_time = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip()
    print(f"Done all the iterations of ats! - Current time: {current_time}")


def simulate_shrink(simulation_times=1, threads_list=[16], log_path="./log", TP=False):
    ###############SHRINK###############
    print("###############SHRINK###############")
    print("###############SHRINK###############")
    print("###############SHRINK###############")
    print("###############SHRINK###############")
    print("###############SHRINK###############")
    print("###############SHRINK###############")
    print("###############SHRINK###############")
    print("###############SHRINK###############")
    print("###############SHRINK###############")
    print("###############SHRINK###############")

    #reset the configuration to suicide
    reset_makefile_config_to_suicide()
    reset_makefile_stm_config_to_suicide()

    # Modify the configuration of tinySTM to SHRINK
    with open('tinySTM/Makefile', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('# DEFINES += -DCM=CM_SUICIDE','DEFINES += -DCM=CM_SUICIDE') \
                                                .replace('DEFINES += -DCM=CM_MODULAR','# DEFINES += -DCM=CM_MODULAR') \
                                                .replace('# DEFINES += -DSHRINK_ENABLE','DEFINES += -DSHRINK_ENABLE') \
                                                .replace('DEFINES += -USHRINK_ENABLE','# DEFINES += -USHRINK_ENABLE')
    with open('tinySTM/Makefile', 'w') as f:
        f.write(modified_makefile_content)

    # If TP is true ,emable SWITCH_STM time profile
    if (TP == True):
        with open('tinySTM/Makefile', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-DSWITCH_STM_TIME_PROFILE', 'DEFINES += -DSWITCH_STM_TIME_PROFILE', makefile_content, flags=re.MULTILINE)
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-USWITCH_STM_TIME_PROFILE', '# DEFINES += -USWITCH_STM_TIME_PROFILE', modified_makefile_content, flags=re.MULTILINE)
        with open('tinySTM/Makefile', 'w') as f:
            f.write(modified_makefile_content)

        with open('stamp-master/common/Makefile.stm', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('# CFLAGS	 += -DSWITCH_STM_TIME_PROFILE','CFLAGS	 += -DSWITCH_STM_TIME_PROFILE')
        with open('stamp-master/common/Makefile.stm', 'w') as f:
            f.write(modified_makefile_content)

    #Compile tinySTM
    subprocess.run(['make'],cwd='tinySTM')

    # Modify the configuration of STAMP to SHRINK
    with open('stamp-master/common/Makefile.stm', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('# CFLAGS   += -DSHRINK_ENABLE','CFLAGS   += -DSHRINK_ENABLE')
    with open('stamp-master/common/Makefile.stm', 'w') as f:
        f.write(modified_makefile_content)

    #Compile STAMP
    for directory in directories:
        subprocess.run(["make", "-f", f"Makefile.stm", "clean"], cwd=directory)
        subprocess.run(["make", "-f", f"Makefile.stm"], cwd=directory)

    #Run the test
    for i in range(simulation_times):
        for threads in threads_list:
            log_name = f"shrink_{threads}.stm"
            if TP:
                log_name = f"shrink_TP_{threads}.stm"
            log_file = os.path.join(log_path, log_name)
            run_tests(log_file=log_file, threads=threads)
        current_time = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip()
        print(f"Done the iteration {i} - Current time: {current_time}")

    #Print current time
    current_time = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip()
    print(f"Done all the iterations of shrink! - Current time: {current_time}")

    # Undo the modification of configuration of STAMP
    with open('stamp-master/common/Makefile.stm', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('CFLAGS   += -DSHRINK_ENABLE','# CFLAGS   += -DSHRINK_ENABLE')
    with open('stamp-master/common/Makefile.stm', 'w') as f:
        f.write(modified_makefile_content)

def simulate_switch_stm(simulation_times=1, threads_list=[16], schedule_policy='seq', CI=True, TP=False, PROFILE=False, log_path="./log"):
    ###############SWITCH_STM###############
    print("###############SWITCH_STM###############")
    print("###############SWITCH_STM###############")
    print("###############SWITCH_STM###############")
    print("###############SWITCH_STM###############")
    print("###############SWITCH_STM###############")
    print("###############SWITCH_STM###############")
    print("###############SWITCH_STM###############")
    print("###############SWITCH_STM###############")
    print("###############SWITCH_STM###############")
    print("###############SWITCH_STM###############")

    #reset the configuration to suicide
    reset_makefile_config_to_suicide()
    reset_makefile_stm_config_to_suicide()
    
    # Modify the configuration of tinySTM to SWITCH_STM
    with open('tinySTM/Makefile', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('# DEFINES += -DCM=CM_SUICIDE','DEFINES += -DCM=CM_SUICIDE') \
                                                .replace('DEFINES += -DCM=CM_MODULAR','# DEFINES += -DCM=CM_MODULAR') \
                                                .replace('# DEFINES += -DSWITCH_STM','DEFINES += -DSWITCH_STM') \
                                                .replace('DEFINES += -USWITCH_STM','# DEFINES += -USWITCH_STM')
    with open('tinySTM/Makefile', 'w') as f:
        f.write(modified_makefile_content)

    # set the schedule policy
    if (schedule_policy == 'rnd'):
        with open('tinySTM/include/param.h', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('#define SCHEDULE_POLICY                     1 ','#define SCHEDULE_POLICY                     0 ') \
                                                    .replace('#define SCHEDULE_POLICY                     2 ','#define SCHEDULE_POLICY                     0 ')
        with open('tinySTM/include/param.h', 'w') as f:
            f.write(modified_makefile_content)
    elif (schedule_policy == 'seq'):
        with open('tinySTM/include/param.h', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('#define SCHEDULE_POLICY                     0 ','#define SCHEDULE_POLICY                     1 ') \
                                                    .replace('#define SCHEDULE_POLICY                     2 ','#define SCHEDULE_POLICY                     1 ')
        with open('tinySTM/include/param.h', 'w') as f:
            f.write(modified_makefile_content)
    elif (schedule_policy == 'laf'):
        with open('tinySTM/include/param.h', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('#define SCHEDULE_POLICY                     0 ','#define SCHEDULE_POLICY                     2 ') \
                                                    .replace('#define SCHEDULE_POLICY                     1 ','#define SCHEDULE_POLICY                     2 ')
        with open('tinySTM/include/param.h', 'w') as f:
            f.write(modified_makefile_content)
        
    # To modify param.h to select the desired strategy,
    # you have to replace the SCHEDULE_POLICY value
    # Change SCHEDULE_POLICY from any other value to the case number of your switch strategy
    # you can use the following template:
        '''
    elif schedule_policy == 'YOUR_POLICY':
        with open('tinySTM/include/param.h', 'r') as f:
            makefile_content = f.read()
        
        modified_makefile_content = makefile_content.replace('#define SCHEDULE_POLICY                     0 ','#define SCHEDULE_POLICY                     2 ') \
                                                    .replace('#define SCHEDULE_POLICY                     1 ','#define SCHEDULE_POLICY                     2 ')
        with open('tinySTM/include/param.h', 'w') as f:
            f.write(modified_makefile_content)
        '''
    else:
        print("No schedule policy is set, the simulation might not correct!!!")
 
    # If CI is true ,set the flag of CI
    if (CI == True):
        with open('tinySTM/Makefile', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('# DEFINES += -DCONTENTION_INTENSITY','DEFINES += -DCONTENTION_INTENSITY') \
                                                    .replace('DEFINES += -UCONTENTION_INTENSITY','# DEFINES += -UCONTENTION_INTENSITY')
        with open('tinySTM/Makefile', 'w') as f:
            f.write(modified_makefile_content)

    # If TP is true ,emable SWITCH_STM time profile
    if (TP == True):
        with open('tinySTM/Makefile', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-DSWITCH_STM_TIME_PROFILE', 'DEFINES += -DSWITCH_STM_TIME_PROFILE', makefile_content, flags=re.MULTILINE)
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-USWITCH_STM_TIME_PROFILE', '# DEFINES += -USWITCH_STM_TIME_PROFILE', modified_makefile_content, flags=re.MULTILINE)
        with open('tinySTM/Makefile', 'w') as f:
            f.write(modified_makefile_content)

        with open('stamp-master/common/Makefile.stm', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('# CFLAGS	 += -DSWITCH_STM_TIME_PROFILE','CFLAGS	 += -DSWITCH_STM_TIME_PROFILE')
        with open('stamp-master/common/Makefile.stm', 'w') as f:
            f.write(modified_makefile_content)

    # If PROFILE is true, enable SWITCH_STM_METRIC_PROFILE
    if (PROFILE == True):
        with open('tinySTM/Makefile', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-DSWITCH_STM_METRIC_PROFILE', 'DEFINES += -DSWITCH_STM_METRIC_PROFILE', makefile_content, flags=re.MULTILINE)
        modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-USWITCH_STM_METRIC_PROFILE', '# DEFINES += -USWITCH_STM_METRIC_PROFILE', modified_makefile_content, flags=re.MULTILINE)
        with open('tinySTM/Makefile', 'w') as f:
            f.write(modified_makefile_content)

        with open('stamp-master/common/Makefile.stm', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('# CFLAGS	 += -DSWITCH_STM_METRIC_PROFILE','CFLAGS	 += -DSWITCH_STM_METRIC_PROFILE')
        with open('stamp-master/common/Makefile.stm', 'w') as f:
            f.write(modified_makefile_content)

            
    #Compile tinySTM
    subprocess.run(['make', 'clean'],cwd='tinySTM')
    subprocess.run(['make'],cwd='tinySTM')

    # Modify the configuration of STAMP to SWITCH_STM
    with open('stamp-master/common/Makefile.stm', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('# CFLAGS   += -I$(STM)/libaco -I$(STM)/src -I$(STM)/src/atomic_ops -DSWITCH_STM','CFLAGS   += -I$(STM)/libaco -I$(STM)/src -I$(STM)/src/atomic_ops -DSWITCH_STM')
    with open('stamp-master/common/Makefile.stm', 'w') as f:
        f.write(modified_makefile_content)

    # If CI is true , set the flag of CI
    if (CI == True):
        with open('stamp-master/common/Makefile.stm', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('# CFLAGS   += -DCONTENTION_INTENSITY','CFLAGS   += -DCONTENTION_INTENSITY')
        with open('stamp-master/common/Makefile.stm', 'w') as f:
            f.write(modified_makefile_content) 

        
    #Compile STAMP
    for directory in directories:
        subprocess.run(["make", "-f", f"Makefile.stm", "clean"], cwd=directory)
        subprocess.run(["make", "-f", f"Makefile.stm"], cwd=directory)

    #specify log name
    if (schedule_policy == 'rnd' and CI == False):
        switch_log_name = 'switch_rnd'
    elif (schedule_policy == 'rnd' and CI == True):
        switch_log_name = 'switch_rnd_CI'
    elif (schedule_policy == 'seq' and CI == False):
        switch_log_name = 'switch_seq'
    elif (schedule_policy == 'seq' and CI == True):
        switch_log_name = 'switch_seq_CI'
    elif (schedule_policy == 'laf' and CI == False):
        switch_log_name = 'switch_laf'
    elif (schedule_policy == 'laf' and CI == True):
        switch_log_name = 'switch_laf_CI'
    else:
        switch_log_name = 'some_wierd_switch_mode'
    
    if PROFILE:
        switch_log_name += '_Profile'
 
    #Run the test
    for i in range(simulation_times):
        for threads in threads_list:
            log_file = os.path.join(log_path, f"{switch_log_name}_{threads}.stm")
            run_tests(log_file=log_file, threads=threads)
        current_time = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip()
        print(f"Done the iteration {i} - Current time: {current_time}")

    #Print current time
    current_time = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip()
    print(f"Done all the iterations of {switch_log_name}! - Current time: {current_time}")

    if (PROFILE == True):
         with open('tinySTM/Makefile', 'r') as f:
            makefile_content = f.read()
            # Disable definition
         modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-DSWITCH_STM_METRIC_PROFILE', '# DEFINES += -DSWITCH_STM_METRIC_PROFILE', makefile_content, flags=re.MULTILINE)
         modified_makefile_content = re.sub(r'^\s*#?\s*DEFINES\s*\+=\s*-USWITCH_STM_METRIC_PROFILE', 'DEFINES += -USWITCH_STM_METRIC_PROFILE', modified_makefile_content, flags=re.MULTILINE)
         with open('tinySTM/Makefile', 'w') as f:
            f.write(modified_makefile_content)

         with open('stamp-master/common/Makefile.stm', 'r') as f:
            makefile_content = f.read()
         modified_makefile_content = makefile_content.replace('CFLAGS	 += -DSWITCH_STM_METRIC_PROFILE', '# CFLAGS	 += -DSWITCH_STM_METRIC_PROFILE')
         with open('stamp-master/common/Makefile.stm', 'w') as f:
            f.write(modified_makefile_content)

    # Undo the modification of configuration of STAMP
    with open('stamp-master/common/Makefile.stm', 'r') as f:
        makefile_content = f.read()
    modified_makefile_content = makefile_content.replace('CFLAGS   += -I$(STM)/libaco -I$(STM)/src -I$(STM)/src/atomic_ops -DSWITCH_STM','# CFLAGS   += -I$(STM)/libaco -I$(STM)/src -I$(STM)/src/atomic_ops -DSWITCH_STM')
    with open('stamp-master/common/Makefile.stm', 'w') as f:
        f.write(modified_makefile_content)

    # If CI is true , reset the flag of CI
    if (CI == True):
        with open('stamp-master/common/Makefile.stm', 'r') as f:
            makefile_content = f.read()
        modified_makefile_content = makefile_content.replace('CFLAGS   += -DCONTENTION_INTENSITY','# CFLAGS   += -DCONTENTION_INTENSITY')
        with open('stamp-master/common/Makefile.stm', 'w') as f:
            f.write(modified_makefile_content)