import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
import time
import numpy as np
import math
import random
import matplotlib.pyplot as plt

pi=math.pi
iterations = 1000 #number of iterations in the loop
timeScale = .01 #numerator in the sleep function

amplitudeBack = pi/8
frequencyBack = 20
offsetBack = 0
motorControlBack = np.zeros(iterations)
for i in range(iterations):
    motorControlBack[i] = amplitudeBack*np.sin(frequencyBack * pi*i/(iterations/2) + offsetBack)

amplitudeFront = pi/8
frequencyFront = 20
offsetFront = 0
motorControlFront = np.zeros(iterations)
for i in range(iterations):
    motorControlFront[i] = amplitudeFront*np.sin(frequencyFront * pi*i/(iterations/2) + offsetFront)


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
    targetPosition = motorControlBack[i],
    maxForce = 10)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
    jointName = b'Torso_FrontLeg',
    controlMode = p.POSITION_CONTROL,
    targetPosition = motorControlFront[i],
    maxForce = 10)



    time.sleep(timeScale/60)

np.save('data/backLegSensorValues.npy',backLegSensorValues)
np.save('data/frontLegSensorValues.npy',frontLegSensorValues)

p.disconnect()