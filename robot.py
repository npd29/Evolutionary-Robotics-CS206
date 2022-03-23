import os
import time

from motor import MOTOR
from sensor import SENSOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy
from pyrosim.neuralNetwork import NEURAL_NETWORK


class ROBOT:
    def __init__(self, solutionID):
        self.nn = NEURAL_NETWORK("brain"+str(solutionID)+".nndf")
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        try:
            os.system("rm brain"+str(solutionID)+".nndf")
        except:
            pass

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for i in self.sensors:
            self.sensors[i].Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robot, desiredAngle)

                # print(neuronName, jointName, desiredAngle)

        # for i in self.motors:
        #     self.motors[i].Set_Value(self.robot, t)

    def Think(self):
        self.nn.Update()
        self.nn.Print()

    def Get_Fitness(self, solutionID):
        stateOfLinkZero = p.getLinkState(self.robot, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoorOfLinkZero = positionOfLinkZero[0]
        file = open("tmp" + str(solutionID) + ".txt", "w")
        time.sleep(.01)
        os.system("mv tmp" + str(solutionID) + ".txt fitness" + solutionID + ".txt")
        file.write(str(xCoorOfLinkZero))
        file.close()
