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


planeId = p.loadURDF("plane.urdf")

p.loadSDF("world.sdf")
simulation = SIMULATION()

# motorControlBack = np.zeros(c.iterations)
# for i in range(c.iterations):
#     motorControlBack[i] = c.amplitudeBack*np.sin(c.frequencyBack * c.pi*i/(c.iterations/2) + c.offsetBack)

# motorControlFront = np.zeros(c.iterations)
# for i in range(c.iterations):
#     motorControlFront[i] = c.amplitudeFront*np.sin(c.frequencyFront * c.pi*i/(c.iterations/2) + c.offsetFront)


# backLegSensorValues = np.zeros(c.iterations)
# frontLegSensorValues = np.zeros(c.iterations)

# for i in range(c.iterations):
#     p.stepSimulation()

#     ####sensors
#     backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
#     frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

#     ##motors
#     pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
#     jointName = b'Torso_BackLeg',
#     controlMode = p.POSITION_CONTROL,
#     targetPosition = motorControlBack[i],
#     maxForce = 10)
#     pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
#     jointName = b'Torso_FrontLeg',
#     controlMode = p.POSITION_CONTROL,
#     targetPosition = motorControlFront[i],
#     maxForce = 10)



#     time.sleep(c.timeScale/60)

# np.save('data/backLegSensorValues.npy',backLegSensorValues)
# np.save('data/frontLegSensorValues.npy',frontLegSensorValues)

# p.disconnect()