import os
import constants as c
from deliverable1 import PHC_BEST
for i in range(c.numRuns):
    phcBest = PHC_BEST()
    phcBest.Evolve()
    phcBest.Show_Best()
