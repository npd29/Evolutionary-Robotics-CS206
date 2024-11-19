import pyrosim.pyrosim as pyrosim
import random


def createWorld():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-5, 5, .5], size=[1, 1, 1])
    pyrosim.End()


def createRobot():
    pass





createRobot()
