import pybullet as p
import math

class WORLD:
    def __init__(self):
        planeId = p.loadURDF("plane.urdf")
        self.objects = p.loadSDF("world.sdf")

    def getObjectPosition(self, objectID):
        posAndOrientation = p.getBasePositionAndOrientation(self.objects[objectID])
        position = posAndOrientation[0]
        # xPosition = position[0]
        # yPosition = position[1]
        # height = position[2]
        return position

    def getNearestPosition(self):
        distance = 100
        for i in range(len(self.objects)):
            posAndOrientation = p.getBasePositionAndOrientation(self.objects[i])
            position = posAndOrientation[0]
            xPosition = position[0]
            yPosition = position[1]
            mydistance = math.sqrt(xPosition**2+yPosition**2)
            if mydistance < distance:
                distance = mydistance
        return distance

    def getTargetPosition(self):
        distance = 100
        for i in range(len(self.objects)):
            posAndOrientation = p.getBasePositionAndOrientation(self.objects[i])
            position = posAndOrientation[0]
            xPosition = position[0]
            yPosition = position[1]
            mydistance = math.sqrt(xPosition**2+yPosition**2)
            if mydistance<distance:
                distance = mydistance
        return distance