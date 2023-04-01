import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
import time
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import constants as c
from simulation import SIMULATION
from time import sleep
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
toDelete = sys.argv[3]

print("to delete: " + str(toDelete))
print(type(toDelete))

simulation = SIMULATION(directOrGUI, solutionID, toDelete)
simulation.Run()



# np.save('data/backLegSensorValues.npy',backLegSensorValues)
# np.save('data/frontLegSensorValues.npy',frontLegSensorValues)
simulation.Get_Fitness()

simulation.__del__()