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
        print("FINDING BEST FIT")
        for i in range(0, c.populationSize):
            print("i: ", str(i), self.parents[bestFit].fitness, self.parents[i].fitness)
            if self.parents[i].fitness > self.parents[bestFit].fitness:
                bestFit = i
                print("TRUE")
        c.fitness = self.parents[bestFit].fitness
        print("FINAL FITNESS:", c.fitness)
        input("Press enter to show the evoloved robot")
        self.parents[bestFit].Start_Simulation("GUI")
        self.saveData(bestFit)

    def Evaluate(self, solutions):
        for i in range(c.populationSize):
            solutions[i].Start_Simulation("DIRECT")
        for i in range(c.populationSize):
            solutions[i].Wait_For_Simulation_To_End("DIRECT")

    def getFile(self):
        with open('data/fitnessData.csv', newline='') as readFile:
            robotReader = csv.DictReader(readFile, delimiter=',')
            i=0
            population = 0
            for robot in robotReader:
                population += 1
                self.parents[i] = OPTOMIZED_SOLUTION(self.nextAvailableID, i)
                # print("OLD:", c.motorJointRange, )
                self.parents[i].Set_Vars(float(robot['frontLeftAmp']), float(robot['frontRightAmp']), float(robot['backLeftAmp']),
                                         float(robot['backRightAmp']), float(robot['frontLeftFreq']), float(robot['frontRightFreq']),
                                         float(robot['backLeftFreq']), float(robot['backRightFreq']), float(robot['frontLeftOffset']),
                                         float(robot['frontRightOffset']), float(robot['backOffset']), float(robot['backRightOffset']),
                                         float(robot['motorJointRange']))
                self.nextAvailableID += 1
                i += 1
            while population < c.populationSize:
                self.parents[i] = OPTOMIZED_SOLUTION(self.nextAvailableID, 11)
                self.parents[i].Set_Vars(numpy.pi*random.random(), numpy.pi*random.random(), numpy.pi*random.random(), numpy.pi*random.random(),
                                         random.random()*10, random.random()*10, random.random()*10, random.random()*10,
                                         random.random(), random.random(), random.random(), random.random(),
                                         random.random())
                population += 1
                self.nextAvailableID += 1
                i += 1


    def saveData(self, best):
        with open('data/fitnessData.csv', newline='') as readFile:
            robotReader = csv.reader(readFile, delimiter=',')
            reader = list(csv.reader(readFile))
            i = 1
            pos = 0
            row = [c.fitness, c.frontLeftAmp, c.frontRightAmp, c.backLeftAmp, c.backRightAmp, c.frontLeftFreq, c.frontRightFreq, c.backLeftFreq,
             c.backRightFreq, c.frontLeftOffset, c.frontRightOffset, c.backLeftOffset, c.backRightOffset, c.motorJointRange]
            for robot in reader:
                if i != 1:
                    if self.parents[best].fitness > float(robot[0]):
                        break
                i += 1
            reader.insert(i-1, row)

        with open('data/fitnessData.csv', "w") as outfile:
            writer = csv.writer(outfile)
            j = 1
            for line in reader:
                if j <= 10:
                    writer.writerow(line)
                j += 1

        if i <= 10: #if the new robot is in the top 10
            print("I:", i)
            numpy.save("data/NNWeights/hold.npy", c.weights)
            for num in range(9, i, -1):
                if not os.path.exists("data/NNWeights/weights"+str(num)+".npy"):
                    numpy.save("data/NNWeights/weights"+str(num)+".npy", c.weights)
                os.system("mv data/NNWeights/weights" + str(num) + ".npy data/NNWeights/weights" + str(num+1) + ".npy")
                time.sleep(0.1)

            while not os.path.exists("data/NNWeights/hold.npy"):
                time.sleep(0.1)
            os.system("mv data/NNWeights/hold.npy data/NNWeights/weights" + str(i) + ".npy")
