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
    def __init__(self, jointName):
        self.jointName = jointName
    
    def Set_Value(self, desiredPosition, robotId):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = self.jointName,controlMode = p.POSITION_CONTROL, targetPosition = desiredPosition, maxForce = c.maxForce)