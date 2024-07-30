import re

def generate_file_list(base_path, prefix, threads):
    return [f'{base_path}/{prefix}_{thread}.stm' for thread in threads]

def caculate_data(file_name, datasets):

    with open(file_name, 'r') as file:
        lines = file.readlines()

    executing_bayes     = False
    executing_genome    = False
    executing_intruder  = False
    executing_kmeans1   = False
    executing_kmeans2   = False
    executing_labyrinth = False
    executing_ssca2     = False
    executing_vacation1 = False
    executing_vacation2 = False
    executing_yada      = False

    bayes_time     = []
    genome_time    = []
    intruder_time  = []
    kmeans1_time   = []
    kmeans2_time   = []
    labyrinth_time = []
    ssca2_time     = []
    vacation1_time = []
    vacation2_time = []
    yada_time      = []

    for line in lines:
        #bayes
        if 'Executing: ./bayes/bayes' in line:
            executing_bayes     = True
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_bayes == True and line.startswith('Learn time ='):
            data = line.split('=', 1)[-1].split()[0]
            bayes_time.append(float(data))
            executing_bayes = False 

        #genome
        if 'Executing: ./genome/genome' in line:
            executing_bayes     = False
            executing_genome    = True
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_genome == True and line.startswith('Time ='):
            data = line.split('=', 1)[-1].split()[0]
            genome_time.append(float(data))
            executing_genome = False

        #intruder
        if 'Executing: ./intruder/intruder' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = True
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_intruder == True and line.startswith('Elapsed time    ='):
            data = line.split('=', 1)[-1].split()[0]
            intruder_time.append(float(data))
            executing_intruder = False

        #kmeans1
        if 'Executing: ./kmeans/kmeans -m40 -n40' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = True
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_kmeans1 == True and line.startswith('Time:'):
            data = line.split(':', 1)[-1].split()[0]
            kmeans1_time.append(float(data))
            executing_kmeans1 = False

        #kmeans2
        if 'Executing: ./kmeans/kmeans -m15 -n15' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = True
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_kmeans2 == True and line.startswith('Time:'):
            data = line.split(':', 1)[-1].split()[0]
            kmeans2_time.append(float(data))
            executing_kmeans2 = False

        #labyrinth
        if 'Executing: ./labyrinth/labyrinth' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = True
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_labyrinth == True and line.startswith('Elapsed time    ='):
            data = line.split('=', 1)[-1].split()[0]
            labyrinth_time.append(float(data))
            executing_labyrinth = False

        #ssca2
        if 'Executing: ./ssca2/ssca2' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = True
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_ssca2 == True and line.startswith('Time taken for all is'):
            data = line.split('is', 1)[-1].split()[0]
            ssca2_time.append(float(data))
            executing_ssca2 = False

        #vacation1
        if 'Executing: ./vacation/vacation -n2' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = True
            executing_vacation2 = False
            executing_yada      = False
        if executing_vacation1 == True and line.startswith('Time ='):
            data = line.split('=', 1)[-1].split()[0]
            vacation1_time.append(float(data))
            executing_vacation1 = False

        #vacation2
        if 'Executing: ./vacation/vacation -n4' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = True
            executing_yada      = False
        if executing_vacation2 == True and line.startswith('Time ='):
            data = line.split('=', 1)[-1].split()[0]
            vacation2_time.append(float(data))
            executing_vacation2 = False

        #yada
        if 'Executing: ./yada/yada' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = True
        if executing_yada == True and line.startswith('Elapsed time                    ='):
            data = line.split('=', 1)[-1].split()[0]
            yada_time.append(float(data))
            executing_yada = False

    '''
    print("bayes_time     ",bayes_time     ) 
    print("genome_time    ",genome_time    ) 
    print("intruder_time  ",intruder_time  ) 
    print("kmeans1_time   ",kmeans1_time   ) 
    print("kmeans2_time   ",kmeans2_time   ) 
    print("labyrinth_time ",labyrinth_time ) 
    print("ssca2_time     ",ssca2_time     ) 
    print("vacation1_time ",vacation1_time ) 
    print("vacation2_time ",vacation2_time ) 
    print("yada_time      ",yada_time      )
    '''

    datasets[0].append(sum(bayes_time)    / len(bayes_time)     )if len(bayes_time) >     0 else datasets[0].append(0) 
    datasets[1].append(sum(genome_time)   / len(genome_time)    )if len(genome_time) >    0 else datasets[1].append(0) 
    datasets[2].append(sum(intruder_time) / len(intruder_time)  )if len(intruder_time) >  0 else datasets[2].append(0) 
    datasets[3].append(sum(kmeans1_time)  / len(kmeans1_time)   )if len(kmeans1_time) >   0 else datasets[3].append(0) 
    datasets[4].append(sum(kmeans2_time)  / len(kmeans2_time)   )if len(kmeans2_time) >   0 else datasets[4].append(0) 
    datasets[5].append(sum(labyrinth_time)/ len(labyrinth_time) )if len(labyrinth_time) > 0 else datasets[5].append(0) 
    datasets[6].append(sum(ssca2_time)    / len(ssca2_time)     )if len(ssca2_time) >     0 else datasets[6].append(0) 
    datasets[7].append(sum(vacation1_time)/ len(vacation1_time) )if len(vacation1_time) > 0 else datasets[7].append(0) 
    datasets[8].append(sum(vacation2_time)/ len(vacation2_time) )if len(vacation2_time) > 0 else datasets[8].append(0) 
    datasets[9].append(sum(yada_time)     / len(yada_time)      )if len(yada_time) >      0 else datasets[9].append(0)

