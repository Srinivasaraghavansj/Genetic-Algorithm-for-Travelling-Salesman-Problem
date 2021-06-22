"""
Author:Srinivasaraghavan Seshadhri R00195470
file:TSP_report_gen.py


The runner.py saves each data in each subfolder.
It is difficult to manually collect the data and consolidate them.

This file searches for benchmark%.tsp files in all sub folders, reads them
and consolidates the information in a reasonable format.

Please note that this code is not generic at the moment and was built
for this application only, due to time constraint. However with a little
more effort and time, this can be easily converted into a generic code.

All this file does is, it gathers the above specified information
and stores it as TSP_Benchmark_Report.xlsx
"""


###So far developed code compiled together
import os
import pandas as pd
rootdir = os.getcwd()
benchmarks = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if ".tsp" in file and "benchmark" in file:
            benchmarks.append(os.path.join(subdir, file))
#             print(os.path.join(subdir, file))
diction = {
    "File Name":[],
    "Population Size":[],
    "Mutation Rate":[],
    "Number of Iterations":[],
    "Initial population selection method":[],
    "Parent Selection method":[],
    "Crossover method":[],
    "Mutation method":[],
    "Mean duration":[],
    "Median duration":[],
    "Mean fitness":[],
    "Median fitness":[],
    "Run 1 duration":[],
    "Run 2 duration":[],
    "Run 3 duration":[],
    "Run 4 duration":[],
    "Run 5 duration":[],
    "Run 1 Fitness":[],
    "Run 2 Fitness":[],
    "Run 3 Fitness":[],
    "Run 4 Fitness":[],
    "Run 5 Fitness":[]
}
for bench in benchmarks:
    a = []
    b = []
    with open(bench, 'r') as reader:
        for line in reader.readlines():
            a.append(line[:-1])
    for i in range(len(a)):
        a[i] = a[i].replace(f'Run {i+1}',f'Run {i+1} duration')
        a[i] = a[i].replace(f'Fitness', f'Run {i+1} Fitness')
    columns = ["File Name","Population Size","Mutation Rate","Number of Iterations","Initial population selection method","Parent Selection method","Crossover method","Mutation method","Mean duration","Median duration","Mean fitness","Median fitness","Run 1 duration","Run 2 duration","Run 3 duration","Run 4 duration","Run 5 duration","Run 1 Fitness","Run 2 Fitness","Run 3 Fitness","Run 4 Fitness","Run 5 Fitness"]
    for column in columns:
        for i in a:
            if column in i:
                b.append(i)
    c = b[:12]
    d = []
    for i in b[-5:]:
        d.append(i.split(',')[0])
        d.append(i.split(',')[1])
    for i in range(len(d)):
        d[i] = d[i].strip()
    b = c+d
    for i in range(len(b)):
        if ' secs' in b[i]:
            b[i] = b[i][:-5]
    for i in b:
        z = i.split(":")
        y = diction[z[0].strip()]
        y.append(z[1].strip())
        diction[z[0].strip()] = y
df = pd.DataFrame(diction)
df = df.round(3)
df.to_excel("TSP_Benchmark_Report.xlsx")