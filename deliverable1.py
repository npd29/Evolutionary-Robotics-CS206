import glob
import os

from optimizedSolution import OPTOMIZED_SOLUTION
import constants as c
import copy
import csv
import numpy
import subprocess as sp
import cv2
import pyautogui


class PHC_BEST:
    def __init__(self):
        self.generation = 1
        self.currentBest = 0
        files = glob.glob("brain*.nndf")
        for file in files:
            os.remove(file)
        files = glob.glob("fitness*.txt")
        for file in files:
            os.remove(file)
        files = glob.glob("tmp*.txt")
        for file in files:
            os.remove(file)
        self.parents = dict()
        self.nextAvailableID = 0
        # Simulate all 10 robots
        self.getFile()

    def Evolve(self):
        self.Evaluate(self.parents)
        # self.parent.Evaluate("GUI")
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
        # if self.bestFitnessFromFile < self.currentBest:
        #     for currentGeneration in range(c.numberOfGenerations):
        #         self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = dict()
        for i in self.parents.keys():
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in self.children:
            self.children[i].Mutate()

    def Select(self):
        for i in self.parents:
            if self.parents[i].fitness > self.children[i].fitness:
                self.parents[i] = self.children[i]
            elif self.parents[i].fitness < self.bestFitnessFromFile:
                self.currentBest = self.parents[i].fitness

    def Print(self):
        row = "\n" + str(self.generation)
        with open('data/fitnessData.csv', 'a') as fd:
            for i in self.parents.keys():
                print("\n", self.parents[i].fitness, self.children[i].fitness, "\n")
                row += "," + str(self.parents[i].fitness)
            fd.write(row)
        self.generation += 1
        fd.close()

    def Show_Best(self):
        bestFit = 0
        # print("FINDING BEST FIT")
        for i in range(0, c.populationSize):
            # print("i: ", str(i), self.parents[bestFit].fitness, self.parents[i].fitness)
            if self.parents[i].fitness < self.parents[bestFit].fitness:
                bestFit = i
                # print("TRUE")
        c.fitness = self.parents[bestFit].fitness
        print("FINAL FITNESS:", c.fitness)
        input("Press ENTER to show the evolved robot and save")
        self.parents[bestFit].Start_Simulation("GUI")
        # self.recordScreen()
        self.saveData(bestFit)

    def Show_Top(self):
        # print("FINDING BEST FIT")
        self.parents[0].Start_Simulation("GUI")
        self.parents[0].Wait_For_Simulation_To_End("GUI")
        print("FITNESS: ", self.parents[0].fitness)

    def Evaluate(self, solutions):
        for i in range(c.populationSize):
            solutions[i].Start_Simulation("DIRECT")
        for i in range(c.populationSize):
            solutions[i].Wait_For_Simulation_To_End("DIRECT")

    def getFile(self):
        if not c.show: #  If evolving robots
            with open('data/savedFitness.csv', newline='') as readFile:
                robotReader = csv.DictReader(readFile, delimiter=',')
                i = 0
                population = 0
                self.bestFitnessFromFile = 0
                for robot in robotReader:
                    if population < c.populationSize:
                        if population == 0:
                            self.bestFitnessFromFile = float(robot['fitness'])
                        population += 1
                        self.parents[i] = OPTOMIZED_SOLUTION(self.nextAvailableID, i + 1)
                        self.nextAvailableID += 1
                        i += 1
                while population < c.populationSize:
                    self.parents[i] = OPTOMIZED_SOLUTION(self.nextAvailableID, 11)
                    population += 1
                    self.nextAvailableID += 1
                    i += 1
        else:
            with open('data/savedFitness.csv', newline='') as readFile:
                robotReader = csv.DictReader(readFile, delimiter=',')
                i = 0
                population = 0
                self.bestFitnessFromFile = 0
                for robot in robotReader:
                    if population < c.populationSize:
                        if population == 0:
                            self.bestFitnessFromFile = float(robot['fitness'])
                        population += 1
                        self.parents[i] = OPTOMIZED_SOLUTION(self.nextAvailableID, i + 1)
                        self.nextAvailableID += 1
                        i += 1
            # for i in range(3):
            #     num = i+1
            #     self.parents[num] = OPTOMIZED_SOLUTION(self.nextAvailableID, num)
            #     self.nextAvailableID += 1

    def saveData(self, best):
        with open('data/savedFitness.csv', newline='') as readFile:
            robotReader = csv.reader(readFile, delimiter=',')
            reader = list(csv.reader(readFile))
            i = 1  # index to insert into
            pos = 0
            doNotInsert = False

            for robot in reader:
                if i != 1:  # skip the first line (headers)
                    if self.parents[best].fitness == float(robot[1]):  # check fitnesses
                        doNotInsert = True
                    if self.parents[best].fitness < float(robot[1]):  # check fitnesses
                        break  # if you find a fitness that is worse than the best fitness
                i += 1  # Get onto the next line

            i -= 1  # ok now go back because idk
            row = [i, self.parents[best].fitness]
            if not doNotInsert:
                reader.insert(i, row)

        # TODO: Something is up with this and its deleting all the date and saving nothing

        with open('data/savedFitness.csv', "w") as outfile:  # Write the updated data back into the file
            writer = csv.writer(outfile)
            # j = 0
            for line in reader:
                print(line)
                writer.writerow(line)
            # j += 1

        if i < c.numToSave and not doNotInsert:  # if it is a new fitness and in the top 10
            # temporarily save the numpy weights
            numpy.save("data/NNWeights/SensorWeights/holdSensor.npy", self.parents[best].sensorWeights)
            numpy.save("data/NNWeights/HiddenWeights/holdHidden.npy", self.parents[best].sensorWeights)
            numpy.save("data/NNWeights/MotorWeights/holdMotor.npy", self.parents[best].motorWeights)

            for num in range(c.numToSave - 1, i - 1,
                             -1):  # start at 1 less than the number to be saved and cound down to index
                sensorCommand = "mv data/NNWeights/SensorWeights/sensorWeight-" + str(
                    num) + ".npy data/NNWeights/SensorWeights/sensorWeight-" + str(num + 1) + ".npy"

                hiddenCommand = "mv data/NNWeights/HiddenWeights/hiddenWeight-" + str(
                    num) + ".npy data/NNWeights/HiddenWeights/hiddenWeight-" + str(num + 1) + ".npy"

                motorCommand = "mv data/NNWeights/MotorWeights/motorWeight-" + str(
                    num) + ".npy data/NNWeights/MotorWeights/motorWeight-" + str(num + 1) + ".npy"

                try:
                    # move each of the files after the starting index down one
                    print("Moving File", num, "to", num + 1)
                    sp.run([sensorCommand], check=True, shell=True)
                    sp.run([hiddenCommand], check=True, shell=True)
                    sp.run([motorCommand], check=True, shell=True)

                except (
                        sp.CalledProcessError,
                        FileNotFoundError) as e:  # Create the file of the next index if it doesnt exist
                    print("File " + str(num) + " not found - Creating File")
                    motorFileName = "data/NNWeights/MotorWeights/motorWeight-" + str(num + 1) + ".npy"
                    motorFile = open(motorFileName, 'w')
                    hiddenFileName = "data/NNWeights/HiddenWeights/hiddenWeight-" + str(num + 1) + ".npy"
                    hiddenFile = open(hiddenFileName, 'w')
                    sensorFileName = "data/NNWeights/SensorWeights/sensorWeight-" + str(num + 1) + ".npy"
                    sensorFile = open(sensorFileName, 'w')
                    motorFile.close()
                    sensorFile.close()
                    hiddenFile.close()

                # input("did it work?")
            # input("ready to insert holds into "+str(i))
            sensorCommand = "mv data/NNWeights/SensorWeights/holdSensor.npy data/NNWeights/SensorWeights/sensorWeight-" + str(
                i) + ".npy"
            hiddenCommand = "mv data/NNWeights/HiddenWeights/holdHidden.npy data/NNWeights/HiddenWeights/hiddenWeight-" + str(
                i) + ".npy"
            motorCommand = "mv data/NNWeights/MotorWeights/holdMotor.npy data/NNWeights/MotorWeights/motorWeight-" + str(
                i) + ".npy"
            try:
                sp.run([sensorCommand], check=True, shell=True)
                sp.run([hiddenCommand], check=True, shell=True)
                sp.run([motorCommand], check=True, shell=True)
            except (sp.CalledProcessError, FileNotFoundError) as e:
                print(e, i)
                motorFileName = "data/NNWeights/MotorWeights/motorWeight-" + str(i) + ".npy"
                motorFile = open(motorFileName, 'w')
                hiddenFileName = "data/NNWeights/HiddenWeights/hiddenWeight-" + str(i) + ".npy"
                hiddenFile = open(motorFileName, 'w')
                sensorFileName = "data/NNWeights/SensorWeights/sensorWeight-" + str(i) + ".npy"
                sensorFile = open(sensorFileName, 'w')
                motorFile.close()
                sensorFile.close()
                hiddenFile.close()

        # Save to CSV file for analysis
        with open("data/WeightData/sensorWeights.csv", newline='') as readFile:
            reader = list(csv.reader(readFile))
            line = []
            for row in range(c.numSensorNeurons):
                for col in range(c.numHiddenNeuronsOne):
                    line.append(self.parents[best].sensorWeights[row][col])
            reader.insert(i, line)

        with open('data/WeightData/sensorWeights.csv', "w") as outfile:  # Write the updated data back into the file
            writer = csv.writer(outfile)
            # j = 0
            for line in reader:
                writer.writerow(line)

        with open("data/WeightData/hiddenWeights.csv", newline='') as readFile:
            reader = list(csv.reader(readFile))
            line = []
            for row in range(c.numHiddenNeuronsOne):
                for col in range(c.numHiddenNeuronsTwo):
                    line.append(self.parents[best].hiddenWeights[row][col])
            reader.insert(i, line)

        with open('data/WeightData/hiddenWeights.csv', "w") as outfile:  # Write the updated data back into the file
            writer = csv.writer(outfile)
            # j = 0
            for line in reader:
                writer.writerow(line)

        with open("data/WeightData/motorWeights.csv", newline='') as readFile:
            reader = list(csv.reader(readFile))
            line = []
            for row in range(c.numHiddenNeuronsTwo):
                for col in range(c.numMotorNeurons):
                    line.append(self.parents[best].motorWeights[row][col])
            reader.insert(i, line)

        with open('data/WeightData/motorWeights.csv', "w") as outfile:  # Write the updated data back into the file
            writer = csv.writer(outfile)
            # j = 0
            for line in reader:
                writer.writerow(line)

    # def graphData(self):

    def recordScreen(self):
        i = 1
        while os.path.exists("data/recordings/screenRecording-" + str(i) + ".mp4"):
            # print(fitnessFileName)
            i += 1
        # Specify resolution
        resolution = (1920, 1080)

        # Specify video codec
        codec = cv2.VideoWriter_fourcc(*"mp4v")

        # Specify name of Output file
        filename = "screenRecording-" + str(i) + ".mp4"

        # Specify frames rate. We can choose
        # any value and experiment with it
        fps = 60.0

        # Creating a VideoWriter object
        out = cv2.VideoWriter(filename, codec, fps, resolution)
        timer = 0
        while True:
            # Take screenshot using PyAutoGUI
            img = pyautogui.screenshot()

            # Convert the screenshot to a numpy array
            frame = numpy.array(img)

            # Convert it from BGR(Blue, Green, Red) to
            # RGB(Red, Green, Blue)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Write it to the output file
            out.write(frame)

            # Optional: Display the recording screen
            # cv2.imshow('Live', frame)

            # Stop recording when we press 'q'
            if cv2.waitKey(0):
                break

        # Release the Video writer
        out.release()

        # Destroy all windows
        cv2.destroyAllWindows()