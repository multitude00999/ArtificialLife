import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensors import SENSOR
from motors import MOTOR
import numpy as np
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os


class ROBOT():
	def __init__(self, solutionID):
		self.sensors = {}
		self.motors = {}
		self.solutionID = solutionID
		self.robotId = p.loadURDF("body.urdf")
		self.nn = NEURAL_NETWORK("brain" + str(self.solutionID) + ".nndf")
		pyrosim.Prepare_To_Simulate(self.robotId)
		self.Prepare_To_Sense()
		self.Prepare_To_Act()
		os.system("rm " + "brain" + str(self.solutionID) + ".nndf")

	def Prepare_To_Sense(self):
		for linkName in pyrosim.linkNamesToIndices:
			self.sensors[linkName] = SENSOR(linkName)

	def Prepare_To_Act(self):
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName] = MOTOR(jointName)


	def Sense(self, t):
		for linkName in self.sensors:
			self.sensors[linkName].Get_Value(t)

	def Think(self):
		self.nn.Update()
		# self.nn.Print()

	def Act(self, t):
		for neuronName in self.nn.Get_Neuron_Names():
			if self.nn.Is_Motor_Neuron(neuronName):
				jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
				desiredAngle = c.motorJointRange * self.nn.Get_Value_Of(neuronName)
				self.motors[jointName].Set_Value(self.robotId, desiredAngle)
				# print("neuron Name:", neuronName)
				# print("joint name:", jointName)
				# print("desired Angle:",desiredAngle)
				# print()

	def Get_Fitness(self):
		stateOfLinkZero = p.getLinkState(self.robotId, 0)
		positionOfLinkZero = stateOfLinkZero[0]
		xCoordinateOfLinkZero = positionOfLinkZero[0]
		# print("x cord of link 0",xCoordinateOfLinkZero)
		fitnessFile = "tmp" + str(self.solutionID) + ".txt"
		with open(fitnessFile , 'w') as f:
			f.write(str(xCoordinateOfLinkZero))
		os.system("mv " + fitnessFile + " " + "fitness" + str(self.solutionID) + ".txt")
		# exit()



