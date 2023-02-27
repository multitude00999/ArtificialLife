import numpy as np
from matplotlib import pyplot as plt
import pickle
import os
# backLegSensorValues = np.load('data/backLegSensorValues.npy')
# frontLegSensorValues = np.load('data/frontLegSensorValues.npy')
# backLegSensorValues = np.load('data/motorSinSignalBackLeg.npy')
# frontLegSensorValues = np.load('data/motorSinSignalFrontLeg.npy')

# with open('bestCreatureFitnessVals_109658.pkl', 'rb') as f:
# 	bestCreatureValues_1 = pickle.load(f)

# with open('bestCreatureFitnessVals_231579.pkl', 'rb') as f:
# 	bestCreatureValues_2 = pickle.load(f)

# with open('bestCreatureFitnessVals_761607.pkl', 'rb') as f:
# 	bestCreatureValues_3 = pickle.load(f)

# with open('bestCreatureFitnessVals_861953.pkl', 'rb') as f:
# 	bestCreatureValues_4 = pickle.load(f)

# with open('bestCreatureFitnessVals_579397.pkl', 'rb') as f:
# 	bestCreatureValues_5 = pickle.load(f)

# plt.plot(bestCreatureValues_1, label = "best creature fitness 1", linewidth = 3)
# plt.plot(bestCreatureValues_2, label = "best creature fitness 2", linewidth = 3)
# plt.plot(bestCreatureValues_3, label = "best creature fitness 3", linewidth = 3)
# plt.plot(bestCreatureValues_4, label = "best creature fitness 4", linewidth = 3)
# plt.plot(bestCreatureValues_5, label = "best creature fitness 5", linewidth = 3)
# motorSinSignal = np.load('data/motorSinSignal.npy')
# plt.plot(motorSinSignal)
# plt.plot(backLegSensorValues, label = "Back leg sensor", linewidth = 3)
# plt.plot(frontLegSensorValues, label = "Front leg sensor")

def read_data(filename):
	with open(filename, 'rb') as f:
		bestCreatureValues = pickle.load(f)

	return bestCreatureValues
filelist = os.listdir('./bestFitnessVals')

i = 0
for file in filelist:
	bestCreatureValues = read_data('./bestFitnessVals/' + file)
	plt.plot(bestCreatureValues, label = "best creature fitness " + str(i), linewidth = 3)
	i+=1 
plt.legend()
plt.show()