def caculate_abort_ratio(file_name, datasets):

    with open(file_name, 'r') as file:
        lines = file.readlines()

    executing_bayes     = False
    executing_genome    = False
    executing_intruder  = False
    executing_kmeans1   = False
    executing_kmeans2   = False
    executing_labyrinth = False
    executing_ssca2     = False
    executing_vacation1 = False
    executing_vacation2 = False
    executing_yada      = False

    bayes_abort_ratio     = []
    genome_abort_ratio    = []
    intruder_abort_ratio  = []
    kmeans1_abort_ratio   = []
    kmeans2_abort_ratio   = []
    labyrinth_abort_ratio = []
    ssca2_abort_ratio     = []
    vacation1_abort_ratio = []
    vacation2_abort_ratio = []
    yada_abort_ratio      = []


    for line in lines:
        #bayes
        if 'Executing: ./bayes/bayes' in line:
            executing_bayes     = True
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_bayes == True and line.startswith('committed:'):
            parts = line.split(',')
            abort_ratio = (int(parts[1].split(':')[1]))/(int(parts[0].split(':')[1]))
            bayes_abort_ratio.append(float(abort_ratio))
            executing_bayes = False 

        #genome
        if 'Executing: ./genome/genome' in line:
            executing_bayes     = False
            executing_genome    = True
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_genome == True and line.startswith('committed:'):
            parts = line.split(',')
            abort_ratio = (int(parts[1].split(':')[1]))/(int(parts[0].split(':')[1]))
            genome_abort_ratio.append(float(abort_ratio))
            executing_genome = False

        #intruder
        if 'Executing: ./intruder/intruder' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = True
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_intruder == True and line.startswith('committed:'):
            parts = line.split(',')
            abort_ratio = (int(parts[1].split(':')[1]))/(int(parts[0].split(':')[1]))
            intruder_abort_ratio.append(float(abort_ratio))
            executing_intruder = False

        #kmeans1
        if 'Executing: ./kmeans/kmeans -m40 -n40' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = True
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_kmeans1 == True and line.startswith('committed:'):
            parts = line.split(',')
            abort_ratio = (int(parts[1].split(':')[1]))/(int(parts[0].split(':')[1]))
            kmeans1_abort_ratio.append(float(abort_ratio))
            executing_kmeans1 = False

        #kmeans2
        if 'Executing: ./kmeans/kmeans -m15 -n15' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = True
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_kmeans2 == True and line.startswith('committed:'):
            parts = line.split(',')
            abort_ratio = (int(parts[1].split(':')[1]))/(int(parts[0].split(':')[1]))
            kmeans2_abort_ratio.append(float(abort_ratio))
            executing_kmeans2 = False

        #labyrinth
        if 'Executing: ./labyrinth/labyrinth' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = True
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_labyrinth == True and line.startswith('committed:'):
            parts = line.split(',')
            abort_ratio = (int(parts[1].split(':')[1]))/(int(parts[0].split(':')[1]))
            labyrinth_abort_ratio.append(float(abort_ratio))
            executing_labyrinth = False

        #ssca2
        if 'Executing: ./ssca2/ssca2' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = True
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_ssca2 == True and line.startswith('committed:'):
            parts = line.split(',')
            abort_ratio = (int(parts[1].split(':')[1]))/(int(parts[0].split(':')[1]))
            ssca2_abort_ratio.append(float(abort_ratio))
            executing_ssca2 = False

        #vacation1
        if 'Executing: ./vacation/vacation -n2' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = True
            executing_vacation2 = False
            executing_yada      = False
        if executing_vacation1 == True and line.startswith('committed:'):
            parts = line.split(',')
            abort_ratio = (int(parts[1].split(':')[1]))/(int(parts[0].split(':')[1]))
            vacation1_abort_ratio.append(float(abort_ratio))
            executing_vacation1 = False

        #vacation2
        if 'Executing: ./vacation/vacation -n4' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = True
            executing_yada      = False
        if executing_vacation2 == True and line.startswith('committed:'):
            parts = line.split(',')
            abort_ratio = (int(parts[1].split(':')[1]))/(int(parts[0].split(':')[1]))
            vacation2_abort_ratio.append(float(abort_ratio))
            executing_vacation2 = False

        #yada
        if 'Executing: ./yada/yada' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = True
        if executing_yada == True and line.startswith('committed:'):
            parts = line.split(',')
            abort_ratio = (int(parts[1].split(':')[1]))/(int(parts[0].split(':')[1]))
            yada_abort_ratio.append(float(abort_ratio))
            executing_yada = False


    datasets[0].append(sum(bayes_abort_ratio)    / len(bayes_abort_ratio)     )if len(bayes_abort_ratio) >     0 else datasets[0].append(0) 
    datasets[1].append(sum(genome_abort_ratio)   / len(genome_abort_ratio)    )if len(genome_abort_ratio) >    0 else datasets[1].append(0) 
    datasets[2].append(sum(intruder_abort_ratio) / len(intruder_abort_ratio)  )if len(intruder_abort_ratio) >  0 else datasets[2].append(0) 
    datasets[3].append(sum(kmeans1_abort_ratio)  / len(kmeans1_abort_ratio)   )if len(kmeans1_abort_ratio) >   0 else datasets[3].append(0) 
    datasets[4].append(sum(kmeans2_abort_ratio)  / len(kmeans2_abort_ratio)   )if len(kmeans2_abort_ratio) >   0 else datasets[4].append(0) 
    datasets[5].append(sum(labyrinth_abort_ratio)/ len(labyrinth_abort_ratio) )if len(labyrinth_abort_ratio) > 0 else datasets[5].append(0) 
    datasets[6].append(sum(ssca2_abort_ratio)    / len(ssca2_abort_ratio)     )if len(ssca2_abort_ratio) >     0 else datasets[6].append(0) 
    datasets[7].append(sum(vacation1_abort_ratio)/ len(vacation1_abort_ratio) )if len(vacation1_abort_ratio) > 0 else datasets[7].append(0) 
    datasets[8].append(sum(vacation2_abort_ratio)/ len(vacation2_abort_ratio) )if len(vacation2_abort_ratio) > 0 else datasets[8].append(0) 
    datasets[9].append(sum(yada_abort_ratio)     / len(yada_abort_ratio)      )if len(yada_abort_ratio) >      0 else datasets[9].append(0)
       
