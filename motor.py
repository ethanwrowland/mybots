import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
import time
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import constants as c
class MOTOR:
    def __init__(self, jointName, amplitude, frequency, offset):
        self.jointName = jointName
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset = offset
        self.motorValues = np.zeros(c.iterations)
        for i in range(c.iterations):
            self.motorValues[i] = self.amplitude*np.sin(self.frequency * c.pi*i/(c.iterations/2) + self.offset)
    
    def Set_Value(self, t, robotId):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = self.jointName,controlMode = p.POSITION_CONTROL, targetPosition = self.motorValues[t], maxForce = c.maxForce)