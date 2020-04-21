# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 19:42:44 2020

@author: hp840
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:41:48 2020

@author: hp840
"""

import sys
from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel,QLineEdit, QTextEdit
from qtpy.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


from random import random, randint
import numpy as np
from copy import deepcopy

from hill import *
from pso import *

from qtpy.QtCore import Signal

from qtpy.QtCore import QThread


class MyThread(QThread):
    sign = Signal()
    def __init__(self):
        QThread.__init__(self)
        self.result = None
        self.func = None
        
    def set_func(self, func):
        self.func = func
        
    def run(self):
        result = self.func()
        self.result = result


class Example(QWidget):
    
    eaSignal = Signal()
    hillSignal = Signal()
    psoSignal = Signal()
    
    def __init__(self):
        super().__init__()
        self.qbtn1 = QPushButton('Run EA', self)
        self.qbtn2 = QPushButton('Run HILL CLIMB', self)
        self.qbtn3 = QPushButton('Run PSO', self)
        
        
        self.thread1 = MyThread()
        self.thread2 = MyThread()
        self.thread3 = MyThread()
        
        self.eaSignal.connect(self.showEaResult)
        self.hillSignal.connect(self.showHillResult)
        self.psoSignal.connect(self.showPsoResult)
        
        
        self.stringResEa = ""
        self.stringResHill = ""
        self.stringResPso = ""
       
        
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QVBoxLayout()
        
        #layout 2 - ea
        easizeLayout = QHBoxLayout()
        easizeLabel = QLabel()
        easizeLabel.setText("Size: ")
        self.easizeEdit = QLineEdit()
        easizeLayout.addWidget(easizeLabel)
        easizeLayout.addWidget(self.easizeEdit)
        layout2.addLayout(easizeLayout)
        
        popLayout = QHBoxLayout()
        popLabel = QLabel()
        popLabel.setText("Population dim.: ")
        self.popEdit = QLineEdit()
        popLayout.addWidget(popLabel)
        popLayout.addWidget(self.popEdit)
        layout2.addLayout(popLayout)
        
        probLayout = QHBoxLayout()
        probLabel = QLabel()
        probLabel.setText("Prob. of mutation: ")
        self.probEdit = QLineEdit()
        probLayout.addWidget(probLabel)
        probLayout.addWidget(self.probEdit)
        layout2.addLayout(probLayout)
        
        iterLayout = QHBoxLayout()
        iterLabel = QLabel()
        iterLabel.setText("No. iterations: ")
        self.iterEdit = QLineEdit()
        iterLayout.addWidget(iterLabel)
        iterLayout.addWidget(self.iterEdit)
        layout2.addLayout(iterLayout)
        
        layout2.addWidget(self.qbtn1)

        self.eaResult = QTextEdit()
        layout2.addWidget(self.eaResult)
        
        
        #layout 3 - hill
        sizeLayout = QHBoxLayout()
        sizeLabel = QLabel()
        sizeLabel.setText("Size: ")
        self.sizeEdit = QLineEdit()
        sizeLayout.addWidget(sizeLabel)
        sizeLayout.addWidget(self.sizeEdit)
        layout3.addLayout(sizeLayout)
        layout3.addWidget(self.qbtn2)
        
        self.hillResult = QTextEdit()
        layout3.addWidget(self.hillResult)
        
        
        #layout 4 - pso
        psosizeLayout = QHBoxLayout()
        psosizeLabel = QLabel()
        psosizeLabel.setText("Size: ")
        self.psosizeEdit = QLineEdit()
        psosizeLayout.addWidget(psosizeLabel)
        psosizeLayout.addWidget(self.psosizeEdit)
        layout4.addLayout(psosizeLayout)
        
        psopopLayout = QHBoxLayout()
        psopopLabel = QLabel()
        psopopLabel.setText("Population dim.: ")
        self.psopopEdit = QLineEdit()
        psopopLayout.addWidget(psopopLabel)
        psopopLayout.addWidget(self.psopopEdit)
        layout4.addLayout(psopopLayout)
        
        psoiterLayout = QHBoxLayout()
        psoiterLabel = QLabel()
        psoiterLabel.setText("No. iterations: ")
        self.psoiterEdit = QLineEdit()
        psoiterLayout.addWidget(psoiterLabel)
        psoiterLayout.addWidget(self.psoiterEdit)
        layout4.addLayout(psoiterLayout)
        
        layout4.addWidget(self.qbtn3)
        
        self.psoResult = QTextEdit()
        layout4.addWidget(self.psoResult)
        
        
        
        layout1.addLayout(layout2)
        layout1.addLayout(layout3)
        layout1.addLayout(layout4)
        
        self.runButton = QPushButton('Run all -> with threads', self)
        self.stopButton = QPushButton('Stop',self)
        
        layout1.addWidget(self.runButton)
        layout1.addWidget(self.stopButton)

        
        self.setLayout(layout1) 
        
        self.initUI()
        
        

        
        
    def initUI(self):
        
        
        self.qbtn1.clicked.connect(self.on_click1)
        
        self.qbtn2.clicked.connect(self.on_click2)
        
        self.qbtn3.clicked.connect(self.on_click3)
        
        self.runButton.clicked.connect(self.runAll)
        
        self.stopButton.clicked.connect(self.stopButtonClicked)
        
        self.setWindowTitle('Hello! :)')
        self.setWindowIcon(QIcon('web.png'))        
    
        self.show()
    
    @pyqtSlot()
    def stopButtonClicked(self):
        raise SystemExit(0)
    
    @pyqtSlot()
    def on_click1(self):
        self.eaResult.clear()
        
        n = int(self.easizeEdit.text())
        pop = int(self.popEdit.text())
        prob = float(self.probEdit.text())
        noIter = int(self.iterEdit.text())
        
        ev = Evolutionary(n,pop,prob,noIter)
        indivFinal = ev.algorithm()
        
        m = 3*n*n #max fitness
        
        strr = 'Final result: individ optim \n' + str(indivFinal) +"fitness: "+ str(indivFinal.fitness())+ "/" + str(m) + "\n"
        self.eaResult.setText(strr)
        
    @pyqtSlot()
    def on_click2(self):
        n = int(self.sizeEdit.text())
        hill = HillClimbing(n)
        sol = hill.algorithm()
        strr = ""
        strr += "FINAL result:\n"
        strr += str(sol)
        strr += "fitness: " + str(sol.fitness()) + "/" + str(3*n*n)
        
        self.hillResult.setText(strr)
        
        
    @pyqtSlot()
    def on_click3(self):
        
        n = int(self.psosizeEdit.text())
        pop = int(self.psopopEdit.text())
        noIter = int(self.psoiterEdit.text())
        
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
        
        strr = 'Final result: individ optim \n' + str(indivFinal) +"fitness: "+ str(indivFinal.fitness())+ "/" + str(m) + "\n"
        
        
        self.psoResult.setText(strr)
    
    
    def runEa(self):
        n = int(self.easizeEdit.text())
        pop = int(self.popEdit.text())
        prob = float(self.probEdit.text())
        noIter = int(self.iterEdit.text())
        
        ev = Evolutionary(n,pop,prob,noIter)
        indivFinal = ev.algorithm()
        
        m = 3*n*n #max fitness
        
        strr = 'Final result: individ optim \n' + str(indivFinal) +"fitness: "+ str(indivFinal.fitness())+ "/" + str(m) + "\n"
        
        self.stringResEa = strr
    
        self.eaSignal.emit()
        
        
    def runHill(self):
        n = int(self.sizeEdit.text())
        hill = HillClimbing(n)
        sol = hill.algorithm()
        strr = ""
        strr += "FINAL result:\n"
        strr += str(sol)
        strr += "fitness: " + str(sol.fitness()) + "/" + str(3*n*n)
        self.stringResHill = strr
        
        self.hillSignal.emit()
        
    def runPso(self):
        n = int(self.psosizeEdit.text())
        pop = int(self.psopopEdit.text())
        noIter = int(self.psoiterEdit.text())
        
        # max fitness
        m = 3*n*n

        # specific parameters for PSO
        w = 1.0
        c1 = 1.
        c2 = 2.5
        neighSize = 20
        
        particlePop = ParticlePopulation(pop, n)
        pso = PSO(particlePop, noIter)

        indivFinal = pso.algorithm(w, c1, c2, neighSize)
        strr = 'Final result: individ optim \n' + str(indivFinal) +"fitness: "+ str(indivFinal.fitness())+ "/" + str(m) + "\n"
        
        self.stringResPso = strr
        
        self.psoSignal.emit()
        
        
    def showEaResult(self):
        self.eaResult.setText(self.stringResEa)
        self.update()
    
    def showHillResult(self):
        self.hillResult.setText(self.stringResHill)
        self.update()
        
    def showPsoResult(self):
        self.psoResult.setText(self.stringResPso)
        self.update()
        
        
    @pyqtSlot()
    def runAll(self):
        self.thread1.set_func(self.runEa)
        self.thread2.set_func(self.runHill)
        self.thread3.set_func(self.runPso)
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        
        
        
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())