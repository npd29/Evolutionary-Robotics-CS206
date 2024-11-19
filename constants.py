import numpy
import math
# -------------GENERAL-------------
numRuns = 1
numToSave = 10
simLength = 1000  #600 is 50 secs
numberOfGenerations = 1000
populationSize = 25
show = False #keep this as false. will be changed automaticall by running showBest.py
#population size less than 10 will only re-simulate the top 10 robots

goal = [-10,10]
goalStartDistance = math.sqrt(goal[0]**2+goal[1]**2)
obstacleSize = 1
obstacleSizeArray = [obstacleSize,obstacleSize,obstacleSize]

# -------------FITNESS-------------
fitness = 0

# ---------JOINT MOTOR RANGE---------
motorJointRange = 1
CPG = 10
t = 0

numSensorNeurons = 9
numMotorNeurons = 8
numHiddenNeuronsOne = 4
numHiddenNeuronsTwo = 4


# variables = [fitness, FLUAmp, FRUAmp, BLUAmp, BRUAmp, FLLAmp, FRLAmp, BLLAmp, BRLAmp, FLUFreq, FRUFreq, BLUFreq,
#              BRUFreq, FLLFreq, FRLFreq, BLLFreq, BRLFreq, FLUOffset, FRUOffset, BLUOffset, BRUOffset, FLLOffset,
#              FRLOffset, BLLOffset, BRLOffset, motorJointRange
#              ]

motorWeights = numpy.eye(numHiddenNeuronsTwo, numMotorNeurons)
sensorWeights = numpy.eye(numSensorNeurons, numHiddenNeuronsOne)
hiddenWeights = numpy.eye(numHiddenNeuronsOne, numHiddenNeuronsTwo)


saveID = 0
