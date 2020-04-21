# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 19:46:30 2020

@author: Bacotiu-Denisa Cristina - group 921/1
"""
from itertools import permutations
from copy import deepcopy
from random import random, choice

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import statistics




class Ant:
    
    def __init__(self,n):
        self.__size = n
        self.__solution = [[] for i in range(2*n)] #2*n empty lists
        
    
        
        #generate all possible permutations
        lst = []
        for i in range(1, self.__size+1):
            lst.append(i)
        perms = list(permutations(lst))
        all_perms = []
        for perm in perms:
            all_perms.append(list(perm))
        self.__all_perms = all_perms #a list with all the permutations of size "size"
        
        self.__solution[0] = choice(self.__all_perms) #put a random perm on the first position
        
        

        
    def getSolution(self):
        return self.__solution
    
    def setSolution(self, newSol):
        self.__solution = newSol
    
    def isOkUntilNowOnColumns(self, sol):
        """
        input : sol : list of 2*n lists (empty or not) - representation of a possible solution
        output : True/False
        
        checks if there are no repeating elements on the columns of sol
        """
        
        #checks if the list sol - representing a possible solution - is correct until now
        #in other words, if it can lead to a solution
        #for columns -> add for every column the nr of unique elements
        cols = []
        for i in range(0, self.__size):
            c1=[]
            c2=[]
            for j in range(0,self.__size):
                if sol[j]!= []:
                    c1.append(sol[j][i])           #coloanele corespunzatoare primei cifre din pereche
                if sol[j+self.__size] != []:
                    c2.append(sol[j+self.__size][i]) #coloanele corespunzatoare la a doua cifra din pereche
            cols.append(c1)
            cols.append(c2)
        
        #for every col, check if ok
        for col in cols:
            if len(set(col)) != len(col): #un  element se repeta in vreo coloana (completa sau incompleta)
                return False
        
        return True
    
    
    def evaluate(self):
        """
        -- returns the fitness of the solution sol
        i know in every point that on lines and cols everything is ok
        so i have to compute the number of good pairs (non repeating)
        """
        #fac o lista cu toate perechile si vad daca se repeta vreuna (pana acum)
        nr=0
        
        pairs = []
        for i in range(0,self.__size):
            for j in range(0, self.__size):
                if self.__solution[i] != [] and self.__solution[i+self.__size] != [] : #sa am de unde face perechea
                    p=[]
                    p.append(self.__solution[i][j])
                    p.append(self.__solution[i+self.__size][j])
                    pairs.append(p)
        for p in pairs:
            if pairs.count(p) == 1:
                nr += 1

        return self.__size*self.__size - nr + 1 # pun acel +1 ca sa nu fie 0 niciodata -> ca sa nu am probleme la impartire
                                                # la 0 mai incolo
        #return nr
    
    def getFirstEmptyList(self):
        """
        Returns : -1 if the sol is complete
                    i: int - the index of the first empty sublist from self.__solution
        """
        for i in range(0, len(self.__solution)):
            if self.__solution[i] == []:
                return i
        return -1
        
    
    def nextMoves(self, sol):
        #returneaza o lista de posibile permutari corecte de adaugat la solutia curenta - sol
        perms = []
        for perm in self.__all_perms:
            new_sol = deepcopy( sol)
            pos = self.getFirstEmptyList()
            if pos==-1:
                return None
            new_sol[pos] = perm
            if self.isOkUntilNowOnColumns(new_sol) == True:
                perms.append(perm)
        return perms
    
    def distMove(self, perm):
        #if we put perm on the first empty pos, calculate the empirical distance for that solution
        new_sol = deepcopy(self.__solution)
        pos = self.getFirstEmptyList()
        if pos==-1:
            return None
        new_sol[pos] = perm
        return (len(self.__all_perms)-len(self.nextMoves(new_sol)))
    
    def update(self, q0, trace, alpha, beta):
        """
        updates the solution of this ant
        adds a new perm in the ant's solution
        
        returns : True - if the solution was successfully updated
                  None - if the sol cannot be updated (no next moves)
                  False - if the sol is already complete
        """
        # adauga o noua permutare in solutia furnicii daca este posibil
        p = []

        nextSteps = deepcopy(self.nextMoves(self.__solution))
        
        if nextSteps == None:
            return None
        
        # determina urmatoarele pozitii valide in nextSteps
        # daca nu avem astfel de pozitii iesim 
        if (len(nextSteps) == 0):
            return False
        
        p = [0 for i in range(len(nextSteps))]
        
        # punem pe pozitiile valide valoarea distantei empirice
        for i in range(len(nextSteps)):
            p[i] = self.distMove(nextSteps[i]) #nextSteps[i] -> permutation
            
        p=[ (p[i]**beta)*(trace[(tuple(self.__solution[self.getFirstEmptyList()-1]),tuple(nextSteps[i]))]**alpha) for i in range(len(p))]
        #pentru fiecare perm din nextSteps (adica pt fiecare vecin), calculam produsul trace^alpha si vizibilitate^beta
        #-> trace de ultima permutare din solutie si cei p vecini
        

        if (random()<q0):
            # adaugam cea mai buna dintre mutarile posibile
            p = [ [i, p[i]] for i in range(len(p)) ]
            p = max(p, key=lambda a: a[1])
            #put perm nextSteps[i] on the first empty sublist of the current solution
            pos = self.getFirstEmptyList()
            self.__solution[pos] = nextSteps[i]
        else:
            # adaugam cu o probabilitate un drum posibil (ruleta)
            pos = self.getFirstEmptyList()
            self.__solution[pos] = choice(nextSteps) #choose a random one :)

        return True
    
    
    def __str__(self):
        res=""
        for i in range(0,self.__size):
            line=[]
            for j in range(0, self.__size):
                p=[]
                if self.__solution[i] == []: #if we do not have elements on that perm, put an empty space :)
                    p.append("")
                else:
                    p.append(self.__solution[i][j])
                
                if self.__solution[i+self.__size] == []:
                    p.append("")
                else:
                    p.append(self.__solution[i+self.__size][j])
                line.append(p)
            res+=str(line)+"\n"
        return res



class Controller:
    def __init__(self,noAnts, n, noEpoch, problem):
        self.__population = []
        self.__noAnts = noAnts
        self.__n = n
        self.__problem = problem
        
        
        lst = []
        for i in range(1, self.__n+1):
            lst.append(i)
        perms = list(permutations(lst))
        all_perms = []
        for perm in perms:
            all_perms.append(tuple(perm)) #a list with all possible permutations as tuples
            
        self.__trace = {} #a dictionary - like a graph - each vertice is  a permutation
                    #we have edges between all the permutations (a complete graph, where the ants will walk)
                    #the value on the edge is the trace oof pheromons that the ants leave
                    #initially, this value is 0
                    #repr : key - tuple of 2 tuples (because in python dict i can use only tuples, not lists:(  )
                    #       value - number (float)
        
        for i in all_perms:
            for j in all_perms:
                self.__trace[(i,j)] = 0
        
        self.__noEpoch = noEpoch
    
    def iteration(self, alpha, beta, q0, rho):
        
        self.__population = [Ant(self.__n) for i in range(self.__noAnts)]
    
        for i in range(2*self.__n):
            # numarul maxim de iteratii intr-o epoca este lungimea solutiei
            for x in self.__population:
                res = x.update(q0, self.__trace, alpha, beta)
                if res == False: #the board is full -> we have solution
                    return x
            
        # actualizam trace-ul cu feromonii lasati de toate furnicile
        dTrace=[ 1.0 / self.__population[i].evaluate() for i in range(len(self.__population))]
    
        
        #se evaporeaza feromonii
        for key in self.__trace:
            self.__trace[key] = (1 - rho) * self.__trace[key]
    
            
        for i in range(len(self.__population)): #parcurgem furnicile
            for j in range(len(self.__population[i].getSolution())-1): #parcurgem fiecare permutare din fiecare furnica
                perm1 = self.__population[i].getSolution()[j]   #perm1 
                perm2 = self.__population[i].getSolution()[j+1] #perm2 - luam permutarile cate 2, in ordine
                if perm1 != [] and perm2!=[]:
                    self.__trace[(tuple(perm1),tuple(perm2))] = self.__trace[(tuple(perm1),tuple(perm2))] + dTrace[i] #update the trace between perm1 and perm2
            
        # return best ant
        f=[ [self.__population[i].evaluate(), i] for i in range(len(self.__population))]
        f=min(f)
        return self.__population[f[1]]
    
    def runAlg(self):
        alpha = self.__problem.getAlpha()
        beta = self.__problem.getBeta()
        q0 = self.__problem.getQ0()
        rho = self.__problem.getRho()
        
        bestSol= Ant(self.__n)
        
        print("Programul ruleaza! Dureaza ceva timp pana va termina!")
        for i in range(self.__noEpoch):
            antSol = self.iteration(alpha, beta, q0, rho)
            if antSol.evaluate() < bestSol.evaluate():
                bestSol.setSolution ( deepcopy(antSol.getSolution()) )
            if bestSol.evaluate() == 1 :
                print("**************FINAL SOLUTION*****************")
                print(bestSol)
                print("fitness: ", bestSol.evaluate(), " --> (best is 1, worst is ", self.__n*self.__n+1 , ")")
                print("<3 found perfect solution <3")
                return bestSol
            print("-------------------------------------")
            print("epoca nr: ",i)
            print("sol epoca curenta: ")
            print("fitness: ", antSol.evaluate(),  " --> (best is 1, worst is ", self.__n*self.__n+1 , ")")
            print(antSol)
            print("best sol util now:")
            print("fitness: ", bestSol.evaluate(),  " --> (best is 1, worst is ", self.__n*self.__n+1 , ")")
            print(bestSol)
            
        print ("gata")
        return bestSol
    
    def runAlg_noPrints(self):
        """
        same fct as before, but with no prints - used for statistics only
        """
        alpha = self.__problem.getAlpha()
        beta = self.__problem.getBeta()
        q0 = self.__problem.getQ0()
        rho = self.__problem.getRho()
        
        bestSol= Ant(self.__n)
        
        for i in range(self.__noEpoch):
            antSol = self.iteration(alpha, beta, q0, rho)
            if antSol.evaluate() < bestSol.evaluate():
                bestSol.setSolution ( deepcopy(antSol.getSolution()) )
            if bestSol.evaluate() == 1 :
                return bestSol

        return bestSol
        

class Statistics:
    def __init__(self):
        self.fitnesses = []
        
    def statistics_fct(self,x_coords, y_coords, index, n):
        x_coords.append(index)
        
        problem = Problem("specific_params.txt")
        #for 3 ants and 30 epoch
        ctrl = Controller(3,n,40,problem)
        
        indivFinal = ctrl.runAlg_noPrints()
                
        y_coords.append(indivFinal.evaluate())
        
        self.fitnesses.append(indivFinal.evaluate())
        
        plt.cla()
        plt.plot(x_coords, y_coords)
        plt.show()
        
        
    def statistics(self,n):
        x_coords = []
        y_coords = []
        
        index = 0
        
        for i in range(0,30):
            index = index + 1
            print(" --> best is 1, worst is ", n*n+1)
            FuncAnimation(plt.gcf(), self.statistics_fct(x_coords, y_coords, index, n), interval = 100)
        plt.tight_layout()
        
        #sum of all fitnesses
        fitSum = 0
        for fit in self.fitnesses:
            fitSum = fitSum + fit    
            
        print(" --> best is 1, worst is ", n*n+1)
            
        print("Stastics:")

        avg = fitSum / len(self.fitnesses)
        print ("Average: ", avg)
        
        dev = statistics.stdev(self.fitnesses)
        print ("Standard deviation: ", dev)
            

class Problem:
    """
    Reads from file the specific params for ACO
    in this order, each on a line : alpha, beta, q0, rho
    """
    def __init__(self, filename):
        self.__alpha= 1.9
        self.__beta = 0.9
        self.__rho = 0.05
        self.__q0 = 0.5     #default values
        self.__filename = filename
        self.loadProblem()
    
    def loadProblem(self):
        f = open(self.__filename, 'r')
        self.__alpha = float(f.readline())
        self.__beta = float(f.readline())
        self.__q0 = float(f.readline())
        self.__rho = float(f.readline())
    
    def getAlpha(self):
        return self.__alpha
    
    def getBeta(self):
        return self.__beta
    
    def getRho(self):
        return self.__rho
    
    def getQ0(self):
        return self.__q0
    
    
class UI:
        
    def start(self):
        """
        !!!!!!!!!!!!!! in the file "specific_params.txt" !!!!!!!!!!!!!
        the specific parameters are : alpha = 1.9,beta = 0.9,rho = 0.05,q0 = 0.5
        """
        print("Commands:")
        print("1 - Default run: n=4, noEpoch=100 and noAnts=3")
        print("2 - You choose these parameters :)")
        print("3 - Statistics")
        cmd = input("Enter command: ")
        if cmd == "2":
            n = int(input("Give n:"))
            noEpoch = int(input("Give nr epoch:"))
            noAnts = int(input("Give nr ants:"))
            problem = Problem("specific_params.txt")
            ctrl = Controller(noAnts,n,noEpoch,problem)
            ctrl.runAlg()
            
        if cmd=="1":
            problem = Problem("specific_params.txt")
            ctrl = Controller(3,4,100,problem)
            ctrl.runAlg()
        
        if cmd == "3":
            s = Statistics()
            s.statistics(4)

ui = UI()
ui.start()




        