
import numpy
import constants as c
from simulation import SIMULATION




# backLegSensorValues = numpy.zeros(1000)
# frontLegSensorValues = numpy.zeros(1000)
# frontAngles = numpy.zeros(1000)
# backAngles = numpy.zeros(1000)
#

# numpy.save("data/backLegSensorValues.npy", backLegSensorValues)
# numpy.save("data/frontLegSensorValues.npy", frontLegSensorValues)
# numpy.save("data/frontAngles.npy", frontAngles)
# numpy.save("data/backAngles.npy", backAngles)
#
#
simulation = SIMULATION()
simulation.Run()
