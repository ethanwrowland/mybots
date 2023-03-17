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
class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain.nndf")

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
                self.motors[jointNameRevised].Set_Value(desiredAngle, self.robotId)
    
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

        f = open("fitness.txt", "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()  

        exit()



