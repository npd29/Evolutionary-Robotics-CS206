
import numpy
import constants as c
from simulation import SIMULATION
import sys




# backLegSensorValues = numpy.zeros(1000)
# frontLegSensorValues = numpy.zeros(1000)
# frontAngles = numpy.zeros(1000)
# backAngles = numpy.zeros(1000)

# numpy.save("data/backLegSensorValues.npy", backLegSensorValues)
# numpy.save("data/frontLegSensorValues.npy", frontLegSensorValues)
# numpy.save("data/frontAngles.npy", frontAngles)
# numpy.save("data/backAngles.npy", backAngles)

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
c.frontAmp = float(sys.argv[3])
c.backAmp = float(sys.argv[4])
c.frontFreq = float(sys.argv[5])
c.backFreq = float(sys.argv[6])
c.frontOffset = float(sys.argv[7])
c.backOffset = float(sys.argv[8])
c.motorJointRange = float(sys.argv[9])
print(solutionID)
simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()
simulation.Get_Fitness()
