import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:
	def __init__(self, jointName):
		self.jointName = jointName
		self.maxForce = 10
		self.Prepare_To_Act()

	def Prepare_To_Act(self):
		self.amplitude = c.amplitude
		self.frequency = c.frequency
		self.offset = c.offset
		
		if self.jointName == b'Torso_BackLeg':
			print("yo")
			self.frequency /=2
		x = np.linspace(0, 2*np.pi, c.numSteps)
		self.motorValues = np.sin(self.frequency*x + self.offset) * self.amplitude

	def Set_Value(self, robotId, t):
		pyrosim.Set_Motor_For_Joint( bodyIndex = robotId, jointName = self.jointName, controlMode = p.POSITION_CONTROL, \
										targetPosition = self.motorValues[t], \
										maxForce = self.maxForce)

	def Save_Values(self, filepath):
		with open(filepath, 'wb') as f:
			np.save(f, self.motorValues)

