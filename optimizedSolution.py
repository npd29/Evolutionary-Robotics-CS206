import random
import time

import numpy
import pyrosim.pyrosim as pyrosim
import os
import constants as c


class OPTOMIZED_SOLUTION:

    def __init__(self, nextAvailableID, recreateID):
        self.myID = nextAvailableID
        if recreateID > -10:  # if its not in the top 10 then create a random robot
            self.sensorWeights = numpy.random.rand(c.numSensorNeurons, c.numHiddenNeuronsOne)
            self.motorWeights = numpy.random.rand(c.numHiddenNeuronsTwo, c.numMotorNeurons)
            self.hiddenWeights = numpy.random.rand(c.numHiddenNeuronsOne, c.numHiddenNeuronsTwo)
            self.hiddenWeights = self.hiddenWeights * 2 - 1
            self.sensorWeights = self.sensorWeights * 2 - 1
            self.motorWeights = self.motorWeights * 2 - 1
        else:  # import the brain
            try:
                print("IMPORTING", nextAvailableID, recreateID)
                self.sensorWeights = numpy.load("data/NNWeights/SensorWeights/sensorWeight-" + str(recreateID) + ".npy")
                self.hiddenWeights = numpy.load("data/NNWeights/HiddenWeights/hiddenWeight-" + str(recreateID) + ".npy")
                self.motorWeights = numpy.load("data/NNWeights/MotorWeights/motorWeight-" + str(recreateID) + ".npy")
            except ValueError:
                print("VALUE ERROR")
                self.sensorWeights = numpy.random.rand(c.numSensorNeurons, c.numHiddenNeuronsOne)
                self.motorWeights = numpy.random.rand(c.numHiddenNeuronsTwo, c.numMotorNeurons)
                self.hiddenWeights = numpy.random.rand(c.numHiddenNeuronsOne, c.numHiddenNeuronsTwo)
                self.hiddenWeights = self.hiddenWeights * 2 - 1
                self.sensorWeights = self.sensorWeights * 2 - 1
                self.motorWeights = self.motorWeights * 2 - 1
            # try:
            #     self.sensorWeights = numpy.load("data/NNWeights/SensorWeights/sensorWeight-" + str(recreateID) + ".npy")
            #     self.motorWeights = numpy.load("data/NNWeights/MotorWeights/motorWeight-" + str(recreateID) + ".npy")
            #     print(recreateID)
            #     print(self.sensorWeights)
            # except (FileNotFoundError, ValueError) as e:
            #     print("FILE NOT FOUND")
            #     self.sensorWeights = numpy.random.rand(c.numSensorNeurons, c.numHiddenNeurons)
            #     self.motorWeights = numpy.random.rand(c.numHiddenNeurons, c.numMotorNeurons)
            #     self.sensorWeights = self.sensorWeights * 2 - 1
            #     self.motorWeights = self.motorWeights * 2 - 1

        c.sensorWeights = self.sensorWeights
        c.hiddenWeights = self.hiddenWeights
        c.motorWeights = self.motorWeights

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " &")

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
        pyrosim.Send_Cube(name="goal", pos=[c.goal[0], c.goal[1], .5], size=[1, 1, 1], mass=.5)
        # randX = random.randint(1, c.goal[0]-1)
        # randY = random.randint(1, c.goal[1]-1)
        pyrosim.Send_Cube(name="obstacle", pos=[-3, 1.5, .5], size=[1,3,1], mass=50.0)
        pyrosim.Send_Cube(name="obstacle", pos=[-1.5, 2.5, .5], size=[2,1,1], mass=50.0)

        pyrosim.End()

        # obstacleArray = self.Create_Obstacles()
        # for row in range(len(obstacleArray)):
        #     for col in range(len(obstacleArray[row])):  # loop throught he whole array
        #         if obstacleArray[row][col] > 0:  # if something in occupying that cell
        #             try:
        #                 if obstacleArray[row][col-1] <= 0 and obstacleArray[row-1][col] <= 0:  # if nothing is occupying the cell to the left
        #                     size = obstacleArray[row][col]/2
        #                     position = [row-c.obstacleArraySize/2+size/2, col-c.obstacleArraySize/2+size/2, size]
        #                     name = "ball-"+str(row)+"-"+str(col)
        #                     pyrosim.Send_Sphere(name=name, pos=position, size=size, mass=1.0)
        #             except:
        #                 size = obstacleArray[row][col] / 2
        #                 position = [row - c.obstacleArraySize/2 + size / 2, col - c.obstacleArraySize/2 + size / 2, size]
        #                 name = "ball-" + str(row) + "-" + str(col)
        #                 pyrosim.Send_Sphere(name=name, pos=position, size=size, mass=1.0)



    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        # TORSO
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1], mass=1.0)

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
        pyrosim.Send_Sensor_Neuron(name=4, linkName="nearest-obstacle")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="goal")
        pyrosim.Send_Hidden_Neuron(name=6)
        pyrosim.Send_Hidden_Neuron(name=7)
        pyrosim.Send_Hidden_Neuron(name=8)
        pyrosim.Send_Hidden_Neuron(name=9)
        pyrosim.Send_Hidden_Neuron(name=10)
        pyrosim.Send_Hidden_Neuron(name=11)
        pyrosim.Send_Hidden_Neuron(name=12)
        pyrosim.Send_Hidden_Neuron(name=13)
        pyrosim.Send_Motor_Neuron(name=14, jointName="Torso_upper-back-left")
        pyrosim.Send_Motor_Neuron(name=15, jointName="Torso_upper-front-left")
        pyrosim.Send_Motor_Neuron(name=16, jointName="Torso_upper-front-right")
        pyrosim.Send_Motor_Neuron(name=17, jointName="Torso_upper-back-right")
        pyrosim.Send_Motor_Neuron(name=18, jointName="upper-back-left_lower-back-left")
        pyrosim.Send_Motor_Neuron(name=19, jointName="upper-front-left_lower-front-left")
        pyrosim.Send_Motor_Neuron(name=20, jointName="upper-front-right_lower-front-right")
        pyrosim.Send_Motor_Neuron(name=21, jointName="upper-back-right_lower-back-right")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numHiddenNeuronsOne):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + c.numSensorNeurons,
                                     weight=self.sensorWeights[currentRow][currentColumn])

        for currentRow in range(c.numHiddenNeuronsOne):
            for currentColumn in range(c.numHiddenNeuronsTwo):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow + c.numSensorNeurons,
                                     targetNeuronName=currentColumn + c.numSensorNeurons + c.numHiddenNeuronsOne,
                                     weight=self.hiddenWeights[currentRow][currentColumn])

        for currentRow in range(c.numHiddenNeuronsTwo):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow + c.numSensorNeurons + c.numHiddenNeuronsOne,
                                     targetNeuronName=currentColumn + c.numHiddenNeuronsOne + c.numSensorNeurons + c.numHiddenNeuronsTwo,
                                     weight=self.motorWeights[currentRow][currentColumn])

        pyrosim.End()

        while not os.path.exists("brain" + str(self.myID) + ".nndf"):
            time.sleep(0.01)

    def Mutate(self):
        row = random.randint(0, c.numSensorNeurons - 1)
        col = random.randint(0, c.numHiddenNeuronsOne - 1)
        self.sensorWeights[row][col] = random.random() * 2 - 1
        row = random.randint(0, c.numHiddenNeuronsOne - 1)
        col = random.randint(0, c.numHiddenNeuronsTwo - 1)
        self.hiddenWeights[row][col] = random.random() * 2 - 1
        row = random.randint(0, c.numHiddenNeuronsTwo - 1)
        col = random.randint(0, c.numMotorNeurons - 1)
        self.motorWeights[row][col] = random.random() * 2 - 1

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

    # def Set_Vars(self, FLUAmp, FRUAmp, BLUAmp, BRUAmp, FLLAmp, FRLAmp, BLLAmp, BRLAmp, FLUFreq, FRUFreq, BLUFreq,
    #              BRUFreq, FLLFreq, FRLFreq, BLLFreq, BRLFreq, FLUOffset, FRUOffset, BLUOffset, BRUOffset, FLLOffset,
    #              FRLOffset, BLLOffset, BRLOffset, motorJointRange):
    #     foo = [FLUAmp, FRUAmp, BLUAmp, BRUAmp, FLLAmp, FRLAmp, BLLAmp, BRLAmp, FLUFreq, FRUFreq, BLUFreq,
    #            BRUFreq, FLLFreq, FRLFreq, BLLFreq, BRLFreq, FLUOffset, FRUOffset, BLUOffset, BRUOffset, FLLOffset,
    #            FRLOffset, BLLOffset, BRLOffset, motorJointRange]
    #     varCounter = 0
    #     for i in c.variables.keys():  # vars
    #         if i != 'fitness' and i != 'jointRange':
    #             for j in c.variables[i].keys():  # upper/lower
    #                 for k in c.variables[i][j].keys():  # front back
    #                     c.variables[i][j][k][0] = foo[varCounter]
    #                     varCounter += 1
    #                     c.variables[i][j][k][1] = foo[varCounter]
    #                     varCounter += 1
    #
    #     c.variables['jointRange'] = motorJointRange

    def Output_Vars(self):
        output = ""
        for i in c.variables.keys():  # vars
            if i != 'fitness' and i != 'jointRange':
                for j in c.variables[i].keys():  # upper/lower
                    for k in c.variables[i][j].keys():  # front back
                        output += str(c.variables[i][j][k][0]) + " " + str(c.variables[i][j][k][1]) + " "

        output += str(c.variables.get('jointRange'))
        return output

    def Create_Obstacles(self):
        obstacleArray = []
        for row in range(c.obstacleArraySize):
            nextRow = []
            for col in range(c.obstacleArraySize):
                nextRow.append(0)  # initialize with zeros
            obstacleArray.append(nextRow)

        for i in range(5):
            for j in range(5):
                obstacleArray[int(c.obstacleArraySize/2)+i-2][int(c.obstacleArraySize/2)+j-2] = -1

        for row in range(len(obstacleArray)):
            if row % 2 == 1:  # if its a odd row
                for col in range(len(obstacleArray[row])):
                    if col % 2 == 1:  # if its an odd column
                        if obstacleArray[row][col] == 0:  # if the array square is empty
                            rand = random.randint(0, 20)  # generate a random number 0-19
                            if rand < 12:
                                randSize = 0
                            elif rand < 17:
                                randSize = 1
                            elif rand < 19: # 17,18 size 2
                                randSize = 2
                            else: # 19 is size 3
                                randSize = 3
                            for check in range(randSize + 1):  # check if anything is occupying those cells
                                try:
                                    if obstacleArray[row][col + check] != 0:
                                        randSize = 0
                                except IndexError:
                                    pass
                            if randSize == 0:
                                obstacleArray[row][col] =- 1
                            else:
                                for i in range(randSize):
                                    for j in range(randSize):
                                        try:
                                            obstacleArray[row + i][col + j] = randSize
                                            obstacleArray[row - 1][col + j] = -1  # make right side of cube blank (-1)
                                            obstacleArray[row + randSize][col + j] = -1  # make left side of cube blank (-1)
                                        except IndexError:
                                            pass
                                    try:
                                        obstacleArray[row + i][col + randSize] = -1  # make right side of cube blank (-1)
                                        obstacleArray[row + i][col - 1] = -1  # make left side of cube blank (-1)
                                    except IndexError:
                                        pass
                                try:
                                    obstacleArray[row - 1][col - 1] = -1
                                    obstacleArray[row - 1][col + randSize] = -1
                                    obstacleArray[row + randSize][col - 1] = -1
                                    obstacleArray[row + randSize][col + randSize] = -1
                                except:
                                    pass
        return obstacleArray
        # with open('data/obstacleArray.csv', 'w') as fd:
        #     outRow = "\n"
        #     for r in range(len(obstacleArray)):
        #         for c in range(len(obstacleArray[r])):
        #             outRow += str(obstacleArray[r][c]) + ","
        #
        #         fd.write(outRow.rstrip(','))
        #         outRow = '\n'
        # fd.close()


