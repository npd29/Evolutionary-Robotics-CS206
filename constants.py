import numpy

fitness = 0
saveID = 0
frontAmp = numpy.pi/4
frontFreq = 1
frontOffset = 0
backAmp = numpy.pi/4
backFreq = 1
backOffset = 0

simLength = 1000
numberOfGenerations = 10
populationSize = 10

numSensorNeurons = 4
numMotorNeurons = 8

motorJointRange = .9

variables = [fitness, frontAmp, backAmp, frontFreq, backFreq, frontOffset, backOffset, motorJointRange]

weights = numpy.eye(numSensorNeurons, numMotorNeurons)
