# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import numpy

def b():
    nr = int(input("give nr of numbers:"))
    print("1. normal distribution \n2.uniform \n3.geometric \n4.poisson")
    cmd = input("give cmd:")
    if cmd == "1":
        x = numpy.random.normal(5,0.1,size=nr) #mean and standard deviation
    if cmd == "2":
        x = numpy.random.uniform(0,10,size=nr)
    if cmd == "3":
        x = numpy.random.geometric(0.35,size=nr) 
    if cmd == "4":
        x = numpy.random.poisson(1,size=nr) 
        
    print(x)
    plt.plot(x,'ro')
    plt.ylabel("some random numbers")
    plt.axis([0,10,0,20])
    plt.show()
        
b()

    
    