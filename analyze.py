import numpy
import matplotlib.pyplot as matplot

backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")
frontAngles = numpy.load("data/frontAngles.npy")
backAngles = numpy.load("data/backAngles.npy")


matplot.plot(frontAngles, label="Front Angles", linewidth=5)
matplot.plot(backAngles, label="Back Angles")


# matplot.plot(backLegSensorValues, label="Back Leg", linewidth=5)
# matplot.plot(frontLegSensorValues, label="Front Leg")

matplot.legend()
matplot.show()
