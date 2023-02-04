import numpy as np
import matplotlib.pyplot as plt

targetAngles = np.load('data/targetAngles.npy')
plt.plot(targetAngles)
plt.show()

backLegSensorValues = np.load('data/backLegSensorValues.npy')
frontLegSensorValues = np.load('data/frontLegSensorValues.npy')

print("back: ", backLegSensorValues)
print("front: ",frontLegSensorValues)

plt.plot(backLegSensorValues, label = 'back leg', linewidth = 4)
plt.plot(frontLegSensorValues, label = 'front leg')

plt.legend()
plt.show()


