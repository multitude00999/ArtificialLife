import numpy as np
from matplotlib import pyplot as plt

# backLegSensorValues = np.load('data/backLegSensorValues.npy')
# frontLegSensorValues = np.load('data/frontLegSensorValues.npy')
backLegSensorValues = np.load('data/motorSinSignalBackLeg.npy')
frontLegSensorValues = np.load('data/motorSinSignalFrontLeg.npy')

# motorSinSignal = np.load('data/motorSinSignal.npy')
# plt.plot(motorSinSignal)
plt.plot(backLegSensorValues, label = "Back leg sensor", linewidth = 3)
plt.plot(frontLegSensorValues, label = "Front leg sensor")
plt.legend()
plt.show()