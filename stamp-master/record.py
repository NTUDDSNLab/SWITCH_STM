import re
import matplotlib.pyplot as plt

average_bayes     = []
average_genome    = []
average_intruder  = []
average_kmeans1   = []
average_kmeans2   = []
average_labyrinth = []
average_ssca2     = []
average_vacation1 = []
average_vacation2 = []
average_yada      = []

shrink_average_bayes     = []
shrink_average_genome    = []
shrink_average_intruder  = []
shrink_average_kmeans1   = []
shrink_average_kmeans2   = []
shrink_average_labyrinth = []
shrink_average_ssca2     = []
shrink_average_vacation1 = []
shrink_average_vacation2 = []
shrink_average_yada      = []

file_list = ['real_karma_1.stm'
            ,'real_karma_2.stm'
            ,'real_karma_4.stm'
            ,'real_karma_8.stm'
            ,'real_karma_16.stm'
            # ,'real_delay_32.stm'
            # ,'real_delay_64.stm'
            ]

file_list2 = ['real_polka_1.stm'
            , 'real_polka_2.stm'
            , 'real_polka_4.stm'
            , 'real_polka_8.stm'
            , 'real_polka_16.stm'
            # , 'real_delay_shrink_32.stm'
            # , 'real_delay_shrink_64.stm'
            ]
             
# start original data
for file_name in file_list:
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

    bayes_learn_time     = []
    genome_learn_time    = []
    intruder_learn_time  = []
    kmeans1_learn_time   = []
    kmeans2_learn_time   = []
    labyrinth_learn_time = []
    ssca2_learn_time     = []
    vacation1_learn_time = []
    vacation2_learn_time = []
    yada_learn_time      = []

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
            bayes_learn_time.append(float(data))
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
            genome_learn_time.append(float(data))
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
            intruder_learn_time.append(float(data))
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
            kmeans1_learn_time.append(float(data))
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
            kmeans2_learn_time.append(float(data))
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
            labyrinth_learn_time.append(float(data))
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
            ssca2_learn_time.append(float(data))
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
            vacation1_learn_time.append(float(data))
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
            vacation2_learn_time.append(float(data))
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
            yada_learn_time.append(float(data))
            executing_yada = False

    '''
    print("bayes_learn_time     ",bayes_learn_time     ) 
    print("genome_learn_time    ",genome_learn_time    ) 
    print("intruder_learn_time  ",intruder_learn_time  ) 
    print("kmeans1_learn_time   ",kmeans1_learn_time   ) 
    print("kmeans2_learn_time   ",kmeans2_learn_time   ) 
    print("labyrinth_learn_time ",labyrinth_learn_time ) 
    print("ssca2_learn_time     ",ssca2_learn_time     ) 
    print("vacation1_learn_time ",vacation1_learn_time ) 
    print("vacation2_learn_time ",vacation2_learn_time ) 
    print("yada_learn_time      ",yada_learn_time      )
    '''

    average_bayes    .append(sum(bayes_learn_time)    / len(bayes_learn_time)     )if len(bayes_learn_time) >     0 else average_bayes    .append(0) 
    average_genome   .append(sum(genome_learn_time)   / len(genome_learn_time)    )if len(genome_learn_time) >    0 else average_genome   .append(0) 
    average_intruder .append(sum(intruder_learn_time) / len(intruder_learn_time)  )if len(intruder_learn_time) >  0 else average_intruder .append(0) 
    average_kmeans1  .append(sum(kmeans1_learn_time)  / len(kmeans1_learn_time)   )if len(kmeans1_learn_time) >   0 else average_kmeans1  .append(0) 
    average_kmeans2  .append(sum(kmeans2_learn_time)  / len(kmeans2_learn_time)   )if len(kmeans2_learn_time) >   0 else average_kmeans2  .append(0) 
    average_labyrinth.append(sum(labyrinth_learn_time)/ len(labyrinth_learn_time) )if len(labyrinth_learn_time) > 0 else average_labyrinth.append(0) 
    average_ssca2    .append(sum(ssca2_learn_time)    / len(ssca2_learn_time)     )if len(ssca2_learn_time) >     0 else average_ssca2    .append(0) 
    average_vacation1.append(sum(vacation1_learn_time)/ len(vacation1_learn_time) )if len(vacation1_learn_time) > 0 else average_vacation1.append(0) 
    average_vacation2.append(sum(vacation2_learn_time)/ len(vacation2_learn_time) )if len(vacation2_learn_time) > 0 else average_vacation2.append(0) 
    average_yada     .append(sum(yada_learn_time)     / len(yada_learn_time)      )if len(yada_learn_time) >      0 else average_yada     .append(0)

    bayes_learn_time    .clear() 
    genome_learn_time   .clear() 
    intruder_learn_time .clear() 
    kmeans1_learn_time  .clear() 
    kmeans2_learn_time  .clear() 
    labyrinth_learn_time.clear() 
    ssca2_learn_time    .clear() 
    vacation1_learn_time.clear() 
    vacation2_learn_time.clear() 
    yada_learn_time     .clear() 
# end original data    

