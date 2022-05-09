import os
import time
from os.path import exists
from motor import MOTOR
from sensor import SENSOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
import math
import world
import numpy
from pyrosim.neuralNetwork import NEURAL_NETWORK


class ROBOT:
    def __init__(self, solutionID):
        self.sensors = {}
        self.motors = {}
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        # if os.path.exists("brain"+str(solutionID)+".nndf"):
        #     print("FILE EXISTS! CHECKED FOR FILE: ","brain"+str(solutionID)+".nndf")
        self.nn = NEURAL_NETWORK("brain"+str(solutionID)+".nndf")
        os.system("rm brain"+str(solutionID)+".nndf")

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            if linkName.split('-')[0] == 'lower': # added this because it wasnt working
                self.sensors[linkName] = SENSOR(linkName)
        self.sensors["nearest-obstacle"] = SENSOR("nearest-obstacle")
        self.sensors["goal"] = SENSOR("goal")

    def Sense(self, t, world):
        sensorNum = 0
        for i in self.sensors:
            if sensorNum < c.numSensorNeurons-2:
                self.sensors[i].Get_Value(t)
            sensorNum += 1
        #  Find distnace to nearest object and set sensor neuron
        nearestPos = .5**world.getNearestPosition()
        # print(world.getNearestPosition())
        self.sensors["nearest-obstacle"].Set_Value(t, nearestPos)

        #  find distance to goal and set sensor neuron
        distance = self.Get_Distance_To_Goal()
        self.sensors["goal"].Set_Value(t, distance)
        # print(self.Get_Distance_To_Goal())
        return [nearestPos, distance]

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robot, desiredAngle)

                # print(neuronName, jointName, desiredAngle)

        # for i in self.motors:
        #     self.motors[i].Set_Value(self.robot, t)

    def Think(self, distances):
        self.nn.Update(distances)
        # self.nn.Print()

    def Get_Fitness(self, solutionID):  # Use distance formula
        # stateOfLinkZero = p.getLinkState(self.robot, 0)
        # positionOfLinkZero = stateOfLinkZero[0]
        # xCoorOfLinkZero = positionOfLinkZero[0]
        # yCoorOfLinkZero = positionOfLinkZero[1]
        distance = self.Get_Distance_To_Goal()
        file = open("tmp" + str(solutionID) + ".txt", "w")
        file.write(str(distance))
        file.close()
        os.system("mv tmp" + str(solutionID) + ".txt fitness" + str(solutionID) + ".txt")

    def GetXY(self):
        stateOfLinkZero = p.getLinkState(self.robot, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoorOfLinkZero = positionOfLinkZero[0]
        yCoorOfLinkZero = positionOfLinkZero[1]
        return [xCoorOfLinkZero, yCoorOfLinkZero]

    def Get_Distance_To_Goal(self):
        position = self.GetXY()
        xDelta = position[0] - c.goal[0]
        yDelta = position[1] - c.goal[1]
        distance = math.sqrt(xDelta**2+yDelta**2)
        return distance