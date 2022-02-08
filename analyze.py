import numpy
import matplotlib.pyplot as matplot

backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")

matplot.plot(backLegSensorValues, label="Back Leg", linewidth=5)
matplot.plot(frontLegSensorValues, label="Front Leg")

matplot.legend()
matplot.show()
