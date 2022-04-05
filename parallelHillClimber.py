import glob
import os

from solution import SOLUTION
import constants as c
import copy


class PARALLEL_HILL_CLIMBER:
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
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

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
        self.parents[bestFit].Start_Simulation("GUI")

    def Evaluate(self, solutions):
        for i in range(c.populationSize):
            solutions[i].Start_Simulation("DIRECT")
        for i in range(c.populationSize):
            solutions[i].Wait_For_Simulation_To_End("DIRECT")
