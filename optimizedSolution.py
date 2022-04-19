import random
import time

import numpy
import pyrosim.pyrosim as pyrosim
import os
import constants as c


class OPTOMIZED_SOLUTION:

    def __init__(self, nextAvailableID, recreateID):
        self.myID = nextAvailableID
        if recreateID > 10:
            # print("new")
            self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons)
            self.weights = self.weights * 2 - 1
        else:
            try:
                self.weights = numpy.load("data/NNWeights/weights" + str(recreateID) + ".npy")
                print("data/NNWeights/weights" + str(recreateID) + ".npy")
            except FileNotFoundError:
                self.weights = numpy.load("data/NNWeights/weights" + str(recreateID + 1) + ".npy")
                print("FILE NOT FOUND")
        c.weights = self.weights
        # print(self.weights)
        # print(c.weights)
        # print(self.Output_Vars())

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        output = self.Output_Vars()
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " " + output + " &")

    def Wait_For_Simulation_To_End(self, directOrGUI):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            # print(fitnessFileName)
            time.sleep(0.1)
        file = open(fitnessFileName, "r")
        self.fitness = float(file.read())
        file.close()
        os.system("rm " + fitnessFileName)

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-5, 5, .5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        # TORSO
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])

        # UPPER LEGS
        pyrosim.Send_Joint(name="Torso_upper-front-left", parent="Torso", child="upper-front-left", type="revolute",
                           position=[0, .5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="upper-front-left", pos=[0, .5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name="Torso_upper-back-left", parent="Torso", child="upper-back-left", type="revolute",
                           position=[0, -0.5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="upper-back-left", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name="Torso_upper-front-right", parent="Torso", child="upper-front-right", type="revolute",
                           position=[-0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="upper-front-right", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])

        pyrosim.Send_Joint(name="Torso_upper-back-right", parent="Torso", child="upper-back-right", type="revolute",
                           position=[0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="upper-back-right", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])

        # LOWER LEGS
        pyrosim.Send_Joint(name="upper-front-left_lower-front-left", parent="upper-front-left",
                           child="lower-front-left", type="revolute",
                           position=[0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="lower-front-left", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="upper-back-left_lower-back-left", parent="upper-back-left", child="lower-back-left",
                           type="revolute",
                           position=[0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="lower-back-left", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="upper-front-right_lower-front-right", parent="upper-front-right",
                           child="lower-front-right", type="revolute",
                           position=[-1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="lower-front-right", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="upper-back-right_lower-back-right", parent="upper-back-right",
                           child="lower-back-right", type="revolute",
                           position=[1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="lower-back-right", pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="lower-front-left")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="lower-back-left")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="lower-front-right")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="lower-back-right")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_upper-back-left")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_upper-front-left")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_upper-front-right")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_upper-back-right")
        pyrosim.Send_Motor_Neuron(name=8, jointName="upper-back-left_lower-back-left")
        pyrosim.Send_Motor_Neuron(name=9, jointName="upper-front-left_lower-front-left")
        pyrosim.Send_Motor_Neuron(name=10, jointName="upper-front-right_lower-front-right")
        pyrosim.Send_Motor_Neuron(name=11, jointName="upper-back-right_lower-back-right")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + c.numSensorNeurons,
                                     weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

        while not os.path.exists("brain" + str(self.myID) + ".nndf"):
            time.sleep(0.01)

    def Mutate(self):
        row = random.randint(0, 2)
        col = random.randint(0, 1)
        self.weights[row][col] = random.random() * 2 - 1
        # self.Mutate_Vars()

    def Mutate_Vars(self):
        var = random.choice(list(c.variables.keys()))  # amp, freq, offset, jointrange
        print("MUTATING VARIABLE", var)

        if var == "jointRange":
            c.variables[var] = random.random() * 5
            print(c.variables.get(var))
        elif var == "fitness":
            pass
        else:
            upperLower = random.choice(list(c.variables[var].keys()))  # upper, lower
            frontBack = random.choice(list(c.variables[var][upperLower].keys()))  # front, back
            leftRight = random.randint(0, 1)
            if var == 'amplitudes':  # amplitudes
                randNum = numpy.pi * random.random()
            elif var == 'frequencies':
                randNum = random.random() * 10
            elif var == 'offsets':
                randNum = random.random() * 10
            else:
                randNum = 0

            c.variables[var][upperLower][frontBack][leftRight] = randNum

    def Set_ID(self, newID):
        self.myID = newID

    def Set_Vars(self, FLUAmp, FRUAmp, BLUAmp, BRUAmp, FLLAmp, FRLAmp, BLLAmp, BRLAmp, FLUFreq, FRUFreq, BLUFreq,
                 BRUFreq, FLLFreq, FRLFreq, BLLFreq, BRLFreq, FLUOffset, FRUOffset, BLUOffset, BRUOffset, FLLOffset,
                 FRLOffset, BLLOffset, BRLOffset, motorJointRange):
        foo = [FLUAmp, FRUAmp, BLUAmp, BRUAmp, FLLAmp, FRLAmp, BLLAmp, BRLAmp, FLUFreq, FRUFreq, BLUFreq,
               BRUFreq, FLLFreq, FRLFreq, BLLFreq, BRLFreq, FLUOffset, FRUOffset, BLUOffset, BRUOffset, FLLOffset,
               FRLOffset, BLLOffset, BRLOffset, motorJointRange]
        varCounter = 0
        for i in c.variables.keys():  # vars
            if i != 'fitness' and i != 'jointRange':
                for j in c.variables[i].keys():  # upper/lower
                    for k in c.variables[i][j].keys():  # front back
                        c.variables[i][j][k][0] = foo[varCounter]
                        varCounter += 1
                        c.variables[i][j][k][1] = foo[varCounter]
                        varCounter += 1

        c.variables['jointRange'] = motorJointRange

    def Output_Vars(self):
        output = ""
        for i in c.variables.keys():  # vars
            if i != 'fitness' and i != 'jointRange':
                for j in c.variables[i].keys():  # upper/lower
                    for k in c.variables[i][j].keys():  # front back
                        output += str(c.variables[i][j][k][0]) + " " + str(c.variables[i][j][k][1]) + " "

        output += str(c.variables.get('jointRange'))
        return output
