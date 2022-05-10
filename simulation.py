from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import constants as c
import os
import csv


class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        self.id = solutionID
        if self.directOrGUI == "GUI":
            physicsClient = p.connect(p.GUI)
        else:
            physicsClient = p.connect(p.DIRECT)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    def Run(self):
        if self.directOrGUI == 'GUI':
            counter = 1
            while os.path.exists("data/XYData/" + str(counter) + ".csv"):
                counter += 1
            outfile = open("data/XYData/" + str(counter) + ".csv", 'w')
            writer = csv.writer(outfile)

        for i in range(c.simLength):
            if self.directOrGUI == 'GUI':
                time.sleep(.01)
                if i%10 == 0:
                    line = self.getXY()
                    # line = position[0] + "," + position[1]
                    writer.writerow(line)
            p.stepSimulation()
            distances = self.robot.Sense(i, self.world)
            self.robot.Think(distances)
            # print(self.robot.Get_Distance_To_Goal())
            self.robot.Act(i)
            # backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            # frontAngles[i] = c.frontAmp * numpy.sin(c.frontFreq * i / 100 + c.frontOffset)
            # backAngles[i] = c.backAmp * numpy.sin(c.backFreq * i / 100 + c.backOffset)
            # if self.directOrGUI == "GUI":
            #     time.sleep(.00001)

        if self.directOrGUI == 'GUI':
            outfile.close()

    def Get_Fitness(self):
        self.robot.Get_Fitness(self.id)

    def getXY(self):
        return self.robot.GetXY()

    def SaveData(self):
        pass

    def __del__(self):
        p.disconnect()
