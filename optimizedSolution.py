import random
import time

import numpy
import pyrosim.pyrosim as pyrosim
import os
import constants as c
class OPTOMIZED_SOLUTION:

    def __init__(self, nextAvailableID):

        self.myID = nextAvailableID
        self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
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
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position=[0, .5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, .5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                           position=[0, -0.5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute",
                           position=[-0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])

        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute",
                           position=[0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])

        #LOWER LEGS
        pyrosim.Send_Joint(name="FrontLeg_FrontLower", parent="FrontLeg", child="FrontLower", type="revolute",
                           position=[0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLower", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="BackLeg_BackLower", parent="BackLeg", child="BackLower", type="revolute",
                           position=[0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLower", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="LeftLeg_LeftLower", parent="LeftLeg", child="LeftLower", type="revolute",
                           position=[-1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLower", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="RightLeg_RightLower", parent="RightLeg", child="RightLower", type="revolute",
                           position=[1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLower", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="FrontLower")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLower")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="LeftLower")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="RightLower")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=8, jointName="BackLeg_BackLower")
        pyrosim.Send_Motor_Neuron(name=9, jointName="FrontLeg_FrontLower")
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftLeg_LeftLower")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightLeg_RightLower")

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
        self.Mutate_Vars(random.randint(0, 7))

    def Mutate_Vars(self, var):
        print("MUTATING VARIABLE", var)
        print("VALUES:", c.variables[var], end=" ")
        if var == 0: # fitness
            pass
        elif var == 1:
            c.frontAmp = numpy.pi*random.random()
        elif var == 2:
            c.backAmp = numpy.pi*random.random()
        elif var == 3:
            c.frontFreq = random.random()*10
        elif var == 4:
            c.backFreq = random.random()*10
        elif var == 5:
            c.frontOffset = random.random()
        elif var == 5:
            c.backOffset = random.random()
        elif var == 7:
            c.motorJointRange = random.random()

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
    #
    # def Get_Vars(self):
    #     c.frontAmp = self.front
    #     c.backAmp = backAmp
    #     c.frontFreq = frontFreq
    #     c.backFreq = backFreq
    #     c.frontOffset = frontOffset
    #     c.backOffset = backOffset
    #     c.motorJointRange = motorJointRange
