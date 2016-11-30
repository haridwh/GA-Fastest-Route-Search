import math
import random

node = ['S','A','B','C','D','E','F','G']
edge = [
    [0, 0.1, 0.233, 0.167,  0,      0,      0,      0   ],
    [0, 0,   0.1,   0,      0.4,    0,      0,      0   ],
    [0, 0.1, 0,     0.067,  0,      0.25,   0,      0   ],
    [0, 0,   0.067, 0,      0,      0,      0.3,    0   ],
    [0, 0,   0,     0,      0,      0.067,  0,      0.15],
    [0, 0,   0,     0,      0.067,  0,      0.067,  0.15],
    [0, 0,   0,     0,      0,      0.067,  0,      0.15],
    [0, 0,   0,     0,      0,      0,      0,      0   ],
]

def _initPopulation(individu):
    population = [];
    for i in range(individu):
        chromosome = []
        chromosome.append(0)
        currentNode = 0
        nextNode = random.randint(1,7)
        while (len(chromosome)<8):
            if (7 in chromosome):
                while (nextNode in chromosome):
                    nextNode = random.randint(1,7)
            else:
                while ((nextNode in chromosome) or (edge[currentNode][nextNode] == 0)):
                    nextNode = random.randint(1,7)
            chromosome.append(nextNode)
            currentNode = nextNode
        population.append(chromosome)
    return population

def getFitness(chromosome):
    fitness = 0
    i = 0
    while chromosome[i] != 7:
        if edge[chromosome[i]][chromosome[i+1]] == 0:
            return 0
        fitness += edge[chromosome[i]][chromosome[i+1]]
        i += 1
    return 1/fitness

def getProbability(population):
    listFitness = []
    fitnessProbability = []
    sumFitness = 0
    probability = 0
    for i in range(len(population)):
        fitness = getFitness(population[i])
        listFitness.append(fitness)
        sumFitness += fitness
    for i in range(len(listFitness)):
        probability += listFitness[i]/sumFitness
        fitnessProbability.append(probability)
    return fitnessProbability

def getParent(population):
    parent = []
    pin = random.uniform(0,1)
    probability = getProbability(population)
    for i in range(2):
        find = False
        i = 0
        while not find:
            if pin<probability[i]:
                if not population[i] in parent:
                    parent.append(population[i])
                    find = True
                else:
                    pin = random.uniform(0,1)
                    i = 0
            i+=1
    return parent

def crossOver(parent):
    for i in range(8):
        cross = random.randint(0,1)
        if cross==1:
            parent[0][i], parent[1][i] = parent[1][i],parent[0][i]
    return parent;

def getBestPopulation(individu, population):
    for i in range( individu*2):
        for j in range(individu*2):
            if getFitness(population[j]) < getFitness(population[i]):
                population[j],population[i]=population[i],population[j]
    return population[:individu]

def getNewPopulation(individu, generasi):
    newPopulation = _initPopulation(individu)
    for i in range(generasi):
        population = []
        for j in range(individu):
            population.append(newPopulation[j])
        for j in range(individu/2):
            child = crossOver(getParent(newPopulation))
            for k in range(2):
                population.append(child[k])
        newPopulation = getBestPopulation(individu, population)
    return newPopulation

def main(individu, generasi):
    population = getNewPopulation(individu, generasi)
    rute = []
    waktu = 0
    k = 0
    for i in range( individu):
        for j in range(i+1, individu):
            if getFitness(population[j]) < getFitness(population[i]):
                population[j],population[i]=population[i],population[j]
    if getFitness(population[0]) != 0:
        while population[0][k] != 7:
            waktu+= edge[population[0][k]][population[0][k+1]]
            k+=1
    print "Route : ",population[0], ", Fitness : ", getFitness(population[0]), ", Waktu : ", waktu*60, " menit"

main(50,1)
