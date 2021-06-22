This folder is submitted by:
Srinivasaraghavan Seshadhri
R00195470
MSc Artificial Intelligence Student
Metaheuristic Optimization Assignment 1
8 Nov 2020

MHO Assignment 1_R00195470.pdf contains the assignment report(just for convinience)

inst-7.tsp,inst-19.tsp,inst-20.tsp are the given TSP instances in the assignment

Individual.py is a py module used in the Assignment. This was also given by
the lecturer, it is unmodified.

TSP_R00195470.py  is the main assignment file, the given template has been edited
to the specifications. The I/O are also according to the specification in the assignment.
to run use the below command line:
>>python TSP_R00195470.py <Instance File Name>

runner.py is an additional program designed to evaluate the different configurations of
the given TSP. It runs the permutations and combinations of the given parameters and stores all the results in the specified folder.
To run, use the code below:
>>python runner.py <New folder name to save the results>

TSP_report_gen.py is an additional program to look into the subfolders, grab all the benchmark result files and consolidate the data into 1 TSP_Benchmark_Report.xlsx file.
To run, use the code below:
>>python TSP_report_gen.py

TSP_Benchmark_Report.xlsx contains all the consolidated results as a spreadsheet for easy analysis.

Results folder contains all the results of the run TSPs in separate folders, which in turn contain the benchmark files, and the solution files.