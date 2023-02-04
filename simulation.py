import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
import time
import numpy as np
import math
import random

pi=math.pi
iterations = 1000 #number of iterations in the loop
timeScale = 1 #numerator in the sleep function

targetAngles = np.zeros(1000)
print(targetAngles)
for i in range(0,1000):
    targetAngles[i] = i*(pi/500)
targetAngles = (pi/4)*np.sin(targetAngles)
print(targetAngles)
np.save('data/targetAngles.npy',targetAngles)
exit()

physicsClient = p.connect(p.GUI)

p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = planeId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = np.zeros(iterations)
frontLegSensorValues = np.zeros(iterations)

for i in range(iterations):
    p.stepSimulation()

    ####sensors
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    ##motors
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
    jointName = b'Torso_BackLeg',
    controlMode = p.POSITION_CONTROL,
    targetPosition = (pi)*random.random()-(pi/2),
    maxForce = 15)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
    jointName = b'Torso_FrontLeg',
    controlMode = p.POSITION_CONTROL,
    targetPosition = (pi)*random.random()-(pi/2),
    maxForce = 15)



    time.sleep(timeScale/60)

np.save('data/backLegSensorValues.npy',backLegSensorValues)
np.save('data/frontLegSensorValues.npy',frontLegSensorValues)

p.disconnect()