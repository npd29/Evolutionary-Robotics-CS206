import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy
import random


physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robot = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robot)
backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)
frontAngles = numpy.zeros(1000)
backAngles = numpy.zeros(1000)

frontAmp = numpy.pi/4
frontFreq = 1
frontOffset = 0
backAmp = numpy.pi/4
backFreq = 1
backOffset = numpy.pi/4


for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    frontAngles[i] = frontAmp * numpy.sin(frontFreq * i/100 + frontOffset)
    backAngles[i] = backAmp * numpy.sin(backFreq * i/100 + backOffset)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robot,
        jointName="Torso_BackLeg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=backAngles[i],
        maxForce=50)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robot,
        jointName="Torso_FrontLeg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=frontAngles[i],
        maxForce=50)
    time.sleep(.0001)
numpy.save("data/backLegSensorValues.npy", backLegSensorValues)
numpy.save("data/frontLegSensorValues.npy", frontLegSensorValues)
numpy.save("data/frontAngles.npy", frontAngles)
numpy.save("data/backAngles.npy", backAngles)


p.disconnect()
