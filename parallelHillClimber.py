import os

from solution import SOLUTION
import constants as c
import copy


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
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
        self.children = {}
        for i in self.parents.keys():
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID()
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
        for i in self.parents:
            if self.parents[i].fitness > self.parents[bestFit].fitness:
                bestFit = i
        self.parents[bestFit].Start_Simulation("GUI")

    def Evaluate(self, solutions):
        for i in solutions:
            solutions[i].Start_Simulation("DIRECT")
        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End("DIRECT")
