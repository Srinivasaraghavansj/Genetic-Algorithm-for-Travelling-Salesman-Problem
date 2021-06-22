
"""
Author:Srinivasaraghavan Seshadhri R00195470
file:runner.py

This file was created from scratch to run the given TSP 
configurations at maximum time efficiency using multiprocessing.
    Basically this is a file that automates running TSP in
different configurations without manual intervention.

This file benchmarks the TSP problems according to given
configs and stores them in separate folders, with the
individual report and output format mentioned in the assignment.

'Benchmark%.tsp' files are the report file which runs a given
config 5 times and reports the statistics.

General python code utilizes only 1 thread of the CPU.
In our TSP problem, that takes sevaral days if its run multiple configs.
Therefore to speed up the process, multiprocessing has been made and the
TSPs will be run parallely, using up all the available threads, speeding
up the whole process.

Please note that this code has been built as generic as possible, for
usage in other similar applications.
"""


#importing the required libraries
import multiprocessing
from TSP_R00195470 import *
from time import time
from statistics import mean, median
import os

#Mention the TSP inst file names
TSP_FILES = ["inst-7.tsp", "inst-19.tsp","inst-20.tsp"]

#Declaring the required configs as per assignment,
#Please refer the TSP_R00195470.py file to know the below keys
configs = [
    {
        '_initPop' : 'random',
        '_selectiontype' : 'bts',
        '_crossovertype' : 'o1c',
        '_mutationtype' : 'im'
    },
        {
        '_initPop' : 'random',
        '_selectiontype' : 'bts',
        '_crossovertype' : 'uc',
        '_mutationtype' : 'sm'
    },
        {
        '_initPop' : 'random',
        '_selectiontype' : 'bts',
        '_crossovertype' : 'o1c',
        '_mutationtype' : 'sm'
    },
        {
        '_initPop' : 'random',
        '_selectiontype' : 'bts',
        '_crossovertype' : 'uc',
        '_mutationtype' : 'im'
    },
        {
        '_initPop' : 'nn',
        '_selectiontype' : 'bts',
        '_crossovertype' : 'o1c',
        '_mutationtype' : 'sm'
    },
        {
        '_initPop' : 'nn',
        '_selectiontype' : 'bts',
        '_crossovertype' : 'uc',
        '_mutationtype' : 'im'
    }
]

#Setting up parameters to run in combinations and permutations
popSizes = [50 ,100 , 150]
mutationRates = [0.05,0.1]
maxIter = 500


#This runs the TSP in the given config once, saves and returns reqd info
def benchmark(_fName, output_file, _popSize, _mutationRate, _maxIterations, _initPop = 'random',_selectiontype = 'rs',_crossovertype = 'rc',_mutationtype = 'rm'):
    ga = BasicTSP(_fName, _popSize, _mutationRate, _maxIterations, _initPop = 'random',_selectiontype = 'rs',_crossovertype = 'rc',_mutationtype = 'rm')
    start = time()
    ga.search() 
    duration = time() - start

    saveSolution(output_file, ga.best.genes, ga.best.fitness)
    return duration, ga.best.fitness

#This runs the TSP upto mentioned number of times, saves the files in appropriate folders
def repeat(folder_name,n_times, _fName, _popSize, _mutationRate, _maxIterations, _initPop = 'random',_selectiontype = 'rs',_crossovertype = 'rc',_mutationtype = 'rm'):
    folder = folder_name + f"/{_initPop}_{_selectiontype}_{_crossovertype}_{_mutationtype}_{_popSize}_{_mutationRate}_{_maxIterations}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    f = open(folder+"/benchmark_"+_fName, "w")
    try:
        durations = []
        fitnesses = []
        for ind in range(n_times):
            duration, fitness = benchmark(_fName, folder+f"/run_{ind}_"+_fName, _popSize, _mutationRate, _maxIterations, _initPop,_selectiontype,_crossovertype,_mutationtype)
            f.write(f'Run {ind+1}: {duration} secs, Fitness: {fitness}\n')
            durations.append(duration)
            fitnesses.append(fitness)
        mean_dur = mean(durations)
        mean_fitness = mean(fitnesses)
        median_dur = median(durations)
        median_fitness = median(fitnesses)
        f.write('\n')
        f.write(f"Mean duration: {mean_dur}\nMedian duration: {median_dur}\nMean fitness: {mean_fitness}\nMedian fitness: {median_fitness}")
        f.write('\n')
        f.write(f"""
File Name: {_fName}
Population Size: {_popSize}
Mutation Rate: {_mutationRate}
Number of Iterations: {_maxIterations}
Initial population selection method: {"Nearest Neighbour Selection" if _initPop == 'nn'  else "Random Selection"}
Parent Selection method: {"Random Selection" if _selectiontype == 'rs'  else "Binary Tournament Selection"}
Crossover method: {"Random Crossover" if _crossovertype == 'rc' else  "Uniform Crossover" if _crossovertype == 'uc' else "Order1 Crossover"}
Mutation method: {"Random Mutation" if _mutationtype == 'rm' else "scrambleMutation" if _mutationtype == 'sm' else "Inversion Mutation"}
""")
        f.close()
    except KeyboardInterrupt:
        f.close()

#This creates processes, assigns them for multiprocessing.
#Each permutation and combination is an individual process
def main(folder_name):
    processes = []
    try:
        for f in TSP_FILES:
            for popSize in popSizes:
                for mut in mutationRates:
                    for config in configs:
                        params = {'folder_name':folder_name,'n_times': 5, '_fName':f, '_popSize': popSize, '_mutationRate':mut, '_maxIterations': maxIter}
                        params.update(config)
                        p = multiprocessing.Process(target=repeat, kwargs=params)
                        processes.append(p)
                        p.start()
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()

#It expects a folder name as sys arg to create that folder and to save all the run details in them.
if __name__ == '__main__':
    main(sys.argv[1])