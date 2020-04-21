# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 18:50:24 2020

@author: hp840
"""

import copy

class State:
    '''
    n - dim of the board
    empty space : 0
    occuppied space : 1
    repr: a board nxn -  bidim matrix
    
    '''
    
    def __init__(self, n):
        self.__n = n
        self.__values = []
        for i in range(0,n):
            l=[]
            for j in range(0,n):
                l.append(0)
            self.__values.append(l)
            
    
    def findFirstEmptyLine(self):
        '''
        find first line containing only zeros
        output: the index of the line 
                or None if all lines contain 1's (the board is completed)
        '''
        for i in range(0,len(self.__values)):
            if self.__values[i].count(1) == 0:
                return i
        return None
            
    
    def isSolution(self):                
        '''
        if the board is ok until now (checks all the required conditions) + is full => is solution
        '''
        if self.isOkUntilNow() == True and self.findFirstEmptyLine() == None:
            return True
        
        return False
    
    
    
    def isOkUntilNow(self):
        '''
        checks if the current state can lead to a solution
        returns - false if this state can  not lead to a solution
                - true if this state is ok until now
        '''
        #1. only 0 and 1
        for l in self.__values:
            for i in l:
                if i not in [0,1]:
                    return False
        
        #2. sum 1 or 0 on lines
        for l in self.__values:
            sum = 0
            for i in l:
                sum += i
            if sum not in [0,1]:
                return False
        
        #3. sum 1 or 0 on columns
        for c in range(0, self.__n):
            sum = 0
            for l in range(0,self.__n):
                sum += self.__values[l][c]
            if sum not in [0,1]:
                return False
        
        #4. the long condition :)))
        for i1 in range(0,self.__n):
            for j1 in range(0,self.__n):
                if self.__values[i1][j1] == 1:
                    for i2 in range(0,self.__n):
                        for j2 in range(0, self.__n):
                            if self.__values[i2][j2] == 1 and abs(i1-i2)-abs(j1-j2)==0 and (i1!=i2 or j1!=j2):
                                return False
        
        return True
        
        
        
    
    def getValues(self):
        return self.__values
    
    def setValues(self, new_board):
        self.__values = new_board
        
    def getN(self):
        return self.__n
    
    def setN(self, new_n):
        self.__n = new_n
        
    def __str__(self):  
        res=""
        for l in self.__values:
            res+=str(l)
            res+="\n"
        return res
        


class Problem:
    def __init__(self, n):
        self.__initialState = State(n)
        self.__finalState = State(n)
        self.__n = n

    def getN(self):
        return self.__n

    def getInitialState(self):
        return self.__initialState

    def getFinalState(self):
        return self.__finalState

    def setFinalState(self, state):
        self.__finalState = state
        
    def expand(self, state):
        '''
        generate children states for a given state
        input: state - State
        output: list of states
        '''
        firstEmptyLine = state.findFirstEmptyLine()
        if firstEmptyLine is None:  # board is completed
            return []
        
        
        # create children for the currentState
        # put 1 on every position (column) from the line firstEmptyLine
        listOfStates = []
        for i in range(0,len(state.getValues())): #parsing the line - the index of the colum

            childBoard = []
                
            #make a deepcopy of the state
            for r in range(0,len(state.getValues())):
                row = []
                for c in range(0,len(state.getValues())):
                    row.append(copy.deepcopy(state.getValues()[r][c]))
                childBoard.append(row)
            
            
            childBoard[firstEmptyLine][i] = 1  # add value 1 on the corrresponding position

            childState = State(self.getN())
            childState.setValues(childBoard)
            #print(childState)
            listOfStates.append(childState)

        return listOfStates
        

    '''
        computes a characteristic of a state that will be used in sorting them in a priority queue
        input: state - State
        output: nr - int
    '''
    def heuristic(self, state):
        if state.isOkUntilNow() == False:
            return state.getN() + 1
        
        firstEmptyLine = state.findFirstEmptyLine()
        if firstEmptyLine is None:  # board is completed
            return 0

        #compute how many correct children (until this step) i can derive from this state
        nr = 0
        for childState in self.expand(state):
                    if childState.isOkUntilNow():
                        nr+=1
        
        return nr 
    
    def heuristic2(self, state):
        if state.isOkUntilNow() == False:
            return state.getN() + 1
        
        firstEmptyLine = state.findFirstEmptyLine()
        if firstEmptyLine is None:  # board is completed
            return 0

        #compute how many correct 1's i can put on the remaining board (lines without 1's)
        nr = 0
        
        for line_index in range(firstEmptyLine, state.getN()):
            for col_index in range(0, state.getN()):
                #1.suma pe linie si coloana a fie 0 (ca sa pot pune 1)
                sum_line = 0
                sum_col = 0
                
                
                #2.sa nu atace pe diagonala - sa nu fie alti de 1 pe diagnala
                
                
                nr += 1
        
        
        return nr 
    

class Controller:
    def __init__(self, problem):
        self.__instance = problem

    def getProblem(self):
        return self.__instance

    '''
        depth first search (uninformed search) - does not use an heuristic function
        input: problem - Problem
        output: solutionState, or None
    '''
    def DFS(self, problem):
        root = problem.getInitialState()
        q = [root]

        while len(q) > 0:
            currentState = q.pop(0)
            #print(currentState)
            if currentState.isSolution():
                self.__instance.setFinalState(currentState)
                return currentState
            else:
                childrenStates = self.getProblem().expand(currentState)
                q = childrenStates + q # for dfs, q = childrenStates + q (to visit the children first)
                
        return None
    
    
    
    def GREEDY(self,problem):
        '''
        uses a priority queue: toVisit ( because aux is sorted before being added in front of the pr queue)
        the pr queue is sorted using a heuristic function that returns an int value for each state
        '''
        root = problem.getInitialState()
        
        
        visited = []
        toVisit = [root]
        while len(toVisit) > 0:
            currentState = toVisit.pop(0)
            #print(currentState)
            visited = visited + [currentState]
            if currentState.isSolution():
                self.getProblem().setFinalState(currentState)
                return currentState
            
            if currentState.isOkUntilNow():
                aux = []
                for childState in self.getProblem().expand(currentState):
                    if childState not in visited:
                        aux.append(childState)
    
                # map each state from aux into a list: [ state, h(state) ]
                aux = [[state, self.getProblem().heuristic(state)] for state in aux]
                aux.sort(key=lambda x: x[1])    #sort dupa int ul rezultat de la functia heurisica
                aux = [x[0] for x in aux]  # leave only the states, without the heuristics (x[1])
                toVisit = aux[:] + toVisit
        return None



class UI:
    def __init__(self, controller):
        self.__controller = controller

    def getController(self):
        return self.__controller

    @staticmethod
    def printCommmands():
        print("\tChoose method:")
        print("0. Exit")
        print("1. DFS")
        print("2. GREEDY")

    def runMenu(self):
        #print(self.getController().getProblem().getInitialState())
        while True:
            try:
                UI.printCommmands()
                cmd = int(input())

                if cmd == 0:
                    break
                elif cmd == 1:
                    self.runDFS()
                elif cmd == 2:
                    self.runGREEDY()
                else:
                    print("\tInvalid command!\n")

            except ValueError:
                print("\tInvalid command!\n")

    def runDFS(self):
        finalState = self.getController().DFS(self.getController().getProblem())
        if finalState is None:
            print("\tNo solution for this n!\n")
        else:
            print("Solution found <3")
            print(finalState)


    def runGREEDY(self):
        finalState = self.getController().GREEDY(self.getController().getProblem())
        if finalState is None:
            print("\tNo solution for this n!\n")
        else:
            print("Solution found <3")
            print(finalState)
            
            
            
            

def main():    
    n = int(input("give n:"))
    problem = Problem(n)
    ctrl = Controller(problem)
    ui = UI(ctrl)
    ui.runMenu()


main()
