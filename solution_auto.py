import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import sys
import time
import constants as c

class SOLUTION_AUTO():
	def __init__(self, myID, numLinks):
		self.numLinks = numLinks
		self.keepSensor = np.random.choice([0,1], size=self.numLinks)
		self.numSensorNeurons = np.sum(self.keepSensor)
		self.numMotorNeurons = self.numLinks-1
		self.weights = np.random.rand(self.numSensorNeurons, self.numMotorNeurons)
		self.weights = self.weights*2 - 1
		self.myID = myID
		self.maxCubeXDim = 1
		self.maxCubeYDim = 1
		self.maxCubeZDim = 1
		self.minCubeDim = 0.5

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

	def Start_Simulation(self, mode, deleteBrain):
		if self.myID == 0: # generate body and world only once
			self.Create_World()
			self.Generate_Body()
		self.Generate_Brain()
		# exit()
		os.system("python3 simulate.py " + mode +  " " + str(self.myID) + " " + str(deleteBrain) +" "+ "2&>1" + " &")
		# os.system("python3 simulate.py " + mode +  " " + str(self.myID) + " &")

	def Wait_For_Simulation_To_End(self):
		fitnessFile = "fitness" + str(self.myID) + ".txt"
		while not os.path.exists(fitnessFile):
			time.sleep(0.01)

		with open(fitnessFile, 'r') as f:
			self.fitness = float(f.readlines()[0])

		os.system("rm " + fitnessFile)
		

	def Create_World(self):
		pyrosim.Start_SDF("world.sdf")
		# pyrosim.Send_Cube(name="Box", pos = [-5, 5, 2.5]  , size=[1, 1, 1], mass=10000)
		pyrosim.Send_Sphere(name="Ball", pos = [3,-3,0.5], size = [0.5], mass=1)
		pyrosim.End()
		while not os.path.exists("world.sdf"):
			time.sleep(0.01)

	def Generate_Body(self):
		pyrosim.Start_URDF("body.urdf")

		size_x = max(random.random()*self.maxCubeXDim, self.minCubeDim)
		size_y = max(random.random()*self.maxCubeYDim, self.minCubeDim)
		size_z = max(random.random()*self.maxCubeZDim, self.minCubeDim)
		if self.keepSensor[0] == 1:
			pyrosim.Send_Cube(name="0", pos = [0, 0, self.maxCubeZDim/2]  , size=[size_x, size_y, size_z], mass = size_x*size_y*size_z, color = "Green", rgba = "0 1.0 0 1.0")
		else:
			pyrosim.Send_Cube(name="0", pos = [0, 0, self.maxCubeZDim/2]  , size=[size_x, size_y, size_z], mass = size_x*size_y*size_z, color = "Blue", rgba = "0 0 1.0 1.0")
		pyrosim.Send_Joint( name = "0" + "_" + "1", parent= "0" , child = "1" , type = "revolute", position = [-size_x/2, 0, self.maxCubeZDim/2], jointAxis = "0 1 0")

		

		# left of origin
		for i in range(1,self.numLinks):
			size_x = max(random.random()*self.maxCubeXDim, self.minCubeDim)
			size_y = max(random.random()*self.maxCubeYDim, self.minCubeDim)
			size_z = max(random.random()*self.maxCubeZDim, self.minCubeDim)
			
			if self.keepSensor[i]==1:
				pyrosim.Send_Cube(name=str(i), pos = [-size_x/2, 0, 0]  , size=[size_x, size_y, size_z], mass = size_x*size_y*size_z, color = "Green", rgba = "0 1.0 0 1.0")

			else:
				pyrosim.Send_Cube(name=str(i), pos = [-size_x/2, 0, 0]  , size=[size_x, size_y, size_z], mass = size_x*size_y*size_z, color = "Blue", rgba = "0 0 1.0 1.0")


			if i != self.numLinks-1:
				pyrosim.Send_Joint( name = str(i) + "_" + str(i+1), parent= str(i) , child = str(i+1) , type = "revolute", position = [-size_x, 0, 0], jointAxis = "0 1 0")


		pyrosim.End()
		while not os.path.exists("body.urdf"):
			time.sleep(0.01)
		# exit()

	def Generate_Brain(self):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")


		cnt = 0
		for i in range(len(self.keepSensor)):
			if self.keepSensor[i] == 1:
				pyrosim.Send_Sensor_Neuron(name = cnt , linkName = str(i))
				cnt+=1

		for i in range(self.numMotorNeurons):
			pyrosim.Send_Motor_Neuron( name = i + self.numSensorNeurons, jointName = str(i) + "_" + str(i+1))

		for currentRow in range(self.numSensorNeurons):
			for currentCol in range(self.numMotorNeurons):
				pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentCol+self.numSensorNeurons , weight = self.weights[currentRow][currentCol])
		
		pyrosim.End()
		while not os.path.exists("brain" + str(self.myID) + ".nndf"):
			time.sleep(0.01)


	def Mutate(self):
		randomRow = random.randint(0,self.weights.shape[0]-1)
		randomCol = random.randint(0,self.weights.shape[1]-1)
		self.weights[randomRow][randomCol] = random.random()*2 - 1

