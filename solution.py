import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import sys
import time
import constants as c

class SOLUTION():
	def __init__(self, myID):
		self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
		self.weights = self.weights*2 - 1
		self.myID = myID

	def Set_ID(self, myID):
		self.myID = myID

	def Evaluate(self, mode):
		self.Create_World()
		self.Generate_Body()
		self.Generate_Brain()
		os.system("python3 simulate.py " + mode +  " " + str(self.myID) + " " + "2&>1" + " &")
		# os.system("python3 simulate.py " + mode +  " " + str(self.myID) + " &")
		fitnessFile = "fitness" + str(self.myID) + ".txt"
		while not os.path.exists(fitnessFile):
			time.sleep(0.01)
		with open(fitnessFile, 'r') as f:
			self.fitness = float(f.readlines()[0])
		# print("fitness: ", self.fitness)

	def Start_Simulation(self, mode):
		if self.myID == 0: # generate body and world only once
			self.Create_World()
			self.Generate_Body()
		self.Generate_Brain()
		os.system("python3 simulate.py " + mode +  " " + str(self.myID) + " " + "2&>1" + " &")
		# os.system("python3 simulate.py " + mode +  " " + str(self.myID) + " &")

	def Wait_For_Simulation_To_End(self):
		fitnessFile = "fitness" + str(self.myID) + ".txt"
		while not os.path.exists(fitnessFile):
			time.sleep(0.01)

		with open(fitnessFile, 'r') as f:
			self.fitness = float(f.readlines()[0])

		os.system("rm " + fitnessFile)
		# print("fitness for", self.myID,  self.fitness)
		

	def Create_World(self):
		pyrosim.Start_SDF("world.sdf")
		pyrosim.Send_Cube(name="Box", pos = [-3, 3, 0.5]  , size=[1, 1, 1])
		pyrosim.End()
		while not os.path.exists("world.sdf"):
			time.sleep(0.01)

	def Generate_Body(self):
		pyrosim.Start_URDF("body.urdf")
		pyrosim.Send_Cube(name="Torso", pos = [0, 0, 1]  , size=[1, 1, 1])
		pyrosim.Send_Cube(name="FrontLeg", pos = [0, -0.5, 0]  , size=[0.2, 1, 0.2])
		pyrosim.Send_Cube(name="BackLeg", pos = [0, 0.5, 0]  , size=[0.2, 1, 0.2])
		pyrosim.Send_Cube(name="LeftLeg", pos = [-0.5, 0, 0]  , size=[1, 0.2, 0.2])
		pyrosim.Send_Cube(name="RightLeg", pos = [0.5, 0, 0]  , size=[1, 0.2, 0.2])
		pyrosim.Send_Cube(name="FrontLowerLeg", pos = [0, 0, -0.5]  , size=[0.2, 0.2, 1])
		pyrosim.Send_Cube(name="BackLowerLeg", pos = [0, 0, -0.5]  , size=[0.2, 0.2, 1])
		pyrosim.Send_Cube(name="LeftLowerLeg", pos = [0, 0, -0.5]  , size=[0.2, 0.2, 1])
		pyrosim.Send_Cube(name="RightLowerLeg", pos = [0, 0, -0.5]  , size=[0.2, 0.2, 1])


		pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0, -0.5, 1], jointAxis = "1 0 0")
		pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0, 0.5, 1], jointAxis = "1 0 0")
		pyrosim.Send_Joint( name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5, 0, 1], jointAxis = "0 1 0")
		pyrosim.Send_Joint( name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5, 0, 1], jointAxis = "0 1 0")
		pyrosim.Send_Joint( name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", position = [0, -1, 0], jointAxis = "1 0 0")
		pyrosim.Send_Joint( name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [0, 1, 0], jointAxis = "1 0 0")
		pyrosim.Send_Joint( name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", position = [-1, 0, 0], jointAxis = "0 1 0")
		pyrosim.Send_Joint( name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [1, 0, 0], jointAxis = "0 1 0")


		pyrosim.End()
		while not os.path.exists("body.urdf"):
			time.sleep(0.01)
		# exit()

	def Generate_Brain(self):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
		# pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
		# pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
		# pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
		# pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
		# pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")

		pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "FrontLowerLeg")
		pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLowerLeg")
		pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LeftLowerLeg")
		pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "RightLowerLeg")

		pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_BackLeg")
		pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Torso_FrontLeg")
		pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Torso_LeftLeg")
		pyrosim.Send_Motor_Neuron( name = 7 , jointName = "Torso_RightLeg")
		pyrosim.Send_Motor_Neuron( name = 8 , jointName = "FrontLeg_FrontLowerLeg")
		pyrosim.Send_Motor_Neuron( name = 9 , jointName = "BackLeg_BackLowerLeg")
		pyrosim.Send_Motor_Neuron( name = 10 , jointName = "LeftLeg_LeftLowerLeg")
		pyrosim.Send_Motor_Neuron( name = 11 , jointName = "RightLeg_RightLowerLeg")

		for currentRow in range(c.numSensorNeurons):
			for currentCol in range(c.numMotorNeurons):
				pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentCol+c.numSensorNeurons , weight = self.weights[currentRow][currentCol])
		
		pyrosim.End()
		while not os.path.exists("brain" + str(self.myID) + ".nndf"):
			time.sleep(0.01)


	def Mutate(self):
		randomRow = random.randint(0,self.weights.shape[0]-1)
		randomCol = random.randint(0,self.weights.shape[1]-1)
		self.weights[randomRow][randomCol] = random.random()*2 - 1

