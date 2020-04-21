# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 20:03:23 2020

@author: hp840
"""

import math
import numpy as np
import random

'''
1. Sudoku game
Consider a Sudoku game - a logic puzzle represented on a n x n board; some squares
contain already a number, others must be completed with other numbers from {1,2,…,n} in such a
way that each line, column and square with the edge equal with √n must contain only different
numbers. Determine one correct solution for the puzzle.
'''

'''
Repr. : 
    -1 , empty space
    a number from 1 to 9 , otherwise
'''


def read_board(file):
    f = open(file)
    n = int(f.readline())
    table = []
    for i in range(n):
        line = f.readline()
        tok = line.split()
        for i in range(len(tok)):
            tok[i] = int(tok[i])
        table.append(tok)
        
    f.close()    
    return table, n


def nr_empty_spaces(table):
    nr = 0
    for line in table:
        for i in line:
            if i==-1:
                nr+=1
    return nr



def generate_random_sudoku(size, nr):
    return np.random.randint(1,size+1,nr)



def place_on_board(table,arr):
    idx=0
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == -1:
                table[i][j] = arr[idx]
                idx+=1  
    return table

        

def create_table(table, n):
    nr = nr_empty_spaces(table)
    arr = generate_random_sudoku(n,nr)
    tbl = place_on_board(table,arr)
    return tbl
  



def is_solution(table, n):
    #verify - diff values on each line
    for line in table:
        if len(line)!=len(set(line)):
            return False
        
    #verify - diff values on each column
    for i in range(n):
        col = []
        for j in range(n):
            col.append(table[j][i])
        if len(col)!=len(set(col)):
            return False
        
    #verify - diff values in each small square (of dim sqrt(n)*sqrt(n))
    for i in range(0, len(table), int(math.sqrt(len(table)))):
        for j in range(0, len(table), int(math.sqrt(len(table)))):
            elems_in_square = []
            for t in range(i, i + int(math.sqrt(len(table)))):
                for t2 in range(j, j + int(math.sqrt(len(table)))):
                    elems_in_square.append(table[t][t2])
            if len(elems_in_square) != len(set(elems_in_square)):
                return False
            if len(elems_in_square) != len(table):
                return False
        
    return True




def sudoku(nr_de_incercari):
    table, n = read_board("sudoku.txt")
    copie, n = read_board("sudoku.txt")
    print("problem:")
    for l in table:
        print(l)
    
    for i in range(nr_de_incercari):
        table, n = read_board("sudoku.txt")
        

        tbl = create_table(table,n)
        
        #print(tbl)
                
        res = is_solution(tbl,n)
        if res == True:
            print("solution")
            for i in tbl:
                print(i)
            return
    print("no solution")

#sudoku(10000)
'''
solutie pt sudoku mic:
[3, 4, 1, 2]
[2, 1, 4, 3]
[1, 2, 3, 4]
[4, 3, 2, 1]
'''
            

'''
2. Implement an algorithm that solves a crypt-arithmetic problem as the ones presented in
Figure 4 knowing that:
● Each letter represent a hexadecimal cipher;
● The result of the arithmetic operation must be correct when the letters are replaced
by numbers;
● The numbers can not start with 0;
● Every problem can have only one solution.
'''        

def read_words(file):
    f = open(file)
    w1 = f.readline()
    w2 = f.readline()
    w3 = f.readline()

    word1 = ""
    word2 = ""
    word3 = ""

    letters = []
    for i in w1:
        if i!='\n':
            letters.append(i)
            word1+=i
    for i in w2:
        if i!='\n':
            letters.append(i)
            word2+=i
    for i in w3:
        if i!='\n':
            letters.append(i)
            word3+=i

    #remove duplicates from letters
    letters = set(letters)
    letters = list(letters)
    f.close()
    
    #return letters,w1,w2,w3
    return letters,word1,word2,word3


def generate_random_codification(l):
    indexes = np.random.randint(0,16,len(l))
    hex_list = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    code_dict = {}
    for i in range(len(l)):
        code_dict[l[i]] = hex_list[indexes[i]]
    return code_dict

def is_solution_crypt(code_dict, w1, w2, w3):

    if code_dict[w1[0]] == "0":
        return False
    if code_dict[w2[0]] == "0":
        return False
    if code_dict[w3[0]] == "0":
        return False

    w1_hexa = ""
    for letter in w1:
        w1_hexa += code_dict[letter]
    w2_hexa = ""
    for letter in w2:
        w2_hexa += code_dict[letter]
    w3_hexa = ""
    for letter in w3:
        w3_hexa += code_dict[letter]
    
    res = hex(int(w1_hexa,16)+int(w2_hexa,16)).upper()
    
    #print(res)
    #print(w3_hexa)
    
    if "0X"+w3_hexa == res:
        return True
    return False


def crypt(nr_de_incercari):
    l,w1,w2,w3 = read_words("crypt2.txt")
    
    print("problem")
    print(l)
    print(w1)
    print(w2)
    print(w3)
    
    for i in range(nr_de_incercari):
        code_dict = generate_random_codification(l)
        #print(code_dict)
        if is_solution_crypt(code_dict,w1,w2,w3):
            print("solution")
            print(code_dict)
            return
    print("no solution")

#crypt(100000)

'''
DUPA 100000000000 DE ANI
finally o solutie.............

['t', 'h', 'e', 'p', 'a', 'l']
eat
that
apple
{'t': 'F', 'h': '2', 'e': 'E', 'p': '0', 'a': '1', 'l': '3'}

TODO - verif daca e buna
E1F + F21F = 1003E
YAYYYY <3
'''


'''
solutie de la prima rulare yay <3

['d', 'm', 's', 'e', 'o', 'r', 'n', 'y']
send
more
money
{'d': '0', 'm': '1', 's': 'F', 'e': 'A', 'o': '0', 'r': 'F', 'n': 'B', 'y': 'A'}

'''






'''
3. Geometric forms
Consider the geometric forms from Figure 5. Determine an arrangement for this forms on a
square board of 5x6 in such a way that the board will be uniform covered and the forms will not
overlap.

'''

'''
Repr. : 0 - empty cell
        1,2... (code for every particular shape) - occupied cell
'''

def read_shapes():
    
    f = open("shapes3.txt") #shapes -> greu de gast solutia....
                            # shapes2 sau shapes3 -> mneh, dar macar vad ca merge
    
    #nr of shapes
    n = int(f.readline())
    
    shapes = []

    for i in range(n):
        sh = []
        line = f.readline()
        while line not in ["x\n", "x"]:
            tok = line.split()
            for i in range(len(tok)):
                tok[i] = int(tok[i])
            sh.append(tok)
            line = f.readline()
        #shapes.append(sh)
        shapes.append(np.array(sh, dtype=int))    
    f.close()    
    return shapes

'''
shapes = read_shapes()
for s in shapes:
    print(s)
    print("")
'''

def is_uniform_covered(tbl):
    '''
    verifies if the table is full covered (is solution)
    '''
    for l in tbl:
        for i in l:
            if i == 0:
                return False
    return True


def generate_position(x,y):
    '''
    x,y - dim tablei (x*y)
    returns a random position on the board
    '''
    i = np.random.randint(0,x)
    j = np.random.randint(0,y)
    return i,j
    
def shape_fits(tbl, shape, i , j, x, y):
    '''
    verifies if the shape fits on the board , having the up left corner on the
    position : tbl[i][j]
    
    fits means  : 1. be inside the board
                  2. do not overlap other shapes
    '''
    
    #1. the shape must be inside the board
    if i + len(shape) > x:
        return False
    if j + len(shape[0]) > y:
        return False
    
    #2. the shape must not overlap other shapes from the board
    for i2 in range( len(shape)):
        for j2 in range (len(shape[i2])): #parsing the shape
            if shape[i2][j2] != 0 and tbl[i2 + i][j2 + j] != 0: #there is a position 
                                                        #that is not empty -> overlap
                                                        #at least one of them should be 0 
                return False
            
    return True
    
def put_shape(tbl, shape, i, j, x ,y):
    '''
    if the shape fits, put it on the board
    '''
    for i2 in range( len(shape)):
        for j2 in range (len(shape[i2])):
            tbl[i + i2][j + j2] += shape[i2][j2] #at least ne of them is 0, so adding is the
                                            #best solution because it doasn t change anything
    
def geometric_forms(nr_incercari):
    #x, y, shapes = read_shapes("forms.txt")
    x=5
    y=6
    
    shapes = read_shapes()
    
    print("problem")
    print("table of dimension " + str(x) + "x" + str(y))
    print("shapes:")
    #print(shapes)
    for s in shapes:
        print(s)
        print("")
    
    
    for i in range(nr_incercari):
        '''creates a x*y table with only zeros'''
        table = np.zeros((x,y),  dtype = int)
        
        shapes = read_shapes()

        '''
        choose shapes in random order and try to put them on a random generated position
        '''
        while( len(shapes) != 0):
            currentShapeIndex = np.random.randint(0, len(shapes))
            currentShape = shapes.pop(currentShapeIndex)
            i,j = generate_position(x,y)
            if shape_fits(table, currentShape,i,j,x,y) == True:
                put_shape(table, currentShape, i,j,x,y)
            
        print(table)
        if is_uniform_covered(table)==True:
            print("solution")
            print(table)
            return
    print("no solution")


#geometric_forms(10)

'''
MAIN FUNCTION
'''



def main():
    print("1.sudoku \n2.crypt \n3.geometric forms \n")
    cmd = input("Command:")
    nr_incercari = int(input("Nr de incercari:"))
    if(cmd == "1"):
        sudoku(nr_incercari)
    if(cmd == "2"):
        crypt(nr_incercari)
    if(cmd == "3"):
        geometric_forms(nr_incercari)

main()
    


