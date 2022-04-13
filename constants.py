import numpy

# -------------GENERAL-------------

simLength = 10000
numberOfGenerations = 10
populationSize = 15

# -------------FITNESS-------------
fitness = 0

# ------------AMPLITUDES------------
# ACCESS: ["upper"]["front"][0]
# FLL,FRL,BLL,BRL

# UPPER
frontUAmps = [numpy.pi / 4, numpy.pi / 4]
backUAmps = [numpy.pi / 4, numpy.pi / 4]
UAmps = {'front': frontUAmps,
         'back': backUAmps
         }
# LOWER
frontLAmps = [numpy.pi / 4, numpy.pi / 4]
backLAmps = [numpy.pi / 4, numpy.pi / 4]
LAmps = {'front': frontLAmps,
         'back': backLAmps
         }
amplitudes = {'upper': UAmps,
              'lower': LAmps
              }

# ------------FREQUENCIES------------
# ACCESS: ["upper"]["front"][0]
# FLL,FRL,BLL,BRL

# UPPER
frontUFreq = [1, 1]
backUFreq = [1, 1]
UFreq = {'front': frontUFreq,
         'back': backUFreq
         }
# LOWER
frontLFreq = [1, 1]
backLFreq = [1, 1]
LFreq = {'front': frontLFreq,
         'back': backLFreq
         }
frequencies = {'upper': UFreq,
               'lower': LFreq
               }

# --------------OFFSETS--------------
# ACCESS: ["upper"]["front"][0]
# FLL,FRL,BLL,BRL

# UPPER
frontUOffset = [1, 1]
backUOffset = [1, 1]
UOffset = {'front': frontUOffset,
           'back': backUOffset
           }
# LOWER
frontLOffset = [1, 1]
backLOffset = [1, 1]
LOffset = {'front': frontLOffset,
           'back': backLOffset
           }
offsets = {'upper': UOffset,
           'lower': LOffset
           }

# ---------JOINT MOTOR RANGE---------
motorJointRange = .9

numSensorNeurons = 4
numMotorNeurons = 8
variables = {'fitness': fitness,
             'amplitudes': amplitudes,
             'frequencies': frequencies,
             'offsets': offsets,
             'jointRange': motorJointRange
             }
# variables = [fitness, FLUAmp, FRUAmp, BLUAmp, BRUAmp, FLLAmp, FRLAmp, BLLAmp, BRLAmp, FLUFreq, FRUFreq, BLUFreq,
#              BRUFreq, FLLFreq, FRLFreq, BLLFreq, BRLFreq, FLUOffset, FRUOffset, BLUOffset, BRUOffset, FLLOffset,
#              FRLOffset, BLLOffset, BRLOffset, motorJointRange
#              ]

weights = numpy.eye(numSensorNeurons, numMotorNeurons)

saveID = 0
