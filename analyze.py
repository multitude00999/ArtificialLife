import numpy as np
from matplotlib import pyplot as plt
import pickle
# backLegSensorValues = np.load('data/backLegSensorValues.npy')
# frontLegSensorValues = np.load('data/frontLegSensorValues.npy')
# backLegSensorValues = np.load('data/motorSinSignalBackLeg.npy')
# frontLegSensorValues = np.load('data/motorSinSignalFrontLeg.npy')

with open('best_creature_fitness_vals.pkl', 'rb') as f:
	bestCreatureValues = pickle.load(f)

plt.plot(bestCreatureValues, label = "best creature fitness", linewidth = 3)
# motorSinSignal = np.load('data/motorSinSignal.npy')
# plt.plot(motorSinSignal)
# plt.plot(backLegSensorValues, label = "Back leg sensor", linewidth = 3)
# plt.plot(frontLegSensorValues, label = "Front leg sensor")
plt.legend()
plt.show()