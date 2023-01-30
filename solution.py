import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import sys
import time
import warnings
# warnings.filterwarnings("ignore")

class SOLUTION():
	def __init__(self, myID):
		self.weights = np.random.rand(3,2)
		self.weights = self.weights*2 - 1
		self.myID = myID

	def Set_ID(self, myID):
		self.myID = myID

	def Evaluate(self, mode):
		self.Create_World()
		self.Generate_Body()
		self.Generate_Brain()
		os.system("python3 simulate.py " + mode +  " " + str(self.myID) + " " + "2&>1" + " &")
		fitnessFile = "fitness" + str(self.myID) + ".txt"
		while not os.path.exists(fitnessFile):
			time.sleep(0.01)
		with open(fitnessFile, 'r') as f:
			self.fitness = float(f.readlines()[0])
		# print("fitness: ", self.fitness)

	def Start_Simulation(self, mode):
		self.Create_World()
		self.Generate_Body()
		self.Generate_Brain()
		os.system("python3 simulate.py " + mode +  " " + str(self.myID) + " " + "2&>1" + " &")

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
		pyrosim.Send_Cube(name="Torso", pos = [1.5, 0, 1.5]  , size=[1, 1, 1])
		pyrosim.Send_Cube(name="BackLeg", pos = [0.5, 0, -0.5]  , size=[1, 1, 1])
		pyrosim.Send_Cube(name="FrontLeg", pos = [-0.5, 0, -0.5]  , size=[1, 1, 1])
		pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [2, 0, 1])
		pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [1, 0, 1])

		pyrosim.End()
		while not os.path.exists("body.urdf"):
			time.sleep(0.01)

	def Generate_Brain(self):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
		pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
		pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
		pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
		pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
		pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

		for currentRow in range(self.weights.shape[0]):
			for currentCol in range(self.weights.shape[1]):
				pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentCol+3 , weight = self.weights[currentRow][currentCol])
		
		pyrosim.End()
		# while not os.path.exists("brain.nndf"):
		# 	time.sleep(0.01)

	def Mutate(self):
		randomRow = random.randint(0,self.weights.shape[0]-1)
		randomCol = random.randint(0,self.weights.shape[1]-1)
		self.weights[randomRow][randomCol] = random.random()*2 - 1

