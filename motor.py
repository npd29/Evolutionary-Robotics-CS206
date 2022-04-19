import numpy
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.motorValues = numpy.zeros(c.simLength)
        # self.Prepare_To_Act()

    # def Prepare_To_Act(self):
    #     name = self.jointName.split('_')
    #     pieces = name[1].split('-')
    #     if pieces[2] == 'left':
    #         self.amplitude = float(c.variables['amplitudes'][pieces[0]][pieces[1]][0])
    #         self.frequency = float(c.variables['frequencies'][pieces[0]][pieces[1]][0])
    #         self.offset = float(c.variables['offsets'][pieces[0]][pieces[1]][0])
    #     elif pieces[2] == 'right':
    #         self.amplitude = float(c.variables['amplitudes'][pieces[0]][pieces[1]][1])
    #         self.frequency = float(c.variables['frequencies'][pieces[0]][pieces[1]][1])
    #         self.offset = float(c.variables['offsets'][pieces[0]][pieces[1]][1])
    #     for i in range(c.simLength):
    #         self.motorValues[i] = self.amplitude * numpy.sin(self.frequency * i / 100 + self.offset)

    def Set_Value(self, robot, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            maxForce=50)

    def Save_Values(self):
        numpy.save("data/motorValues.npy", self.motorValues)