# start shrink data
for file_name in file_list2:
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

    bayes_learn_time     = []
    genome_learn_time    = []
    intruder_learn_time  = []
    kmeans1_learn_time   = []
    kmeans2_learn_time   = []
    labyrinth_learn_time = []
    ssca2_learn_time     = []
    vacation1_learn_time = []
    vacation2_learn_time = []
    yada_learn_time      = []

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
            bayes_learn_time.append(float(data))
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
            genome_learn_time.append(float(data))
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
            intruder_learn_time.append(float(data))
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
            kmeans1_learn_time.append(float(data))
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
            kmeans2_learn_time.append(float(data))
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
            labyrinth_learn_time.append(float(data))
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
            ssca2_learn_time.append(float(data))
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
            vacation1_learn_time.append(float(data))
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
            vacation2_learn_time.append(float(data))
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
            yada_learn_time.append(float(data))
            executing_yada = False

    '''
    print("bayes_learn_time     ",bayes_learn_time     ) 
    print("genome_learn_time    ",genome_learn_time    ) 
    print("intruder_learn_time  ",intruder_learn_time  ) 
    print("kmeans1_learn_time   ",kmeans1_learn_time   ) 
    print("kmeans2_learn_time   ",kmeans2_learn_time   ) 
    print("labyrinth_learn_time ",labyrinth_learn_time ) 
    print("ssca2_learn_time     ",ssca2_learn_time     ) 
    print("vacation1_learn_time ",vacation1_learn_time ) 
    print("vacation2_learn_time ",vacation2_learn_time ) 
    print("yada_learn_time      ",yada_learn_time      )
    '''

    shrink_average_bayes    .append(sum(bayes_learn_time)    / len(bayes_learn_time)     )if len(bayes_learn_time) >     0 else shrink_average_bayes    .append(0) 
    shrink_average_genome   .append(sum(genome_learn_time)   / len(genome_learn_time)    )if len(genome_learn_time) >    0 else shrink_average_genome   .append(0) 
    shrink_average_intruder .append(sum(intruder_learn_time) / len(intruder_learn_time)  )if len(intruder_learn_time) >  0 else shrink_average_intruder .append(0) 
    shrink_average_kmeans1  .append(sum(kmeans1_learn_time)  / len(kmeans1_learn_time)   )if len(kmeans1_learn_time) >   0 else shrink_average_kmeans1  .append(0) 
    shrink_average_kmeans2  .append(sum(kmeans2_learn_time)  / len(kmeans2_learn_time)   )if len(kmeans2_learn_time) >   0 else shrink_average_kmeans2  .append(0) 
    shrink_average_labyrinth.append(sum(labyrinth_learn_time)/ len(labyrinth_learn_time) )if len(labyrinth_learn_time) > 0 else shrink_average_labyrinth.append(0) 
    shrink_average_ssca2    .append(sum(ssca2_learn_time)    / len(ssca2_learn_time)     )if len(ssca2_learn_time) >     0 else shrink_average_ssca2    .append(0) 
    shrink_average_vacation1.append(sum(vacation1_learn_time)/ len(vacation1_learn_time) )if len(vacation1_learn_time) > 0 else shrink_average_vacation1.append(0) 
    shrink_average_vacation2.append(sum(vacation2_learn_time)/ len(vacation2_learn_time) )if len(vacation2_learn_time) > 0 else shrink_average_vacation2.append(0) 
    shrink_average_yada     .append(sum(yada_learn_time)     / len(yada_learn_time)      )if len(yada_learn_time) >      0 else shrink_average_yada     .append(0)

    bayes_learn_time    .clear() 
    genome_learn_time   .clear() 
    intruder_learn_time .clear() 
    kmeans1_learn_time  .clear() 
    kmeans2_learn_time  .clear() 
    labyrinth_learn_time.clear() 
    ssca2_learn_time    .clear() 
    vacation1_learn_time.clear() 
    vacation2_learn_time.clear() 
    yada_learn_time     .clear() 
# end shrink data    

'''
print("average_bayes     ",average_bayes     ) 
print("average_genome    ",average_genome    ) 
print("average_intruder  ",average_intruder  ) 
print("average_kmeans1   ",average_kmeans1   ) 
print("average_kmeans2   ",average_kmeans2   ) 
print("average_labyrinth ",average_labyrinth ) 
print("average_ssca2     ",average_ssca2     ) 
print("average_vacation1 ",average_vacation1 ) 
print("average_vacation2 ",average_vacation2 ) 
print("average_yada      ",average_yada      )
'''

datasets = [
    average_bayes,
    average_genome,
    average_intruder,
    average_kmeans1,
    average_kmeans2,
    average_labyrinth,
    average_ssca2,
    average_vacation1,
    average_vacation2,
    average_yada
]

datasets2 = [
    shrink_average_bayes,
    shrink_average_genome,
    shrink_average_intruder,
    shrink_average_kmeans1,
    shrink_average_kmeans2,
    shrink_average_labyrinth,
    shrink_average_ssca2,
    shrink_average_vacation1,
    shrink_average_vacation2,
    shrink_average_yada
]

labels = [
    'Bayes',
    'Genome',
    'Intruder',
    'KMeans1',
    'KMeans2',
    'Labyrinth',
    'SSCA2',
    'Vacation1',
    'Vacation2',
    'Yada'
]

x_values = [1,2,4,8,16]

for data, data2, label in zip(datasets, datasets2, labels):
    plt.plot(x_values, data,label='karma')
    plt.plot(x_values, data2,label='polka')
    plt.xlabel('number of threads')
    plt.ylabel('times (second)')
    plt.title(label)
    plt.xticks(x_values, x_values)
    plt.legend()
    plt.savefig(f'{label}_k_p.png')
    plt.clf()