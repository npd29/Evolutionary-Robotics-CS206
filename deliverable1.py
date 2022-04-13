import glob
import os

from optimizedSolution import OPTOMIZED_SOLUTION
import constants as c
import copy
import csv
import numpy
import time
import random


class PHC_BEST:
    def __init__(self):
        self.currentBest = 0
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
        if self.bestFitnessFromFile < self.currentBest:
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
                if self.parents[i].fitness > self.bestFitnessFromFile:
                    self.currentBest = self.parents[i].fitness

    def Print(self):
        for i in self.parents.keys():
            print("\n", self.parents[i].fitness, self.children[i].fitness, "\n")

    def Show_Best(self):
        bestFit = 0
        # print("FINDING BEST FIT")
        for i in range(0, c.populationSize):
            # print("i: ", str(i), self.parents[bestFit].fitness, self.parents[i].fitness)
            if self.parents[i].fitness > self.parents[bestFit].fitness:
                bestFit = i
                # print("TRUE")
        c.fitness = self.parents[bestFit].fitness
        print("FINAL FITNESS:", c.fitness)
        input("Press ENTER to show the evolved robot and save")
        self.parents[bestFit].Start_Simulation("GUI")
        self.saveData(bestFit)

    def Evaluate(self, solutions):
        for i in range(c.populationSize):
            solutions[i].Start_Simulation("DIRECT")
        for i in range(c.populationSize):
            solutions[i].Wait_For_Simulation_To_End("DIRECT")

    def getFile(self):
        with open('data/fitnessData4Legs.csv', newline='') as readFile:
            robotReader = csv.DictReader(readFile, delimiter=',')
            i = 0
            population = 0
            self.bestFitnessFromFile = 0
            for robot in robotReader:
                if population < c.populationSize:
                    if population == 1:
                        self.bestFitnessFromFile = float(robot['fitness'])
                    population += 1
                    self.parents[i] = OPTOMIZED_SOLUTION(self.nextAvailableID, i + 1)
                    # print("OLD:", c.motorJointRange, )
                    # TODO: ENSURE THIS SETS VARIABLES
                    self.parents[i].Set_Vars(float(robot['FLUAmp']), float(robot['FRUAmp']), float(robot['BLUAmp']),
                                             float(robot['BRUAmp']),
                                             float(robot['FLLAmp']), float(robot['FRLAmp']), float(robot['BLLAmp']),
                                             float(robot['BRLAmp']),
                                             float(robot['FLUFreq']), float(robot['FRUFreq']), float(robot['BLUFreq']),
                                             float(robot['BRUFreq']),
                                             float(robot['FLLFreq']), float(robot['FRLFreq']), float(robot['BLLFreq']),
                                             float(robot['BRLFreq']),
                                             float(robot['FLUOffset']), float(robot['FRUOffset']),
                                             float(robot['BLUOffset']), float(robot['BRUOffset']),
                                             float(robot['FLLOffset']), float(robot['FRLOffset']),
                                             float(robot['BLLOffset']), float(robot['BRLOffset']),
                                             float(robot['motorJointRange']))
                    self.nextAvailableID += 1
                    i += 1
            while population < c.populationSize:
                self.parents[i] = OPTOMIZED_SOLUTION(self.nextAvailableID, 11)
                self.parents[i].Set_Vars(random.random() * numpy.pi, random.random() * numpy.pi,
                                         random.random() * numpy.pi, random.random() * numpy.pi,
                                         random.random() * numpy.pi, random.random() * numpy.pi,
                                         random.random() * numpy.pi, random.random() * numpy.pi,
                                         random.randint(0, 10), random.randint(0, 10), random.randint(0, 10),
                                         random.randint(0, 10), random.randint(0, 10), random.randint(0, 10),
                                         random.randint(0, 10), random.randint(0, 10), 0, 0, 0, 0, 0, 0, 0, 0,
                                         random.randint(0, 10))
                population += 1
                self.nextAvailableID += 1
                i += 1

    def saveData(self, best):
        with open('data/fitnessData4legs.csv', newline='') as readFile:
            robotReader = csv.reader(readFile, delimiter=',')
            reader = list(csv.reader(readFile))
            i = 1
            pos = 0
            row = self.Get_Vars()
            for topTenRobot in reader:
                if i != 1:  # skip the first line (headers)
                    if self.parents[best].fitness > float(topTenRobot[0]):  # check fitnesses
                        break  # if you find a fitness that is less than the best fitness
                i += 1

            i -= 1
            reader.insert(i, row)

        with open('data/fitnessData4Legs.csv', "w") as outfile:
            writer = csv.writer(outfile)
            # j = 0
            for line in reader:
                writer.writerow(line)
            # j += 1

        if i <= 10:  # if the new robot is in the top 10
            numpy.save("data/NNWeights/hold.npy", c.weights)
            for num in range(9, i - 1, -1):
                os.system(
                    "mv data/NNWeights/weights" + str(num) + ".npy data/NNWeights/weights" + str(num + 1) + ".npy")
                # input("did it work?")
            # input("ready to insert holds into "+str(i))
            os.system("mv data/NNWeights/hold.npy data/NNWeights/weights" + str(i) + ".npy")

    def Get_Vars(self):
        row = [c.fitness]
        for i in c.variables.keys():  # vars
            if i != 'fitness' and i != 'jointRange':
                for j in c.variables[i].keys():  # upper/lower
                    for k in c.variables[i][j].keys():  # front back
                        row.append(c.variables[i][j][k][0])
                        row.append(c.variables[i][j][k][1])
        row.append(c.variables.get('jointRange'))
        print("CHECKING VARS FROM DELIVERABLE1:", row)
        return row
