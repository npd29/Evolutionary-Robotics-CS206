import random
import time

import numpy
import pyrosim.pyrosim as pyrosim
import os
import constants as c
class OPTOMIZED_SOLUTION:

    def __init__(self, nextAvailableID, recreateID):

        self.myID = nextAvailableID
        if recreateID > 10:
            self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons)
            self.weights = self.weights * 2 - 1
        else:
            try:
                self.weights = numpy.load("data/NNWeights/weights"+str(recreateID)+".npy")
            except FileNotFoundError:
                self.weights = numpy.load("data/NNWeights/weights" + str(recreateID+1) + ".npy")
        c.weights = self.weights

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " " + str(c.frontAmp) + " " + str(c.backAmp) + " " +
                  str(c.frontFreq) + " " + str(c.backFreq) + " " + str(c.frontOffset) + " " + str(c.backOffset) + " " + str(c.motorJointRange) + " &")

    def Wait_For_Simulation_To_End(self, directOrGUI):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            #print(fitnessFileName)
            time.sleep(0.1)
        file = open(fitnessFileName, "r")
        self.fitness = float(file.read())
        file.close()
        os.system("rm " + fitnessFileName)

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-5, 5, .5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        #TORSO
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])

        #UPPER LEGS
        pyrosim.Send_Joint(name="Torso_FLU", parent="Torso", child="FLU", type="revolute",
                           position=[0, .5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FLU", pos=[0, .5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name="Torso_BLU", parent="Torso", child="BLU", type="revolute",
                           position=[0, -0.5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BLU", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name="Torso_FRU", parent="Torso", child="FRU", type="revolute",
                           position=[-0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="FRU", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])

        pyrosim.Send_Joint(name="Torso_BRU", parent="Torso", child="BRU", type="revolute",
                           position=[0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="BRU", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])

        #LOWER LEGS
        pyrosim.Send_Joint(name="FLU_FLL", parent="FLU", child="FLL", type="revolute",
                           position=[0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FLL", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="BLU_BLL", parent="BLU", child="BLL", type="revolute",
                           position=[0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BLL", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="FRU_FRL", parent="FRU", child="FRL", type="revolute",
                           position=[-1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="FRL", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="BRU_BRL", parent="BRU", child="BRL", type="revolute",
                           position=[1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="BRL", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="FLL")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BLL")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FRL")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="BRL")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_BLU")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_FLU")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_FRU")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_BRU")
        pyrosim.Send_Motor_Neuron(name=8, jointName="BLU_BLL")
        pyrosim.Send_Motor_Neuron(name=9, jointName="FLU_FLL")
        pyrosim.Send_Motor_Neuron(name=10, jointName="FRU_FRL")
        pyrosim.Send_Motor_Neuron(name=11, jointName="BRU_BRL")

        for currentRow in range(c.numSensorNeurons):
                for currentColumn in range(c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + c.numSensorNeurons,
                                         weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

        while not os.path.exists("brain" + str(self.myID) + ".nndf"):
                time.sleep(0.01)

    def Mutate(self):
        row = random.randint(0, 2)
        col = random.randint(0, 1)
        self.weights[row][col] = random.random() * 2 - 1
        self.Mutate_Vars(random.randint(0, 26))

    def Mutate_Vars(self, var):
        print("MUTATING VARIABLE", var)
        print("VALUE:", c.variables[var], end=" ")
        if var == 0: # fitness
            print()
        #vars 1-4 are upper amps
        elif var == 1 or var == 2:#front
            r = numpy.pi*random.random()
            c.FLUAmp = r
            c.FRUAmp = r
            print(c.frontAmp)

        elif var == 3 or var == 4:#back
            r = numpy.pi*random.random()
            c.BLUAmp = r
            c.BRUAmp = r
            print(c.frontAmp)

        #5-8 are lower amps
        elif var == 5 or var == 6:#front
            r = numpy.pi*random.random()
            c.FLLAmp = r
            c.FRLAmp = r
            print(c.frontAmp)

        elif var == 5 or var == 6:#back
            r = numpy.pi*random.random()
            c.BLUAmp = r
            c.BRUAmp = r
            print(c.frontAmp)

        elif var == 3:
            r = random.random()*10
            c.frontFreq = r
            print(c.frontFreq)

        elif var == 4:
            r = random.random()*10
            c.backFreq = r
            print(c.backFreq)

        elif var == 5:
            c.frontOffset = random.random()*10
            print(c.frontOffset)

        elif var == 6:
            c.backOffset = random.random()*10
            print(c.backOffset)

        elif var == 7:
            c.motorJointRange = random.random()*5
            print(c.motorJointRange)

    def Set_ID(self, newID):
        self.myID = newID

    def Set_Vars(self, frontAmp, backAmp, frontFreq, backFreq, frontOffset, backOffset, motorJointRange):
        c.frontAmp = frontAmp
        c.backAmp = backAmp
        c.frontFreq = frontFreq
        c.backFreq = backFreq
        c.frontOffset = frontOffset
        c.backOffset = backOffset
        c.motorJointRange = motorJointRange