def switch_data_record(file_name, 
                       avg_switch_time, 
                       avg_run_tx_time, 
                       avg_first_stage_time, 
                       avg_second_stage_time, 
                       avg_switch_committed,
                       avg_switch_aborted,
                       avg_total_committed,
                       avg_total_aborted):

    with open(file_name, 'r') as file:
        lines = file.readlines()

    executing_bayes     = False
    executing_genome    = False
    executing_intruder  = False
    executing_kmeans1   = False
    executing_kmeans2   = False
    executing_labyrinth = False
    executing_ssca2     = False
    executing_vacation1 = False
    executing_vacation2 = False
    executing_yada      = False

    switch_time =       [[] for _ in range(10)]
    run_tx_time =       [[] for _ in range(10)]
    first_stage_time =  [[] for _ in range(10)]
    second_stage_time = [[] for _ in range(10)]
    switch_committed =  [[] for _ in range(10)]
    switch_aborted =    [[] for _ in range(10)]
    total_committed =   [[] for _ in range(10)]
    total_aborted =     [[] for _ in range(10)]

    for line in lines:
        #bayes
        if 'Executing: ./bayes/bayes' in line:
            executing_bayes     = True
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_bayes == True and line.startswith('First stage time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            first_stage_time[0].append(float(numbers[0]))
            second_stage_time[0].append(float(numbers[1]))
        if executing_bayes == True and line.startswith('Switch time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            switch_time[0].append(float(numbers[0]))
            run_tx_time[0].append(float(numbers[1]))
        if executing_bayes == True and line.startswith('commit cause by switch:'):
            numbers = re.findall(r'\d+', line)
            switch_committed[0].append(int(numbers[0]))
            switch_aborted[0].append(int(numbers[1]))
        if executing_bayes == True and line.startswith('committed:'):
            numbers = re.findall(r'\d+', line)
            total_committed[0].append(int(numbers[0]))
            total_aborted[0].append(int(numbers[1]))
            executing_bayes = False


        #genome
        if 'Executing: ./genome/genome' in line:
            executing_bayes     = False
            executing_genome    = True
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_genome == True and line.startswith('First stage time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            first_stage_time[1].append(float(numbers[0]))
            second_stage_time[1].append(float(numbers[1]))
        if executing_genome == True and line.startswith('Switch time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            switch_time[1].append(float(numbers[0]))
            run_tx_time[1].append(float(numbers[1]))
        if executing_genome == True and line.startswith('commit cause by switch:'):
            numbers = re.findall(r'\d+', line)
            switch_committed[1].append(int(numbers[0]))
            switch_aborted[1].append(int(numbers[1]))
        if executing_genome == True and line.startswith('committed:'):
            numbers = re.findall(r'\d+', line)
            total_committed[1].append(int(numbers[0]))
            total_aborted[1].append(int(numbers[1]))
            executing_genome  = False

        #intruder
        if 'Executing: ./intruder/intruder' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = True
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_intruder == True and line.startswith('First stage time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            first_stage_time[2].append(float(numbers[0]))
            second_stage_time[2].append(float(numbers[1]))
        if executing_intruder == True and line.startswith('Switch time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            switch_time[2].append(float(numbers[0]))
            run_tx_time[2].append(float(numbers[1]))
        if executing_intruder == True and line.startswith('commit cause by switch:'):
            numbers = re.findall(r'\d+', line)
            switch_committed[2].append(int(numbers[0]))
            switch_aborted[2].append(int(numbers[1]))
        if executing_intruder == True and line.startswith('committed:'):
            numbers = re.findall(r'\d+', line)
            total_committed[2].append(int(numbers[0]))
            total_aborted[2].append(int(numbers[1]))
            executing_intruder  = False

        #kmeans1
        if 'Executing: ./kmeans/kmeans -m40 -n40' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = True
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_kmeans1 == True and line.startswith('First stage time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            first_stage_time[3].append(float(numbers[0]))
            second_stage_time[3].append(float(numbers[1]))
        if executing_kmeans1 == True and line.startswith('Switch time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            switch_time[3].append(float(numbers[0]))
            run_tx_time[3].append(float(numbers[1]))
        if executing_kmeans1 == True and line.startswith('commit cause by switch:'):
            numbers = re.findall(r'\d+', line)
            switch_committed[3].append(int(numbers[0]))
            switch_aborted[3].append(int(numbers[1]))
        if executing_kmeans1 == True and line.startswith('committed:'):
            numbers = re.findall(r'\d+', line)
            total_committed[3].append(int(numbers[0]))
            total_aborted[3].append(int(numbers[1]))
            executing_kmeans1  = False

        #kmeans2
        if 'Executing: ./kmeans/kmeans -m15 -n15' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = True
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_kmeans2 == True and line.startswith('First stage time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            first_stage_time[4].append(float(numbers[0]))
            second_stage_time[4].append(float(numbers[1]))
        if executing_kmeans2 == True and line.startswith('Switch time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            switch_time[4].append(float(numbers[0]))
            run_tx_time[4].append(float(numbers[1]))
        if executing_kmeans2 == True and line.startswith('commit cause by switch:'):
            numbers = re.findall(r'\d+', line)
            switch_committed[4].append(int(numbers[0]))
            switch_aborted[4].append(int(numbers[1]))
        if executing_kmeans2 == True and line.startswith('committed:'):
            numbers = re.findall(r'\d+', line)
            total_committed[4].append(int(numbers[0]))
            total_aborted[4].append(int(numbers[1]))
            executing_kmeans2  = False


        #labyrinth
        if 'Executing: ./labyrinth/labyrinth' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = True
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_labyrinth == True and line.startswith('First stage time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            first_stage_time[5].append(float(numbers[0]))
            second_stage_time[5].append(float(numbers[1]))
        if executing_labyrinth == True and line.startswith('Switch time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            switch_time[5].append(float(numbers[0]))
            run_tx_time[5].append(float(numbers[1]))
        if executing_labyrinth == True and line.startswith('commit cause by switch:'):
            numbers = re.findall(r'\d+', line)
            switch_committed[5].append(int(numbers[0]))
            switch_aborted[5].append(int(numbers[1]))
        if executing_labyrinth == True and line.startswith('committed:'):
            numbers = re.findall(r'\d+', line)
            total_committed[5].append(int(numbers[0]))
            total_aborted[5].append(int(numbers[1]))
            executing_labyrinth  = False


        #ssca2
        if 'Executing: ./ssca2/ssca2' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = True
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = False
        if executing_ssca2 == True and line.startswith('First stage time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            first_stage_time[6].append(float(numbers[0]))
            second_stage_time[6].append(float(numbers[1]))
        if executing_ssca2 == True and line.startswith('Switch time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            switch_time[6].append(float(numbers[0]))
            run_tx_time[6].append(float(numbers[1]))
        if executing_ssca2 == True and line.startswith('commit cause by switch:'):
            numbers = re.findall(r'\d+', line)
            switch_committed[6].append(int(numbers[0]))
            switch_aborted[6].append(int(numbers[1]))
        if executing_ssca2 == True and line.startswith('committed:'):
            numbers = re.findall(r'\d+', line)
            total_committed[6].append(int(numbers[0]))
            total_aborted[6].append(int(numbers[1]))
            executing_ssca2  = False


        #vacation1
        if 'Executing: ./vacation/vacation -n2' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = True
            executing_vacation2 = False
            executing_yada      = False
        if executing_vacation1 == True and line.startswith('First stage time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            first_stage_time[7].append(float(numbers[0]))
            second_stage_time[7].append(float(numbers[1]))
        if executing_vacation1 == True and line.startswith('Switch time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            switch_time[7].append(float(numbers[0]))
            run_tx_time[7].append(float(numbers[1]))
        if executing_vacation1 == True and line.startswith('commit cause by switch:'):
            numbers = re.findall(r'\d+', line)
            switch_committed[7].append(int(numbers[0]))
            switch_aborted[7].append(int(numbers[1]))
        if executing_vacation1 == True and line.startswith('committed:'):
            numbers = re.findall(r'\d+', line)
            total_committed[7].append(int(numbers[0]))
            total_aborted[7].append(int(numbers[1]))
            executing_vacation1  = False


        #vacation2
        if 'Executing: ./vacation/vacation -n4' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = True
            executing_yada      = False
        if executing_vacation2 == True and line.startswith('First stage time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            first_stage_time[8].append(float(numbers[0]))
            second_stage_time[8].append(float(numbers[1]))
        if executing_vacation2 == True and line.startswith('Switch time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            switch_time[8].append(float(numbers[0]))
            run_tx_time[8].append(float(numbers[1]))
        if executing_vacation2 == True and line.startswith('commit cause by switch:'):
            numbers = re.findall(r'\d+', line)
            switch_committed[8].append(int(numbers[0]))
            switch_aborted[8].append(int(numbers[1]))
        if executing_vacation2 == True and line.startswith('committed:'):
            numbers = re.findall(r'\d+', line)
            total_committed[8].append(int(numbers[0]))
            total_aborted[8].append(int(numbers[1]))
            executing_vacation2  = False


        #yada
        if 'Executing: ./yada/yada' in line:
            executing_bayes     = False
            executing_genome    = False
            executing_intruder  = False
            executing_kmeans1   = False
            executing_kmeans2   = False
            executing_labyrinth = False
            executing_ssca2     = False
            executing_vacation1 = False
            executing_vacation2 = False
            executing_yada      = True
        if executing_yada == True and line.startswith('First stage time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            first_stage_time[9].append(float(numbers[0]))
            second_stage_time[9].append(float(numbers[1]))
        if executing_yada == True and line.startswith('Switch time:'):
            numbers = re.findall(r'\d+\.\d+', line)
            switch_time[9].append(float(numbers[0]))
            run_tx_time[9].append(float(numbers[1]))
        if executing_yada == True and line.startswith('commit cause by switch:'):
            numbers = re.findall(r'\d+', line)
            switch_committed[9].append(int(numbers[0]))
            switch_aborted[9].append(int(numbers[1]))
        if executing_yada == True and line.startswith('committed:'):
            numbers = re.findall(r'\d+', line)
            total_committed[9].append(int(numbers[0]))
            total_aborted[9].append(int(numbers[1]))
            executing_yada = False

    avg_first_stage_time[0].append(sum(first_stage_time[0]) / len(first_stage_time[0]) )if len(first_stage_time[0]) > 0 else avg_first_stage_time[0].append(0) 
    avg_first_stage_time[1].append(sum(first_stage_time[1]) / len(first_stage_time[1]) )if len(first_stage_time[1]) > 0 else avg_first_stage_time[1].append(0) 
    avg_first_stage_time[2].append(sum(first_stage_time[2]) / len(first_stage_time[2]) )if len(first_stage_time[2]) > 0 else avg_first_stage_time[2].append(0) 
    avg_first_stage_time[3].append(sum(first_stage_time[3]) / len(first_stage_time[3]) )if len(first_stage_time[3]) > 0 else avg_first_stage_time[3].append(0) 
    avg_first_stage_time[4].append(sum(first_stage_time[4]) / len(first_stage_time[4]) )if len(first_stage_time[4]) > 0 else avg_first_stage_time[4].append(0) 
    avg_first_stage_time[5].append(sum(first_stage_time[5]) / len(first_stage_time[5]) )if len(first_stage_time[5]) > 0 else avg_first_stage_time[5].append(0) 
    avg_first_stage_time[6].append(sum(first_stage_time[6]) / len(first_stage_time[6]) )if len(first_stage_time[6]) > 0 else avg_first_stage_time[6].append(0) 
    avg_first_stage_time[7].append(sum(first_stage_time[7]) / len(first_stage_time[7]) )if len(first_stage_time[7]) > 0 else avg_first_stage_time[7].append(0) 
    avg_first_stage_time[8].append(sum(first_stage_time[8]) / len(first_stage_time[8]) )if len(first_stage_time[8]) > 0 else avg_first_stage_time[8].append(0) 
    avg_first_stage_time[9].append(sum(first_stage_time[9]) / len(first_stage_time[9]) )if len(first_stage_time[9]) > 0 else avg_first_stage_time[9].append(0)

    avg_second_stage_time[0].append(sum(second_stage_time[0]) / len(second_stage_time[0]) )if len(second_stage_time[0]) > 0 else avg_second_stage_time[0].append(0) 
    avg_second_stage_time[1].append(sum(second_stage_time[1]) / len(second_stage_time[1]) )if len(second_stage_time[1]) > 0 else avg_second_stage_time[1].append(0) 
    avg_second_stage_time[2].append(sum(second_stage_time[2]) / len(second_stage_time[2]) )if len(second_stage_time[2]) > 0 else avg_second_stage_time[2].append(0) 
    avg_second_stage_time[3].append(sum(second_stage_time[3]) / len(second_stage_time[3]) )if len(second_stage_time[3]) > 0 else avg_second_stage_time[3].append(0) 
    avg_second_stage_time[4].append(sum(second_stage_time[4]) / len(second_stage_time[4]) )if len(second_stage_time[4]) > 0 else avg_second_stage_time[4].append(0) 
    avg_second_stage_time[5].append(sum(second_stage_time[5]) / len(second_stage_time[5]) )if len(second_stage_time[5]) > 0 else avg_second_stage_time[5].append(0) 
    avg_second_stage_time[6].append(sum(second_stage_time[6]) / len(second_stage_time[6]) )if len(second_stage_time[6]) > 0 else avg_second_stage_time[6].append(0) 
    avg_second_stage_time[7].append(sum(second_stage_time[7]) / len(second_stage_time[7]) )if len(second_stage_time[7]) > 0 else avg_second_stage_time[7].append(0) 
    avg_second_stage_time[8].append(sum(second_stage_time[8]) / len(second_stage_time[8]) )if len(second_stage_time[8]) > 0 else avg_second_stage_time[8].append(0) 
    avg_second_stage_time[9].append(sum(second_stage_time[9]) / len(second_stage_time[9]) )if len(second_stage_time[9]) > 0 else avg_second_stage_time[9].append(0)

    avg_switch_time[0].append(sum(switch_time[0]) / len(switch_time[0]) )if len(switch_time[0]) > 0 else avg_switch_time[0].append(0) 
    avg_switch_time[1].append(sum(switch_time[1]) / len(switch_time[1]) )if len(switch_time[1]) > 0 else avg_switch_time[1].append(0) 
    avg_switch_time[2].append(sum(switch_time[2]) / len(switch_time[2]) )if len(switch_time[2]) > 0 else avg_switch_time[2].append(0) 
    avg_switch_time[3].append(sum(switch_time[3]) / len(switch_time[3]) )if len(switch_time[3]) > 0 else avg_switch_time[3].append(0) 
    avg_switch_time[4].append(sum(switch_time[4]) / len(switch_time[4]) )if len(switch_time[4]) > 0 else avg_switch_time[4].append(0) 
    avg_switch_time[5].append(sum(switch_time[5]) / len(switch_time[5]) )if len(switch_time[5]) > 0 else avg_switch_time[5].append(0) 
    avg_switch_time[6].append(sum(switch_time[6]) / len(switch_time[6]) )if len(switch_time[6]) > 0 else avg_switch_time[6].append(0) 
    avg_switch_time[7].append(sum(switch_time[7]) / len(switch_time[7]) )if len(switch_time[7]) > 0 else avg_switch_time[7].append(0) 
    avg_switch_time[8].append(sum(switch_time[8]) / len(switch_time[8]) )if len(switch_time[8]) > 0 else avg_switch_time[8].append(0) 
    avg_switch_time[9].append(sum(switch_time[9]) / len(switch_time[9]) )if len(switch_time[9]) > 0 else avg_switch_time[9].append(0)

    avg_run_tx_time[0].append(sum(run_tx_time[0]) / len(run_tx_time[0]) )if len(run_tx_time[0]) > 0 else avg_run_tx_time[0].append(0) 
    avg_run_tx_time[1].append(sum(run_tx_time[1]) / len(run_tx_time[1]) )if len(run_tx_time[1]) > 0 else avg_run_tx_time[1].append(0) 
    avg_run_tx_time[2].append(sum(run_tx_time[2]) / len(run_tx_time[2]) )if len(run_tx_time[2]) > 0 else avg_run_tx_time[2].append(0) 
    avg_run_tx_time[3].append(sum(run_tx_time[3]) / len(run_tx_time[3]) )if len(run_tx_time[3]) > 0 else avg_run_tx_time[3].append(0) 
    avg_run_tx_time[4].append(sum(run_tx_time[4]) / len(run_tx_time[4]) )if len(run_tx_time[4]) > 0 else avg_run_tx_time[4].append(0) 
    avg_run_tx_time[5].append(sum(run_tx_time[5]) / len(run_tx_time[5]) )if len(run_tx_time[5]) > 0 else avg_run_tx_time[5].append(0) 
    avg_run_tx_time[6].append(sum(run_tx_time[6]) / len(run_tx_time[6]) )if len(run_tx_time[6]) > 0 else avg_run_tx_time[6].append(0) 
    avg_run_tx_time[7].append(sum(run_tx_time[7]) / len(run_tx_time[7]) )if len(run_tx_time[7]) > 0 else avg_run_tx_time[7].append(0) 
    avg_run_tx_time[8].append(sum(run_tx_time[8]) / len(run_tx_time[8]) )if len(run_tx_time[8]) > 0 else avg_run_tx_time[8].append(0) 
    avg_run_tx_time[9].append(sum(run_tx_time[9]) / len(run_tx_time[9]) )if len(run_tx_time[9]) > 0 else avg_run_tx_time[9].append(0)
    
    avg_switch_committed[0].append(sum(switch_committed[0]) / len(switch_committed[0]) )if len(switch_committed[0]) > 0 else avg_switch_committed[0].append(0) 
    avg_switch_committed[1].append(sum(switch_committed[1]) / len(switch_committed[1]) )if len(switch_committed[1]) > 0 else avg_switch_committed[1].append(0) 
    avg_switch_committed[2].append(sum(switch_committed[2]) / len(switch_committed[2]) )if len(switch_committed[2]) > 0 else avg_switch_committed[2].append(0) 
    avg_switch_committed[3].append(sum(switch_committed[3]) / len(switch_committed[3]) )if len(switch_committed[3]) > 0 else avg_switch_committed[3].append(0) 
    avg_switch_committed[4].append(sum(switch_committed[4]) / len(switch_committed[4]) )if len(switch_committed[4]) > 0 else avg_switch_committed[4].append(0) 
    avg_switch_committed[5].append(sum(switch_committed[5]) / len(switch_committed[5]) )if len(switch_committed[5]) > 0 else avg_switch_committed[5].append(0) 
    avg_switch_committed[6].append(sum(switch_committed[6]) / len(switch_committed[6]) )if len(switch_committed[6]) > 0 else avg_switch_committed[6].append(0) 
    avg_switch_committed[7].append(sum(switch_committed[7]) / len(switch_committed[7]) )if len(switch_committed[7]) > 0 else avg_switch_committed[7].append(0) 
    avg_switch_committed[8].append(sum(switch_committed[8]) / len(switch_committed[8]) )if len(switch_committed[8]) > 0 else avg_switch_committed[8].append(0) 
    avg_switch_committed[9].append(sum(switch_committed[9]) / len(switch_committed[9]) )if len(switch_committed[9]) > 0 else avg_switch_committed[9].append(0)

    avg_switch_aborted[0].append(sum(switch_aborted[0]) / len(switch_aborted[0]) )if len(switch_aborted[0]) > 0 else avg_switch_aborted[0].append(0) 
    avg_switch_aborted[1].append(sum(switch_aborted[1]) / len(switch_aborted[1]) )if len(switch_aborted[1]) > 0 else avg_switch_aborted[1].append(0) 
    avg_switch_aborted[2].append(sum(switch_aborted[2]) / len(switch_aborted[2]) )if len(switch_aborted[2]) > 0 else avg_switch_aborted[2].append(0) 
    avg_switch_aborted[3].append(sum(switch_aborted[3]) / len(switch_aborted[3]) )if len(switch_aborted[3]) > 0 else avg_switch_aborted[3].append(0) 
    avg_switch_aborted[4].append(sum(switch_aborted[4]) / len(switch_aborted[4]) )if len(switch_aborted[4]) > 0 else avg_switch_aborted[4].append(0) 
    avg_switch_aborted[5].append(sum(switch_aborted[5]) / len(switch_aborted[5]) )if len(switch_aborted[5]) > 0 else avg_switch_aborted[5].append(0) 
    avg_switch_aborted[6].append(sum(switch_aborted[6]) / len(switch_aborted[6]) )if len(switch_aborted[6]) > 0 else avg_switch_aborted[6].append(0) 
    avg_switch_aborted[7].append(sum(switch_aborted[7]) / len(switch_aborted[7]) )if len(switch_aborted[7]) > 0 else avg_switch_aborted[7].append(0) 
    avg_switch_aborted[8].append(sum(switch_aborted[8]) / len(switch_aborted[8]) )if len(switch_aborted[8]) > 0 else avg_switch_aborted[8].append(0) 
    avg_switch_aborted[9].append(sum(switch_aborted[9]) / len(switch_aborted[9]) )if len(switch_aborted[9]) > 0 else avg_switch_aborted[9].append(0)

    avg_total_committed[0].append(sum(total_committed[0]) / len(total_committed[0]) )if len(total_committed[0]) > 0 else avg_total_committed[0].append(0) 
    avg_total_committed[1].append(sum(total_committed[1]) / len(total_committed[1]) )if len(total_committed[1]) > 0 else avg_total_committed[1].append(0) 
    avg_total_committed[2].append(sum(total_committed[2]) / len(total_committed[2]) )if len(total_committed[2]) > 0 else avg_total_committed[2].append(0) 
    avg_total_committed[3].append(sum(total_committed[3]) / len(total_committed[3]) )if len(total_committed[3]) > 0 else avg_total_committed[3].append(0) 
    avg_total_committed[4].append(sum(total_committed[4]) / len(total_committed[4]) )if len(total_committed[4]) > 0 else avg_total_committed[4].append(0) 
    avg_total_committed[5].append(sum(total_committed[5]) / len(total_committed[5]) )if len(total_committed[5]) > 0 else avg_total_committed[5].append(0) 
    avg_total_committed[6].append(sum(total_committed[6]) / len(total_committed[6]) )if len(total_committed[6]) > 0 else avg_total_committed[6].append(0) 
    avg_total_committed[7].append(sum(total_committed[7]) / len(total_committed[7]) )if len(total_committed[7]) > 0 else avg_total_committed[7].append(0) 
    avg_total_committed[8].append(sum(total_committed[8]) / len(total_committed[8]) )if len(total_committed[8]) > 0 else avg_total_committed[8].append(0) 
    avg_total_committed[9].append(sum(total_committed[9]) / len(total_committed[9]) )if len(total_committed[9]) > 0 else avg_total_committed[9].append(0)

    avg_total_aborted[0].append(sum(total_aborted[0]) / len(total_aborted[0]) )if len(total_aborted[0]) > 0 else avg_total_aborted[0].append(0) 
    avg_total_aborted[1].append(sum(total_aborted[1]) / len(total_aborted[1]) )if len(total_aborted[1]) > 0 else avg_total_aborted[1].append(0) 
    avg_total_aborted[2].append(sum(total_aborted[2]) / len(total_aborted[2]) )if len(total_aborted[2]) > 0 else avg_total_aborted[2].append(0) 
    avg_total_aborted[3].append(sum(total_aborted[3]) / len(total_aborted[3]) )if len(total_aborted[3]) > 0 else avg_total_aborted[3].append(0) 
    avg_total_aborted[4].append(sum(total_aborted[4]) / len(total_aborted[4]) )if len(total_aborted[4]) > 0 else avg_total_aborted[4].append(0) 
    avg_total_aborted[5].append(sum(total_aborted[5]) / len(total_aborted[5]) )if len(total_aborted[5]) > 0 else avg_total_aborted[5].append(0) 
    avg_total_aborted[6].append(sum(total_aborted[6]) / len(total_aborted[6]) )if len(total_aborted[6]) > 0 else avg_total_aborted[6].append(0) 
    avg_total_aborted[7].append(sum(total_aborted[7]) / len(total_aborted[7]) )if len(total_aborted[7]) > 0 else avg_total_aborted[7].append(0) 
    avg_total_aborted[8].append(sum(total_aborted[8]) / len(total_aborted[8]) )if len(total_aborted[8]) > 0 else avg_total_aborted[8].append(0) 
    avg_total_aborted[9].append(sum(total_aborted[9]) / len(total_aborted[9]) )if len(total_aborted[9]) > 0 else avg_total_aborted[9].append(0)

def normalized (
        dataset_origin,
        dataset_normalized,
        dataset_suicide     ):
    for origin_data , suicide_data in zip(dataset_origin, dataset_suicide):
        normalized_num = suicide_data[0]
        normalized_result = [normalized_num / number if number != 0 else 0 for number in origin_data]
        dataset_normalized.append(normalized_result)
    
    