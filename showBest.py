import os
import constants as c
from deliverable1 import PHC_BEST

i = 1
numSaved = 1
# while os.path.exists("data/NNWeights/HiddenWeights/hiddenWeight-" + str(i)):
#     i += 1
#     numSaved += 1
c.show =True
for i in range(numSaved):
    phcBest = PHC_BEST()
    phcBest.Show_Top()
