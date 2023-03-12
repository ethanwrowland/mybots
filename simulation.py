import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
import time
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import constants as c
from world import WORLD
from robot import ROBOT
from motor import MOTOR
from sensor import SENSOR

class SIMULATION:
    def __init__(self):
        
        self.physicsClient = p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.robot = ROBOT()
    
    def Run(self):
        for t in range(c.iterations):
            #print(i)
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)

            time.sleep(c.timeScale/60)

    def __del__(self):
        for s in self.robot.sensors.values():
            s.Save_Values()
        p.disconnect()