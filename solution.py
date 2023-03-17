import os
import numpy as np
import pyrosim.pyrosim as pyrosim
import random

class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3,2)
        #print(self.weights)
        self.weights = self.weights * 2 - 1
        #print(self.weights)

    def Evaluate(self, dirOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py "+dirOrGUI)
       
        fitnessFile = "fitness.txt"
        f = open(fitnessFile, "r")
        self.fitness = float(f.read())
        f.close


    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name=("Box"), pos=[-10,0,.5] , size=[1,1,1])
        pyrosim.End()


    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name=("Torso"), pos=[1.5,0,1.5] , size=[1,1,1])

        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2.0,0,1.0])
        pyrosim.Send_Cube(name=("FrontLeg"), pos=[.5,0,-.5] , size=[1,1,1])

        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1.0,0,1.0])
        pyrosim.Send_Cube(name=("BackLeg"), pos=[-.5,0,-.5] , size=[1,1,1])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "BackLeg")
        pyrosim.Send_Motor_Neuron(name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_FrontLeg")

        for currRow in [0,1,2]:
            for currCol in [0,1]:
                pyrosim.Send_Synapse( sourceNeuronName = currRow , targetNeuronName = currCol + 3 , weight = self.weights[currRow][currCol])

                #print(str(currRow) + str(currCol) + str(self.weights[currRow][currCol]))

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0,2)
        randomCol = random.randint(0,1)
        self.weights[randomRow][randomCol] = random.random() * 2 - 1