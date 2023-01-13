import numpy as np
from matplotlib import pyplot as plt

backLegSensorValues = np.load('data/backLegSensorValues.npy')
frontLegSensorValues = np.load('data/frontLegSensorValues.npy')
plt.plot(backLegSensorValues[:500], label = "Back leg sensor", linewidth = 3)
plt.plot(frontLegSensorValues[:500], label = "Front leg sensor")
plt.legend()
plt.show()