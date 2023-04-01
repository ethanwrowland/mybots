import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
import time
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c
from sensor import SENSOR
from motor import MOTOR
import os


class ROBOT:
    def __init__(self, solutionID, toDelete):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        brainFilename = "brain" + solutionID + ".nndf"
        self.nn = NEURAL_NETWORK(brainFilename)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.offGround = np.zeros(c.iterations)

        if(toDelete == "True"):
            rmcall = "rm " +brainFilename
            os.system(rmcall)
        self.myID = solutionID

        #f = open("robotTest.txt", "w")
        #f.close()
        self.solutionId = solutionID


    def Prepare_To_Sense(self):
        self.sensors = {}
        index = 0
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Sensor_Neuron(neuronName):
                self.sensors[index] = neuronName
                index += 1
        # f = open("sensorFile.txt" , "w")
        # f.write(str(self.sensors))
        # f.close

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, t):
        #f=open("robotTest.txt","a")
        miniSum = 0
        for s in self.sensors.values():
            miniSum += self.nn.Get_Value_Of(s)
            #f.write(str(self.nn.Get_Value_Of(s)) + "\t")
        
        if(miniSum == -4):
            self.offGround[t] = 1
        else:
            self.offGround[t] = -1
        
        #f.write(" miniSum: " + str(miniSum) + "\n")
        #f.close()

        #save to external file
        #np.save("offGround" + str(self.solutionId), self.offGround)
        


    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                #print(neuronName + " " +jointName+" " +str(desiredAngle))
                jointNameRevised = bytes(jointName, 'utf-8')
                self.motors[jointNameRevised].Set_Value(c.motorJointRange * desiredAngle, self.robotId)
    
    def Think(self):
        self.nn.Update()
        #self.nn.Print()
    
    def Get_Fitness(self):
        #basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        #basePosition = basePositionAndOrientation[0]
        #xPosition = basePosition[0]

        #jumping fitness function... aim to max fitness
        moreOffThanOn = np.sum(self.offGround) #between 0 and c.iterations
        longestHangTime = self.Longest_Hangtime()

        overallFitness = moreOffThanOn + c.hangTimeFactor*longestHangTime

        outFileName = "tmp"+str(self.myID) + ".txt"
        f = open(outFileName, "w")
        f.write(str(overallFitness))
        osCall = "mv tmp" + str(self.myID) + ".txt fitness" + str(self.myID) + ".txt"
        os.system(osCall)
        f.close()  

        exit()

    def Longest_Hangtime(self):
        curr = 0
        max = 0
        for t in self.offGround:
            if(t==1):
                curr += 1
            else:
                curr = 0

            if(curr > max):
                max = curr

        if(max == 0):
            max = .001
        return max


