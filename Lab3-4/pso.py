# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 22:45:20 2020

@author: hp840
"""



from itertools import permutations
from random import randint, random,randrange
from time import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import statistics
from copy import deepcopy



class Particle:

    def __init__(self,n):

        self.size = n
        
        lst = [] #lista pe care vom face permutarile (lista cu elem de la 1 la size)
        for i in range(1, self.size +1):
            lst.append(i)
        
        values = []
        #generate size*2 random permutations to put them in the list values
        for j in range(0,2*self.size):
            kk_perm = np.random.permutation(lst)
            perm=[]
            for i in kk_perm:
                perm.append(i)
            values.append(perm)
        self.values = values
    
        listPos = []
        for i in range(self.size):
            listPos.append(i)

        self._pozition = listPos
        self.velocity = [0 for i in range(self.size)]
        
        # the memory of that particle
        self._bestPozition = self._pozition


    def __str__(self):
        res=""
        for i in range(0,self.size):
            line=[]
            for j in range(0, self.size):
                p=[]
                p.append(self.values[i][j])
                p.append(self.values[i+self.size][j])
                line.append(p)
            res+=str(line)+"\n"
        return res

    def getVelocity(self):
        return self.velocity

    def getVelocityFromIndex(self, pos):
        return self.velocity[pos]

    def setVelocityAtIndex(self, pos, newVelocity):
        self.velocity[pos] = newVelocity

    def getPosition(self):
        return self._pozition
    
    def setPosition(self, newPosition):
        self._pozition = newPosition

    def getPositionFromIndex(self, pos):
        return self._pozition[pos]

    def setPositionAtIndex(self, pos, newPosition):
        self._pozition[pos] = newPosition

    def getBestPosition(self):
        return self._bestPozition

    def getBestPositionFromIndex(self, pos):
        return self._bestPozition[pos]

    def fitness(self):    
        '''
        returns an int : how many cols are ok:add the nr of different elements on every column (max 2*size*size)
                            and how many pairs are ok (<=> different from each other)(max size*size)
                        i know the lines are ok because i put them as permutations from the begining
        
        on cols : keep the nr of different elements on columns : max from this part : size * ( 2 * size ) 
        
        so, the maximum fitness is : 2*size*size + size*size -> this means if fitness is max, we have solution
        '''
        nr=0
        
        #for columns -> add for every column the nr of unique elements
        cols = []
        for i in range(0, self.size):
            c1=[]
            c2=[]
            for j in range(0,self.size):
                c1.append(self.values[j][i])           #coloanele corespunzatoare primei cifre din pereche
                c2.append(self.values[j+self.size][i]) #coloanele corespunzatoare la a doua cifra din pereche
            cols.append(c1)
            cols.append(c2)
        
        #for every col, add the nr of diff elems -> get this nr by making a set from every col
        for col in cols:
            nr += len(set(col))
                
        #how many pairs are ok (ne se repeta perechile)
        #fac o lista cu toate perechile si adaug la suma cate sunt unice
        pairs = []
        for i in range(0,self.size):
            for j in range(0, self.size):
                p=[]
                p.append(self.values[i][j])
                p.append(self.values[i+self.size][j])
                pairs.append(p)
        for p in pairs:
            if pairs.count(p) == 1:
                nr += 1

        return nr


class ParticlePopulation:
    """
    Create a population of particles

    dimPopulation: the number of particles in the population
    n : size of the "board"
    """

    def __init__(self, dimPopulation,n):
        self.__population = [Particle(n) for x in range(dimPopulation)]
        self.__dimPopulation = dimPopulation
        self.__n = n

    def getPopulation(self):
        return self.__population
    
    def getN(self):
        return self.__n
    
    def selectNeighbors(self, noNeigh):
        """  the selection of the neighbours for each particle

        input --
           noNeigh: int - the number of neighbours of a particle

        output--
           neighbors: list of neighbours for each particle
        """

        if noNeigh > len(self.__population):
            noNeigh = len(self.__population)

        neighbors = []
        for i in range(len(self.__population)):
            localNeighbor = []
            for j in range(noNeigh):
                index = randint(0, len(self.__population) - 1)
                x = self.__population[index]
                while x in localNeighbor:
                    index = randint(0, len(self.__population) - 1)
                    x = self.__population[index]
                localNeighbor.append(x)
            neighbors.append(deepcopy(localNeighbor))
        return neighbors


    def iteration(self, neighbors, c1, c2, w):
        """
        an iteration

        for each particle we update the velocity and the position
        according to the particle's memory and the best neighbor's pozition
        """
        
        # determine the best neighbor for each particle
        bn=[]
        for i in range(len(self.__population)):
            bestNeighbor = neighbors[i][0]
            for j in range(1, len(neighbors[i])):
                bnFitness = bestNeighbor.fitness()
                nFitness = neighbors[i][j].fitness()
                if bnFitness > nFitness:
                    bestNeighbor = neighbors[i][j]
            bn.append(bestNeighbor) #append the best neighbor for particle from position i

        # update the velocity for each particle
        for i in range(len(self.__population)):
            for j in range(len(self.__population[0].getVelocity())):
                newVelocity = w * self.__population[i].getVelocityFromIndex(j)
                newVelocity = newVelocity + c1 * random() * (bn[i].getPositionFromIndex(j) - self.__population[i].getPositionFromIndex(j))
                newVelocity = newVelocity + c2 * random() * (self.__population[i].getBestPositionFromIndex(j) - self.__population[i].getPositionFromIndex(j))
                self.__population[i].setVelocityAtIndex(j, newVelocity)

        # update the position for each particle
        for i in range(len(self.__population)):
            newPosition = [] #the new position for the current particle
            for j in range(len(self.__population[0].getVelocity())):
                newPosition.append(self.__population[i].getPositionFromIndex(j) + self.__population[i].getVelocityFromIndex(j))
            #set the new position to the current particle
            self.__population[i].setPosition(newPosition)

        return self.__population


class PSO:
    def __init__(self, population, noIterations):
        self.__population = population
        self.__noIterations = noIterations

    def algorithm(self, w, c1, c2, neighSize):
        # we establish the particles' neighbors
        neighborhoods = self.__population.selectNeighbors(neighSize)

        for i in range(self.__noIterations):
            self.__population.iteration(neighborhoods, c1, c2, w/(i + 1))

        # get the best individual
        best = 0
        for i in range(1, len(self.__population.getPopulation())):
            if self.__population.getPopulation()[i].fitness() > self.__population.getPopulation()[best].fitness():
                best = i
        individualOptim=self.__population.getPopulation()[best]

        return individualOptim

