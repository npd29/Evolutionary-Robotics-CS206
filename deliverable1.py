import glob
import os

from optimizedSolution import OPTOMIZED_SOLUTION
import constants as c
import copy
import csv
import numpy

class PHC_BEST:
    def __init__(self):
        files = glob.glob("brain*.nndf")
        for file in files:
            os.remove(file)
        files = glob.glob("fitness*.txt")
        for file in files:
            os.remove(file)
        files = glob.glob("tmp*.txt")
        for file in files:
            os.remove(file)
        self.parents = dict()
        self.nextAvailableID = 0
        # Simulate all 10 robots
        self.getFile()


    def Evolve(self):
        self.Evaluate(self.parents)
        # self.parent.Evaluate("GUI")
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = dict()
        for i in self.parents.keys():
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in self.children:
            self.children[i].Mutate()

    def Select(self):
        for i in self.parents:
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]


    def Print(self):
        for i in self.parents.keys():
            print("\n", self.parents[i].fitness, self.children[i].fitness, "\n")


    def Show_Best(self):
        bestFit = 0
        for i in range(0, len(self.parents.keys())-1):
            if self.parents[i].fitness > self.parents[bestFit].fitness:
                bestFit = i
        c.fitness = self.parents[bestFit].fitness
        print("FINAL FITNESS:", c.fitness)
        self.parents[bestFit].Start_Simulation("GUI")
        self.saveData()

    def Evaluate(self, solutions):
        for i in range(c.populationSize):
            solutions[i].Start_Simulation("DIRECT")
        for i in range(c.populationSize):
            solutions[i].Wait_For_Simulation_To_End("DIRECT")

    def getFile(self):
        with open('data/fitnessData.csv', newline='') as readFile:
            robotReader = csv.DictReader(readFile, delimiter=',')
            i=0
            c.populationSize = 0
            for robot in robotReader:
                c.populationSize += 1
                self.parents[i] = OPTOMIZED_SOLUTION(self.nextAvailableID)
                # print("OLD:", c.motorJointRange, )
                self.parents[i].Set_Vars(float(robot['frontAmp']), float(robot['backAmp']), float(robot['frontFreq']),
                                         float(robot['backFreq']), float(robot['frontOffset']), float(robot['backOffset']),
                                         float(robot['motorJointRange']))
                self.nextAvailableID += 1
                i += 1


    def saveData(self):
        row = [c.fitness, c.frontAmp, c.backAmp, c.frontFreq, c.backFreq, c.frontOffset, c.backOffset, c.motorJointRange]
        with open('data/fitnessData.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)

        numpy.save("./data/NN Weights/" + str(c.saveID) + ".npy", c.weights)
