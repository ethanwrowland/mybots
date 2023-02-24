import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
import time
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import constants as c
from sensor import SENSOR
from motor import MOTOR
class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
        print(self.sensors)

    def Prepare_To_Act(self):
        self.motors = {}
        i = 0
        for jointName in pyrosim.jointNamesToIndices:
            divider = 1.0/(i%2+1)
            self.motors[jointName] = MOTOR(jointName, c.amplitude, c.frequency/divider, c.offset)
            i+=1

    def Sense(self, t):
        for s in self.sensors.values():
            s.Get_Value(t)

    def Act(self, t):
        for m in self.motors.values():
            m.Set_Value(t, self.robotId)



