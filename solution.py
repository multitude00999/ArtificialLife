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

	def Start_Simulation(self, mode, deleteBrain):
		if self.myID == 0: # generate body and world only once
			self.Create_World()
			self.Generate_Body()
		self.Generate_Brain()
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
		pyrosim.Send_Cube(name="Torso", pos = [0, 0, 1]  , size=[1.5, 0.5, 0.5], mass = 1 )
		pyrosim.Send_Cube(name="FrontLeftLeg", pos = [0, 0, -0.25]  , size=[0.2, 0.2, 0.5], mass=0.3)
		pyrosim.Send_Cube(name="FrontRightLeg", pos = [0, 0, -0.25]  , size=[0.2, 0.2, 0.5], mass=0.3)
		pyrosim.Send_Cube(name="BackLeftLeg", pos = [0, 0, -0.25]  , size=[0.2, 0.2, 0.5], mass=0.3)
		pyrosim.Send_Cube(name="BackRightLeg", pos = [0, 0, -0.25]  , size=[0.2, 0.2, 0.5],mass=0.3)

		pyrosim.Send_Cube(name="FrontLowerLeftLeg", pos = [0, 0, -0.25]  , size=[0.1, 0.1, 0.5],mass=0.1)
		pyrosim.Send_Cube(name="FrontLowerRightLeg", pos = [0, 0, -0.25]  , size=[0.1, 0.1, 0.5],mass=0.1)
		pyrosim.Send_Cube(name="BackLowerLeftLeg", pos = [0, 0, -0.25]  , size=[0.1, 0.1, 0.5],mass=0.1)
		pyrosim.Send_Cube(name="BackLowerRightLeg", pos = [0, 0, -0.25]  , size=[0.1, 0.1, 0.5],mass=0.1)



		# pyrosim.Send_Cube(name="LeftLeg", pos = [-0.5, 0, 0]  , size=[1, 0.2, 0.2])
		# pyrosim.Send_Cube(name="RightLeg", pos = [0.5, 0, 0]  , size=[1, 0.2, 0.2])
		# pyrosim.Send_Cube(name="FrontLowerLeg", pos = [0, 0, -0.5]  , size=[0.2, 0.2, 1])
		# pyrosim.Send_Cube(name="BackLowerLeg", pos = [0, 0, -0.5]  , size=[0.2, 0.2, 1])
		# pyrosim.Send_Cube(name="LeftLowerLeg", pos = [0, 0, -0.5]  , size=[0.2, 0.2, 1])
		# pyrosim.Send_Cube(name="RightLowerLeg", pos = [0, 0, -0.5]  , size=[0.2, 0.2, 1])


		pyrosim.Send_Joint( name = "Torso_FrontLeftLeg" , parent= "Torso" , child = "FrontLeftLeg" , type = "revolute", position = [-0.75, -0.25, 1], jointAxis = "0 1 0")
		pyrosim.Send_Joint( name = "Torso_FrontRightLeg" , parent= "Torso" , child = "FrontRightLeg" , type = "revolute", position = [-0.75, 0.25, 1], jointAxis = "0 1 0")
		pyrosim.Send_Joint( name = "Torso_BackLeftLeg" , parent= "Torso" , child = "BackLeftLeg" , type = "revolute", position = [0.75, -0.25, 1], jointAxis = "0 1 0")
		pyrosim.Send_Joint( name = "Torso_BackRightLeg" , parent= "Torso" , child = "BackRightLeg" , type = "revolute", position = [0.75, 0.25, 1], jointAxis = "0 1 0")
		
		pyrosim.Send_Joint( name = "FrontLeftLeg_FrontLowerLeftLeg" , parent= "FrontLeftLeg" , child = "FrontLowerLeftLeg" , type = "revolute", position = [0, 0, -0.5], jointAxis = "0 1 0")
		pyrosim.Send_Joint( name = "FrontRightLeg_FrontLowerRightLeg" , parent= "FrontRightLeg" , child = "FrontLowerRightLeg" , type = "revolute", position = [0, 0, -0.5], jointAxis = "0 1 0")
		pyrosim.Send_Joint( name = "BackLeftLeg_BackLowerLeftLeg" , parent= "BackLeftLeg" , child = "BackLowerLeftLeg" , type = "revolute", position = [0, 0, -0.5], jointAxis = "0 1 0")
		pyrosim.Send_Joint( name = "BackRightLeg_BackLowerRightLeg" , parent= "BackRightLeg" , child = "BackLowerRightLeg" , type = "revolute", position = [0, 0, -0.5], jointAxis = "0 1 0")




		pyrosim.End()
		while not os.path.exists("body.urdf"):
			time.sleep(0.01)
		# exit()

	def Generate_Brain(self):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
		pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
		pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLowerLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLowerRightLeg")
		pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "BackLowerLeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "BackLowerRightLeg")


		pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Torso_FrontLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Torso_FrontRightLeg")
		pyrosim.Send_Motor_Neuron( name = 7 , jointName = "Torso_BackLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 8 , jointName = "Torso_BackRightLeg")

		pyrosim.Send_Motor_Neuron( name = 9 , jointName = "FrontLeftLeg_FrontLowerLeftLeg")
		pyrosim.Send_Motor_Neuron( name = 10 , jointName = "FrontRightLeg_FrontLowerRightLeg")
		pyrosim.Send_Motor_Neuron( name = 11 , jointName = "BackLeftLeg_BackLowerLeftLeg")
		pyrosim.Send_Motor_Neuron( name =12 , jointName = "BackRightLeg_BackLowerRightLeg")

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

