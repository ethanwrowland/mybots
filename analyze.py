import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load('data/backLegSensorValues.npy')
frontLegSensorValues = np.load('data/frontLegSensorValues.npy')

print("back: ", backLegSensorValues)
print("front: ",frontLegSensorValues)

plt.plot(backLegSensorValues)
print("check1")
plt.plot(frontLegSensorValues)
print("check2")
plt.show()


