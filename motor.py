import numpy
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.motorValues = numpy.zeros(c.simLength)
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.frontAmp
        self.frequency = c.frontFreq
        self.offset = c.frontOffset
        # TODO: change this back to torso backleg
        if self.jointName == "Torso_FrontLeg":
            self.frequency /= 2
        for i in range(c.simLength):
            self.motorValues[i] = self.amplitude * numpy.sin(self.frequency * i / 100 + self.offset)

    def Set_Value(self, robot, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            maxForce=50)

    def Save_Values(self):
        numpy.save("data/motorValues.npy", self.motorValues)
