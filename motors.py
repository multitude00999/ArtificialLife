import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:
	def __init__(self, jointName):
		self.jointName = jointName
		self.maxForce = 30


	def Set_Value(self, robotId, desiredAngle):
		pyrosim.Set_Motor_For_Joint( bodyIndex = robotId, jointName = self.jointName, controlMode = p.POSITION_CONTROL, \
										targetPosition = desiredAngle, \
										maxForce = self.maxForce)
