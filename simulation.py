from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import constants as c


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
        for i in range(c.simLength):
            if self.directOrGUI == 'GUI':
                time.sleep(.001)
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            # backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            # frontAngles[i] = c.frontAmp * numpy.sin(c.frontFreq * i / 100 + c.frontOffset)
            # backAngles[i] = c.backAmp * numpy.sin(c.backFreq * i / 100 + c.backOffset)
            if self.directOrGUI == "GUI":
                time.sleep(.00001)

    def Get_Fitness(self):
        self.robot.Get_Fitness(self.id)

    def __del__(self):
        p.disconnect()
