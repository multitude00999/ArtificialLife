import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensors import SENSOR
from motors import MOTOR
import numpy as np
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os


class ROBOT():
	def __init__(self, solutionID, objects, deleteBrain, deleteBody):
		self.sensors = {}
		self.motors = {}
		self.solutionID = solutionID
		self.robotId = p.loadURDF("body" + str(self.solutionID) + ".urdf")
		self.objects = objects
		self.nn = NEURAL_NETWORK("brain" + str(self.solutionID) + ".nndf")
		pyrosim.Prepare_To_Simulate(self.robotId)
		self.Prepare_To_Sense()
		self.Prepare_To_Act()
		if deleteBrain == "1":
			os.system("rm " + "brain" + str(self.solutionID) + ".nndf")
		else:
			os.system("mv " + "brain" + str(self.solutionID) + ".nndf" + " brainBest.nndf")

		if deleteBody == "1":
			os.system("rm " + "body" + str(self.solutionID) + ".urdf")

		else:
			os.system("mv " + "body" + str(self.solutionID) + ".nndf" + " bodyBest.nndf")

	def Prepare(self):
		pyrosim.Prepare_To_Simulate(self.robotId)

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
		# stateOfLinkZero = p.getLinkState(self.robotId, 0)
		# positionOfLinkZero = stateOfLinkZero[0]
		# xCoordinateOfLinkZero = positionOfLinkZero[0]
		basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
		basePosition = basePositionAndOrientation[0]
		xPositionRobot = basePosition[0]
		yPositionRobot = basePosition[1]
		zPositionRobot = basePosition[2]
		# print(xPosition, yPosition)
		posAndOrientation = p.getBasePositionAndOrientation(self.objects[0])
		position = posAndOrientation[0]
		xPositionTarget = position[0]
		yPositionTarget = position[1]
		zPositionTarget = position[2]
		# print("ball", xPositionTarget, yPositionTarget, zPositionTarget)
		# print("bot", xPositionRobot, yPositionRobot, zPositionRobot)
		dist = np.sqrt((xPositionTarget-xPositionRobot)**2 + (yPositionTarget-yPositionRobot)**2 + (zPositionTarget-zPositionRobot)**2)
		# dist = xCoordinateOfLinkZero
		
		# print("x cord of link 0",xCoordinateOfLinkZero)
		# print(dist)
		fitnessFile = "tmp" + str(self.solutionID) + ".txt"
		with open(fitnessFile , 'w') as f:
			f.write(str(dist))
		os.system("mv " + fitnessFile + " " + "fitness" + str(self.solutionID) + ".txt")
		# exit()



