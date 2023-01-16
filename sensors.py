import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np
class SENSOR:
	def __init__(self, linkName):
		self.linkName = linkName
		self.values = np.zeros(c.numSteps)

	def Get_Value(self, t):
		self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
		# if t+1 == c.numSteps:
		# 	print(self.values)

	def Save_Values(self, filepath):
		with open(filepath, 'wb') as f:
			np.save(f, self.values)
