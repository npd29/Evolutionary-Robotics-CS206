
import numpy
import constants as c
from simulation import SIMULATION
import sys




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

directOrGUI = sys.argv[1]
simulation = SIMULATION(directOrGUI)
simulation.Run()
simulation.Get_Fitness()
