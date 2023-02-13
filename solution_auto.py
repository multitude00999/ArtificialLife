import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import sys
import time
import constants as c

class SOLUTION_AUTO():
	def __init__(self, myID, numLinks):
		self.numSensorNeurons, self.numMotorNeurons = numLinks, numLinks-1
		self.weights = np.random.rand(self.numSensorNeurons, self.numSensorNeurons)
		self.weights = self.weights*2 - 1
		self.myID = myID
		self.numLinks = numLinks
		self.maxCubeDim = 2
		self.minCubeDim = 0

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
		# print("fitness for", self.myID,  self.fitness)
		

	def Create_World(self):
		pyrosim.Start_SDF("world.sdf")
		# pyrosim.Send_Cube(name="Box", pos = [-5, 5, 2.5]  , size=[1, 1, 1], mass=10000)
		pyrosim.Send_Sphere(name="Ball", pos = [3,-3,0.5], size = [0.5], mass=1)
		pyrosim.End()
		while not os.path.exists("world.sdf"):
			time.sleep(0.01)

	def Generate_Body(self):
		pyrosim.Start_URDF("body.urdf")


		
		size_x, size_y, size_z = 1,1,1
		pos_x, pos_y, pos_z = 0, 0, size_z/2
		pyrosim.Send_Cube(name="0", pos = [pos_x, pos_y, pos_z]  , size=[size_x, size_y, size_z], mass = 1 )
		
		# left of origin
		for i in range(1,self.numLinks):
			if i == 1:
				pyrosim.Send_Joint( name = str(i-1) + "_" + str(i), parent= str(i-1) , child = str(i) , type = "revolute", position = [-size_x/2, pos_y, pos_z], jointAxis = "0 1 0")
				pos_y, pos_z = 0, 0
			else:
				pyrosim.Send_Joint( name = str(i-1) + "_" + str(i), parent= str(i-1) , child = str(i) , type = "revolute", position = [-size_x, pos_y, pos_z], jointAxis = "0 1 0")

			
			size_x = max(random.random()*self.maxCubeDim, self.minCubeDim)
			size_y = max(random.random()*self.maxCubeDim, self.minCubeDim)
			size_z = max(random.random()*self.maxCubeDim, self.minCubeDim)

			print(size_x, size_y, size_z)


			# subracted 0.5 from each cube z position so that there are no intial collisions with plane
			pyrosim.Send_Cube(name=str(i), pos = [-size_x/2, pos_y, pos_z+size_z/2 - 0.5]  , size=[size_x, size_y, size_z], mass = 1 )


		pyrosim.End()
		while not os.path.exists("body.urdf"):
			time.sleep(0.01)
		# exit()

	def Generate_Brain(self):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

		for i in range(self.numLinks):
			pyrosim.Send_Sensor_Neuron(name = i , linkName = str(i))

		for i in range(self.numLinks-1):
			pyrosim.Send_Motor_Neuron( name = i + self.numLinks , jointName = str(i) + "_" + str(i+1))

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

