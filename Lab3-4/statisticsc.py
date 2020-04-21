# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:37:21 2020

@author: hp840
"""


from hill import *
from pso import *


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import statistics

class Statistics:
    
    def __init__(self):
        self.psoFitnesses = []
        self.eaFitnesses = []
        self.hillFitnesses = []
        
        
    
    
    def pso_fct(self, x_coords, y_coords, index, n):
        x_coords.append(index)

        pop = 40
        noIter = 10
        
        # max fitness
        m = 3*n*n

        # specific parameters for PSO
        w = 1.0
        c1 = 1.
        c2 = 2.5
        neighSize = 20
        
        pop = ParticlePopulation(pop, n)
        pso = PSO(pop, noIter)

        indivFinal = pso.algorithm(w, c1, c2, neighSize)
                
        
        y_coords.append(indivFinal.fitness())
        
        self.psoFitnesses.append(indivFinal.fitness())
        
        plt.cla()
        plt.plot(x_coords, y_coords)
        plt.show()
            
        
    def statisticsPSO(self, n):
        x_coords = []
        y_coords = []
        
        index = 0        
        for i in range(0,30):
            index = index + 1 #coord x
            FuncAnimation(plt.gcf(), self.pso_fct(x_coords, y_coords, index, n), interval = 100)
        plt.tight_layout()
        
        #sum of all fitnesses
        fitSum = 0
        for fit in self.psoFitnesses:
            fitSum = fitSum + fit    
            
        print("PSO Stastics:")

        avg = fitSum / len(self.psoFitnesses)
        print ("Average: ", avg)
        
        dev = statistics.stdev(self.psoFitnesses)
        print ("Standard deviation: ", dev)
        
    def ea_fct(self,x_coords, y_coords, index, n):
        x_coords.append(index)
        
        pop = 100
        prob = 0.01
        noIter = 1000 #1000 iterations
        
        ev = Evolutionary(n,pop,prob,noIter)
        indivFinal = ev.algorithm()
                
        y_coords.append(indivFinal.fitness())
        
        self.eaFitnesses.append(indivFinal.fitness())
        
        plt.cla()
        plt.plot(x_coords, y_coords)
        plt.show()
        
        
    def statisticsEA(self,n):
        x_coords = []
        y_coords = []
        
        index = 0
        
        for i in range(0,30):
            index = index + 1
            FuncAnimation(plt.gcf(), self.ea_fct(x_coords, y_coords, index, n), interval = 100)
        plt.tight_layout()
        
        #sum of all fitnesses
        fitSum = 0
        for fit in self.eaFitnesses:
            fitSum = fitSum + fit      
            
        print("EA Stastics:")

        avg = fitSum / len(self.eaFitnesses)
        print ("Average: ", avg)
        
        dev = statistics.stdev(self.eaFitnesses)
        print ("Standard deviation: ", dev)
        
        
    def hill_fct(self,x_coords, y_coords, index, n):
        x_coords.append(index)
        
        hill = HillClimbing(n)
        indivFinal = hill.algorithm()
                
        y_coords.append(indivFinal.fitness())
        
        self.hillFitnesses.append(indivFinal.fitness())
        
        plt.cla()
        plt.plot(x_coords, y_coords)
        plt.show()
        
        
    def statisticsHill(self,n):
        x_coords = []
        y_coords = []
        
        index = 0
        
        for i in range(0,30):
            index = index + 1
            FuncAnimation(plt.gcf(), self.hill_fct(x_coords, y_coords, index, n), interval = 100)
        plt.tight_layout()
        
        #sum of all fitnesses
        fitSum = 0
        for fit in self.hillFitnesses:
            fitSum = fitSum + fit      
            
        print("EA Stastics:")

        avg = fitSum / len(self.hillFitnesses)
        print ("Average: ", avg)
        
        dev = statistics.stdev(self.hillFitnesses)
        print ("Standard deviation: ", dev)
        


class UI:
    
    def main(self):
        
        s = Statistics()
        
        print("1.statistics pso")
        print("2.statistics ea")
        print("3.statistics hill")
        cmd = input("Enter your command:")
        if cmd == "1":
            s.statisticsPSO(4)
        if cmd == "2":
            s.statisticsEA(4)
        if cmd == "3":
            s.statisticsHill(4)


ui = UI()
ui.main()

