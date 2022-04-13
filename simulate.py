import constants as c
from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
varCounter = 3
for i in c.variables.keys():  # vars
    if i != 'fitness' and i != 'jointRange':
        for j in c.variables[i].keys():  # upper/lower
            for k in c.variables[i][j].keys():  # front back
                c.variables[i][j][k][0] = float(sys.argv[varCounter])
                varCounter += 1
                c.variables[i][j][k][1] = float(sys.argv[varCounter])
                varCounter += 1

c.variables['jointRange'] = float(sys.argv[varCounter])

simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()
simulation.Get_Fitness()
