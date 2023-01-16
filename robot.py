import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensors import SENSOR
from motors import MOTOR
import numpy as np
import constants as c

class ROBOT():
	def __init__(self):
		self.sensors = {}
		self.motors = {}
		self.robotId = p.loadURDF("body.urdf")
		pyrosim.Prepare_To_Simulate(self.robotId)
		self.Prepare_To_Sense()
		self.Prepare_To_Act()

	def Prepare_To_Sense(self):
		for linkName in pyrosim.linkNamesToIndices:
			self.sensors[linkName] = SENSOR(linkName)

	def Prepare_To_Act(self):
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName] = MOTOR(jointName)


	def Sense(self, t):
		for linkName in self.sensors:
			self.sensors[linkName].Get_Value(t)

	def Act(self, t):
		for jointName in self.motors:
			self.motors[jointName].Set_Value(self.robotId, t)

