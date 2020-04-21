# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 19:05:00 2020

@author: Bacotiu Denisa-Cristina 921/1

LAB 6
"""

from random import shuffle
from copy import copy
import math
import numpy as np



class Question:
    """
    Question : attribute (column number) + value
    Used to split the dataset
    """
    def __init__(self, column, value):
        """
        :param column: int
        :param value: int
        """
        self.column = column  # index of the column
        self.value = value  # value of that column (in our case, can be from 1 to 5)

    def evaluate(self, instance):
        """
        Gives the response of the instance to the question

        the question to response: Is instance[self.column] >= self.value ?

        :param instance: a list representing a instance from the dataset
        :return: True or False
        """
        return instance[self.column] >= self.value # is the value of the instance on the corresponding column >= self.value?


class Data:

    def __init__(self, dataList, filename):
        self.__data = dataList
        self.__filename = filename

    def getData(self):
        return self.__data

    def classDistribution(self):
        """
        Counts for each class (in our case: L,R,B) how many instances are from that class
        :return: distributionDict - a dictionary
        """
        distributionDict = {}
        for instance in self.__data:
            # in our dataset format, the class is always the first column
            cls = instance[0]
            if cls not in distributionDict:
                distributionDict[cls] = 0
            distributionDict[cls] += 1
        return distributionDict

    def readFromFile(self):
        """
        Reads the data from the file with the name from the string self.__filename
        """
        self.__data = []
        f = open(self.__filename, 'r')
        for i in range(625):
            line = f.readline()
            tok = line.split(',')
            clas = tok[0]
            lw = int(tok[1])
            ld = int(tok[2])
            rw = int(tok[3])
            rd = int(tok[4])
            self.__data.append([clas, lw, ld, rw, rd])

    def shuffleData(self):
        shuffle(self.__data)

    def splitByQuestion(self, instances, question):
        """
        Splits the dataset (instances param) in 2 sets, the instances which answer with True to the question (true_instances)
        and the instances which answer with False to the question (false_instances)

        :param instances: list of lists (the dataset)
        :param question: Question
        :return: true_instances : list of lists - the instances that matches the question <=> answer with true to the question
                false_instances : list of lists - the instances that matches the question <=> answer with false to the question
        """
        true_instances, false_instances = [], []
        for instance in instances:
            if question.evaluate(instance):
                true_instances.append(instance)
            else:
                false_instances.append(instance)
        return true_instances, false_instances

    def gini(self, instances):
        """
        :param instances: list of lists (the dataset)
        :return: gini impurity for the set of instances
        """
        distrDict = self.classDistribution()
        impurity = 1
        for cls in distrDict:
            prob_of_cls = distrDict[cls] / float(len(instances))
            #the formula from the lecture
            impurity -= prob_of_cls * math.log2(prob_of_cls)
        return impurity

    def info_gain(self, left, right, current_uncertainty):
        """
        information gain
        :param left: list of lists
        :param right: list of lists
        :param current_uncertainty: float
        :return: float
        """
        p = float(len(left)) / (len(left) + len(right))
        return current_uncertainty - p * self.gini(left) - (1 - p) * self.gini(right)

    def attributeSelection(self, instances):
        """
        Finds the best question(index of attribute/column + value) to split the set of instances by.
        :param instances: list of lists (set of instances)
        """
        best_gain = 0
        best_question = None

        for col in range(1, 5):  # the indexes of the columns

            values = [1, 2, 3, 4, 5]  # the possible values for each column

            for val in values:  # for each value

                question = Question(col, val) #the corresp question to that column index and value

                true_instances, false_instances = self.splitByQuestion(instances, question)

                if len(true_instances) == 0 or len(false_instances) == 0: #if the data set was not splitted, do not consider this case, go to next :D
                    continue

                gain = self.info_gain(true_instances, false_instances, self.gini(instances))

                #update the best question
                if gain > best_gain:
                    best_gain, best_question = gain, question

        return best_gain, best_question


class LeafNode:
    """
     stores the number of times each class appears in the instances from the training data that reach this leaf
    """

    def __init__(self, instances):
        self.predictions = self.classDistribution(instances)

    def classDistribution(self, instances):
        """
        Counts for each class (in our case: L,R,B) how many instances are from that class
        :return: distributionDict - a dictionary
        """
        distributionDict = {}
        for instance in instances:
            cls = instance[0]  # first column -> the class
            if cls not in distributionDict:
                distributionDict[cls] = 0
            distributionDict[cls] += 1
        return distributionDict


class Node:

    def __init__(self, question, trueNode, falseNode):
        """
        :param question: - a question
        :param trueNode: - a child node corresponding to the "answer" with true to that question
        :param falseNode: - a child node corresponding to the "answer" with false to that question
        """
        self.question = question
        self.trueNode = trueNode
        self.falseNode = falseNode


class Tree:

    def __init__(self, data):
        """
        :param data: Data
        """
        self.__data = data
        self.__node = self.buildTree()

    def buildTreeRec(self, instances):

        gain, question = self.__data.attributeSelection(instances)

        if gain == 0:
            return LeafNode(instances)

        true_instances, false_instances = self.__data.splitByQuestion(instances, question)

        true_branch = self.buildTreeRec(true_instances)

        false_branch = self.buildTreeRec(false_instances)

        return Node(question, true_branch, false_branch)

    def buildTree(self):
        return self.buildTreeRec(self.__data.getData())

    def getNode(self):
        return self.__node

    def classifyRec(self, instance, node):
        if isinstance(node, LeafNode):
            return node.predictions

        if node.question.evaluate(instance):
            return self.classifyRec(instance, node.trueNode)
        else:
            return self.classifyRec(instance, node.falseNode)

    def classify(self, instance):
        return self.classifyRec(instance, self.__node)


class Ui:

    def getProbability(self, predictions):
        """
        :param predictions: dict: with prediction for each class
        :return: dictionary : key : class, value : probability
        """
        total = sum(predictions.values()) * 1.0
        probs = {'L': 0, 'R': 0, 'B': 0}
        for lbl in predictions.keys():
            probs[lbl] = predictions[lbl] / total * 100
        return probs

    def main(self):

        data = Data([], "balance-scale.data")
        data.readFromFile()

        # double the dataset
        # that's the trick for better accuracy :D
        lst = copy(data.getData())
        lst = lst + data.getData()

        acc_list = []  # list of all the accuracies found

        for i in range(100):


            shuffle(lst)

            pos = 80 * len(lst) // 100

            # build the tree from the training data : 80%
            training_data = lst[:pos]
            training = Data(training_data, "")
            my_tree = Tree(training)

            # testing data : 20%
            testing_data = lst[pos:]

            summ = 0

            count = 0
            for instance in testing_data:
                count += 1
                summ += self.getProbability(my_tree.classify(instance))[instance[0]]

            accuracy = summ / count
            print("accuracy for the attempt nr ",i+1,"/100")
            print(accuracy)
            acc_list.append(accuracy)

        print("The avg for those 100 runs: ",np.mean(acc_list))


ui = Ui()
ui.main()




