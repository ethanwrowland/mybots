import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
import time
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import constants as c
class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = np.zeros(c.iterations)
    
    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        #if(t == c.iterations-1):
            #print(self.values)

    def Save_Values(self):
        fileName = "data/"+self.linkName+"SensorValues.npy"
        np.save(fileName, self.values)