# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:20:01 2020

@author: hp840
"""

from random import random, randint
import numpy as np
from copy import deepcopy
import itertools





class Individual:

    def __init__(self, size, values):
        """
        The individual (with the genotype x) is a list made of indices of the words(permutation).
        The first half of words will be put horizontally, and the rest vertically on a board.
        Values - the board
        """
        self.size = size
        self.values = values
        
        
        lst = []
        for i in range(1, self.size+1):
            lst.append(i)
        perms = list(itertools.permutations(lst))
        all_perms = []
        for perm in perms:
            all_perms.append(list(perm))
        
        self.all_perms = all_perms #a list with all the permutations of size "size"
        
        '''
        values : 2*size vector of permutations 
        '''
    
    def getValues(self):
        return self.values
    
    def setValues(self,v):
        self.values=v
    

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

    
    def mutate(self, probability):
        """
        Performs a mutation on an individual with the given probability.
        Mutate an individual by generating 1 new permutation and put it on a random line
        """
        if random() < probability:
            pos = randint(0, len(self.values)-1)  # generate  0 <= pos <= len(self.values)-1
            lst = []
            for i in range(1, self.size+1):
                lst.append(i)
            kk_perm = np.random.permutation(lst)
            perm=[]
            for i in kk_perm:
                perm.append(i)
                
            self.values[pos]=perm
        return None
   
    
    def crossover(self, parent1,parent2):
        """
        Produces the crossover between parent1 and parent2
        Input : parent1 : values for an Individual
                parent2 : values for an Individual
        Ouput : c : Individual
        """
        new_values = []   

        for i in range(len(parent1)):
            perm1 = parent1[i] #take perm i from parent1
            perm2 = parent2[i]  #take perm i from parent2
            
            #crossover between the 2 permutations - ideea from the lecture :)
            poz1 = np.random.randint(0,self.size//2)
            poz2 = poz1 + self.size//2
            
            perm = [-1] * self.size
            for i in range(poz1 ,poz2):
                perm[i] = perm1[i]
                
            current_index = poz2
            
            for i in range(poz2 ,self.size):
                if perm[i] == -1:
                    while perm2[current_index % self.size] in perm:
                        current_index += 1
                    perm[i] = perm2[current_index % self.size]
                    
            for i in range(poz1):
                if perm[i] == -1:
                    while perm2[current_index % self.size] in perm:
                        current_index += 1
                    perm[i] = perm2[current_index % self.size]
                    
            new_values.append(perm)
                
        c = Individual(self.size, new_values)
        return c
    
    def fct_for_sort(self,indiv):
        return indiv.fitness()
    
    
    def find_best_neighbour(self):
        """
        Returns an indivdual - the best neighbour of the current individual
        
        swaps of 2 elements on each perm from the 2*n permutations
        -> a new neighbour for each 2 elems swapped
        """ 
        list_of_neighbours = []
        
        pos = np.random.randint(0,len(self.values))
        
        for pos in range(len(self.values)): #parsng every perm from the representation (all 2*n permutations)
            for i in range(0, self.size-1):
                for j in range(i+1, self.size):
                    
                    #deepcopy of the current representation
                    new_values=[]
                    for l in self.values:
                        new_values.append(deepcopy(l))
                        
                    #on the perm from psition pos, swap elements from positions i and j
                    new_values[pos][i], new_values[pos][j] = new_values[pos][j], new_values[pos][i]
        
                    #put the new individual in the list of neighbours
                    new_neigh = Individual(self.size,new_values)
    
                    #il adaug doar daca are fitness ul mai mare, ca sa nu fac sortul dupaia degeaba
                    if new_neigh.fitness() > self.fitness():
                        list_of_neighbours.append(new_neigh)
            
        list_of_neighbours.sort(key = self.fct_for_sort, reverse = True)
        
        if len(list_of_neighbours) > 0:
            if list_of_neighbours[0].fitness() > self.fitness():
                return list_of_neighbours[0]
        
        new_values=[]
        for l in self.values:
            new_values.append(deepcopy(l))
        return Individual(self.size,new_values)

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
    
    
    def __eq__(self, otherr):
        if otherr == None:
            return False
        vals = otherr.getValues()
        for i in range(len(self.values)):
            if self.values[i] != vals[i]:
                return False
        return True

    
    


class Population:

    def __init__(self, noIndividuals, indivSize):
        """
        """
        self.noIndividuals = noIndividuals
        self.indivSize = indivSize
        self.v = []  # list of pairs [individual , fitness]
        
        lst = [] #lista pe care vom face permutarile (lista cu elem de la 1 la size)
        for i in range(1, self.indivSize+1):
            lst.append(i)
        
        for i in range(0, noIndividuals):
            values = []
            #generate size*2 random permutations to put them in the list values
            for j in range(0,2*self.indivSize):
                kk_perm = np.random.permutation(lst)
                perm=[]
                for i in kk_perm:
                    perm.append(i)
                values.append(perm)
                
            ind = Individual(indivSize, values)
            
            self.v.append(ind)  # individual
            
        

    def getIndividuals(self):
        return self.v
    
    def iteration(self, probability):
        '''
        an iteration - for EA
        '''
        i1=randint(0,len(self.v)-1)
        i2=randint(0,len(self.v)-1)
        if (i1!=i2):
            c = Individual(self.indivSize,[])
            c = c.crossover(self.v[i1].getValues(),self.v[i2].getValues())
            c.mutate(probability)
            f1=self.v[i1].fitness()
            f2=self.v[i2].fitness()
            fc=c.fitness()
            if(f1<f2) and (f1<fc):
                self.v[i1]=c
            if(f2<f1) and (f2<fc):
                self.v[i2]=c

    

class HillClimbing:
    def __init__(self,n):
        self.n=n

    def generateIndividual(self):
        """
        function that recievesthe number of little squares that are found on the edge of the big square and returns a list of permutations
        randomly generated  
        """
        result = []
        for j in range(2* self.n):
            tup = np.random.permutation(self.n)
            for i in range(len(tup)):
                tup[i] = tup[i]+1
            tup = list(tup)
            result.append(tup)
        result = Individual(self.n,result)  
        return result        
    
    def algorithm(self):
        current_individual = self.generateIndividual()

        maxx = 2*self.n*self.n + self.n*self.n
        #print(current_individual)
        #print(current_individual.fitness())
        current_list = []
        generation = 0
        
        
        #daca ajung sa am lista atat de lunga (am luat 100)
        #inseamna ca se cam invarte pe acolo aiurea, nu mai gaseste alte solutii mai bune
        #deci o pastram pe asta si o returnam :)
        while len(current_list)<100:
            if current_individual.fitness() == maxx:
                return current_individual
             
            current_individual = current_individual.find_best_neighbour()
            #print("------------HILL------------")
            #print('Until now: individ optim \n' + str(current_individual) +" with fitness "+ str(current_individual.fitness())+ "/" + str(maxx)  + "\n")
            
            
            if current_individual in current_list: #uses the __eq__ method
                current_list.append(current_individual)
            else:
                current_list = [current_individual]
            generation+=1
        return current_individual


class Evolutionary:
    def __init__(self,n,dimPopulation,probability, noIterations):
        self.__n = n
        self.__dimPopulation = dimPopulation
        self.__prob = probability
        self.__noIterations = noIterations
        
    def algorithm(self):
        P = Population(self.__dimPopulation, self.__n)
        
        m = 3*self.__n*self.__n #max fitness
        
        for i in range(self.__noIterations):
            P.iteration(self.__prob)
            #print the best individual until now
            graded = [ (x.fitness(), x) for x in P.getIndividuals()]
            graded.sort(key=lambda x: x[0], reverse=True)
            result=graded[0]
            fitnessOptim=result[0]
            individualOptim=result[1]
            #print("------------EA------------")
            #print('Until now: individ optim \n' + str(individualOptim) +" with fitness "+ str(fitnessOptim)+ "/" + str(m)  + "\n")
            if fitnessOptim == m: #max fitness => good solution
                break
    
        #print the best individual
        graded = [ (x.fitness(), x) for x in P.getIndividuals()]
        graded.sort(key=lambda x: x[0], reverse=True)
        result=graded[0]
        fitnessOptim=result[0]
        individualOptim=result[1]
        #print('Final result: individ optim \n' + str(individualOptim) +" with fitness "+ str(fitnessOptim)+ "/" + str(m) + "\n")
        return individualOptim


            
