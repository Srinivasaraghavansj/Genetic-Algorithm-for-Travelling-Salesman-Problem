

"""
Author:Srinivasaraghavan Seshadhri R00195470
file:TSP_R00195470.py

This file is the given template to solve our given TSP.
This file has been well commented and explained in all the places where changes have been made.
"""

import random
from Individual import *
from math import sqrt
import sys

myStudentNum = 195470 # R00195470 is student number, hence the numeric seed
random.seed(myStudentNum)

class BasicTSP:
    '''
    More paremeters have been added in the init function for more functionality as follows. 
    _initPop : Initial population type to be selected (random or nearest neighbour heuristic)
    _selectiontype :Parent selection type (Random or Binary Tournament Selection)
    _crossovertype : Crossover method (random,uniform or order 1 crossover)
    _mutationtype : Mutation Method (random, scramble or inversion mutation)
    '''
    def __init__(self, _fName, _popSize, _mutationRate, _maxIterations, _initPop = 'random',_selectiontype = 'rs',_crossovertype = 'rc',_mutationtype = 'rm'):
        """
        Parameters and general variables
        """

        self.population     = []
        self.matingPool     = []
        self.best           = None
        self.popSize        = _popSize
        self.genSize        = None
        self.mutationRate   = _mutationRate
        self.maxIterations  = _maxIterations
        self.iteration      = 0
        self.fName          = _fName
        self.data           = {}
        #updating the passed variables as self of the class
        self.initPop        = _initPop
        self.selectiontype  = _selectiontype
        self.crossovertype  = _crossovertype
        self.mutationtype   = _mutationtype
        self.readInstance()
        self.initPopulation()


    def readInstance(self):
        """
        Reading an instance from fName
        """
        file = open(self.fName, 'r')
        self.genSize = int(file.readline())
        self.data = {}
        for line in file:
            (cid, x, y) = line.split()
            self.data[int(cid)] = (int(x), int(y))
        file.close()

    def euclideanDistance(self, cityA, cityB):
        ##Euclidean distance
        #return sqrt( (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 )
        ##Rounding nearest integer
        return round( sqrt( (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 ) )

    # Choose first city randomly, thereafter append nearest unrouted city to last city added to rpute
    def nearest_neighbour_insertion(self, instance):
        cities = list(instance.keys())
        cIndex = random.randint(0, len(instance)-1)

        tCost = 0

        solution = [cities[cIndex]]

        del cities[cIndex]

        current_city = solution[0]
        while len(cities) > 0:
            bCity = cities[0]
            bCost = self.euclideanDistance(instance[current_city], instance[bCity])
            bIndex = 0
    #        print(bCity,bCost)
            for city_index in range(1, len(cities)):
                city = cities[city_index]
                cost = self.euclideanDistance(instance[current_city], instance[city])
    #            print(cities[city_index], "Cost: ",cost)
                if bCost > cost:
                    bCost = cost
                    bCity = city
                    bIndex = city_index
            current_city = bCity
            solution.append(current_city)
            del cities[bIndex]
        return solution

    def initPopulation(self):
        """
        Creating random individuals in the population
        """
        for i in range(0, self.popSize):
            if self.initPop == 'nn':
                individual = Individual(self.genSize, self.data, self.nearest_neighbour_insertion(self.data))
            elif self.initPop == 'random':
                individual = Individual(self.genSize, self.data,[])
            individual.computeFitness()
            self.population.append(individual)

        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
        print ("Best initial sol: ",self.best.getFitness())

    def updateBest(self, candidate):
        if self.best == None or candidate.getFitness() < self.best.getFitness():
            self.best = candidate.copy()
            print ("iteration: ",self.iteration, "best: ",self.best.getFitness())

    def randomSelection(self):
        """
        Random (uniform) selection of two individuals
        """
        indA = self.matingPool[ random.randint(0, self.popSize-1) ]
        indB = self.matingPool[ random.randint(0, self.popSize-1) ]
        return [indA, indB]

    def binaryTournamentSelection(self):
        """
        Binary Tournament Selection of two individuals
        """
        parents = []
        #Choosing 2 parents randomly in a list from the mating pool
        while len(parents) < 2:
            indA = self.matingPool[ random.randint(0, self.popSize-1) ]
            indB = self.matingPool[ random.randint(0, self.popSize-1) ]
            #Comparing their fitnesses and adding higher fitness one to parents list
            if indA.fitness > indB.fitness:
                if not indA in parents:
                    parents.append(indA)
            else:
                if not indB in parents:
                    parents.append(indB)
        #returning 2 parents ie. individuals
        return parents

    def uniformCrossover(self, indA, indB):
        """
        Uniform Crossover Implementation
        """
        #random Index values selected from parent A
        idx = random.sample([i for i in range(len(indA.genes))], k=int(len(indA.genes)/2))

        #Place corresponding A genes in the above chosen indices, None elsewhere
        childgene = [indA.genes[i] if(i in idx) else None for i in range(len(indA.genes))]

        #Replace None in child gene with genes from B in order
        for i in range(len(childgene)):
            if childgene[i] is None:
                for g in indB.genes:
                    if g not in childgene:
                        childgene[i] = g
                        break
        #return the Crossed individual
        return Individual(self.genSize, self.data, childgene)

    def order1Crossover(self, indA, indB):
        """
        Order-1 Crossover Implementation
        """
        #Collect corresponding genes of parents
        A = indA.genes
        B = indB.genes

        #Generate random locations a,b within genes
        a,b = random.randint(0,len(A)-1),random.randint(0,len(A)-1)

        #To check and get usable values for slicing the gene
        while a == b:
            a,b = random.randint(0,len(A)-1),random.randint(0,len(A)-1)
        if a > b:
            a,b = b,a

        #Select a portion of genes from A, based on a,b
        chunk = A[a:b]

        #Initialize childgenes as genes of B
        childgene = B.copy()

        #Remove genes in chunk from child gene
        for i in chunk:
            childgene.remove(i)

        #Shuffle the selected chunk genes and add it to end of child gene
        random.shuffle(chunk)
        childgene.extend(chunk)

        #Return the individual
        return Individual(self.genSize, self.data, childgene)
        
    def scrambleMutation(self, ind):
        """
        Scramble Mutation implementation
        """

        #To activate this function based on given mutation rate
        if random.random() > self.mutationRate:
            return

        #Generate random locations a,b within genes
        a,b = random.randint(0,len(A)-1),random.randint(0,len(A)-1)

        #To check and get usable values for slicing the gene
        while a == b:
            a,b = random.randint(0,len(A)-1),random.randint(0,len(A)-1)
        if a > b:
            a,b = b,a

        #Select a portion of genes from A, based on a,b
        chunk = A[a:b]

        #Shuffle the selected portion
        random.shuffle(chunk)

        #Replace the shuffled elements within the gene in the previously sliced section
        ind.genes[a:b] = chunk

    def inversionMutation(self, ind):
        """
        Inversion Mutation implementation
        """
        #To activate this function based on given mutation rate
        if random.random() > self.mutationRate:
            return

        #Generate random locations a,b within genes
        a,b = random.randint(0,len(A)-1),random.randint(0,len(A)-1)

        #To check and get usable values for slicing the gene
        while a == b:
            a,b = random.randint(0,len(A)-1),random.randint(0,len(A)-1)
        if a > b:
            a,b = b,a

        #Select a portion of genes from A, based on a,b
        chunk = A[a:b]

        #Reverse the selected portion
        chunk = chunk[::-1]

        #Insert the reversed portion in the gene from the previously sliced section
        ind.genes[a:b] = chunk

    def crossover(self, indA, indB):
        """
        Executes a dummy crossover and returns the genes for a new individual
        """
        midP=int(self.genSize/2)
        cgenes = indA.genes[0:midP]
        for i in range(0, self.genSize):
            if indB.genes[i] not in cgenes:
                cgenes.append(indB.genes[i])
        child = Individual(self.genSize, self.data, cgenes)
        return child

    def mutation(self, ind):
        """
        Mutate an individual by swaping two cities with certain probability (i.e., mutation rate)
        """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp

        ind.computeFitness()
        self.updateBest(ind)

    def updateMatingPool(self):
        """
        Updating the mating pool before creating a new generation
        """
        self.matingPool = []
        for ind_i in self.population:
            self.matingPool.append( ind_i.copy() )

    def newGeneration(self):
        """
        Creating a new generation
        1. Selection
        2. Crossover
        3. Mutation
        """
        for i in range(0, len(self.population)):
            """
            Depending of your experiment you need to use the most suitable algorithms for:
            1. Select two candidates
            2. Apply Crossover
            3. Apply Mutation
            """
            if self.selectiontype == 'rs':
                parent1, parent2 = self.randomSelection()
            elif self.selectiontype == 'bts':
                parent1, parent2 = self.binaryTournamentSelection()
                
            if self.crossovertype == 'rc':
                child = self.crossover(parent1,parent2)
            elif self.crossovertype == 'uc':
                child = self.uniformCrossover(parent1,parent2)
            elif self.crossovertype == 'o1c':
                child = self.order1Crossover(parent1,parent2)
                
            if self.mutationtype == 'rm':
                self.mutation(child)
            elif self.mutationtype == 'sm':
                self.scrambleMutation(child)
            elif self.mutationtype == 'im':
                self.inversionMutation(child)

    def GAStep(self):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """

        self.updateMatingPool()
        self.newGeneration()

    def search(self):
        """
        General search template.
        Iterates for a given number of steps
        """
        self.iteration = 0
        while self.iteration < self.maxIterations:
            self.GAStep()
            self.iteration += 1

        print ("Total iterations: ", self.iteration)
        print ("Best Solution: ", self.best.getFitness())
        
#To save solution in the specified format
def saveSolution(fName, solution, cost):
    file = open(fName, 'w')
    file.write(str(cost)+"\n")
    for city in solution:
        file.write(str(city)+"\n")
    file.close()

'''
The I/O is same as specified in the assignment as LAB1
However a minor modification is made, so that this file
can be imported and used as a module in another file,
and the expected system arguments won't be expected
when imported in another file
'''
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Error - Incorrect input")
        print ("Expecting python BasicTSP.py [instance] ")
        sys.exit(0)

    problem_file = sys.argv[1]
    '''
The below BasicTSP now accepts more arguments for more functionality as mentioned below:
(Use the corresponding strings in the quotes '' to activate that operation, eg 'o1c' in crossover type for order 1 crossover)

_initPop : Initial population type to be selected (random:'random' or nearest neighbour heuristic: 'nn')
_selectiontype :Parent selection type (Random:'rs'  or Binary Tournament Selection:'bts')
_crossovertype : Crossover method (random:'rc,uniform:'uc' or order 1 crossover:'o1c')
_mutationtype : Mutation Method (random:'rm', scramble:'sm' or inversion mutation:'im')

    '''
    ga = BasicTSP(sys.argv[1], 100, 0.05, 500)

    ga.search() 

    saveSolution("solution_"+problem_file, ga.best.genes, ga.best.fitness)