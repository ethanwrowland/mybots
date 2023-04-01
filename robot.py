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
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        brainFilename = "brain" + solutionID + ".nndf"
        self.nn = NEURAL_NETWORK(brainFilename)

        #f = open("robotTest.txt", "a")
       # f.write("solutionID: " + str(solutionID) + " to delete: " + str(toDelete) + "\n")
        #f.close() 

        if(toDelete == "True"):
            #f = open("robotTest.txt", "a")
            rmcall = "rm " +brainFilename
            os.system(rmcall)
            #f.write(rmcall + "\n")
            #f.close()
        self.myID = solutionID


    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
        #print(self.sensors)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, t):
        for s in self.sensors.values():
            s.Get_Value(t)

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
        stateOfLinkZero = p.getLinkState(self.robotId,0)
        #print(stateOfLinkZero)
        positionOfLinkZero = stateOfLinkZero[0]
        #print(positionOfLinkZero)
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        #print(xCoordinateOfLinkZero)

        outFileName = "tmp"+str(self.myID) + ".txt"
        f = open(outFileName, "w")
        f.write(str(xCoordinateOfLinkZero))
        osCall = "mv tmp" + str(self.myID) + ".txt fitness" + str(self.myID) + ".txt"
        os.system(osCall)
        f.close()  

        exit()



