import constants as c
from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
c.frontAmp = float(sys.argv[3])
c.backAmp = float(sys.argv[4])
c.frontFreq = float(sys.argv[5])
c.backFreq = float(sys.argv[6])
c.frontOffset = float(sys.argv[7])
c.backOffset = float(sys.argv[8])
c.motorJointRange = float(sys.argv[9])
print("ID!!!:", solutionID)
simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()
simulation.Get_Fitness()
