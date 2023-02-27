import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import sys
import time
import constants as c
from link import LINK
from joint import CREATURE_JOINT

class SOLUTION_AUTO_3D():
	def __init__(self, myID, fromScratch):

		if fromScratch:
			self.numLinks = random.randint(3,5)
			self.sensor_prob = 70
			self.keepSensor = random.choices([0,1], weights = [100 - self.sensor_prob, self.sensor_prob], k=self.numLinks)
			self.numSensorNeurons = np.sum(self.keepSensor)
			if self.numSensorNeurons == 0:
				randIdx = random.randint(0,len(self.keepSensor)-1)
				self.keepSensor[randIdx] = 1
				self.numSensorNeurons +=1
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

	def Start_Simulation(self, mode, deleteBrain, deleteBody, fromScratch):
		if self.myID == 0: # generate body and world only once
			self.Create_World()
		self.Generate_Body(fromScratch)
		self.Generate_Brain()
		# exit()
		os.system("python3 simulate.py " + mode +  " " + str(self.myID) + " " + str(deleteBrain) +" "+ str(deleteBody) + " " "2&>1" + " &")
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

	def cubeTouchingTheGround(self):
		low = float('inf')
		for i in range(len(self.links)):
			if self.links[i].globalPos[2]-self.links[i].dim[2]/2 < low:
				low = self.links[i].globalPos[2]-self.links[i].dim[2]/2
		return low

	def getJointPosOnFace(self, parentCubeIdx, face):
		if face == "x_plus":
			jointX = self.links[parentCubeIdx].relPos[0] + self.links[parentCubeIdx].dim[0]/2
			jointY = self.links[parentCubeIdx].relPos[1] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[1]/2
			jointZ = self.links[parentCubeIdx].relPos[2] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[2]/2

		elif face == "x_minus":
			jointX = self.links[parentCubeIdx].relPos[0] - self.links[parentCubeIdx].dim[0]/2
			jointY = self.links[parentCubeIdx].relPos[1] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[1]/2
			jointZ = self.links[parentCubeIdx].relPos[2] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[2]/2

		elif face == "y_plus":
			jointY = self.links[parentCubeIdx].relPos[1] + self.links[parentCubeIdx].dim[1]/2
			jointX = self.links[parentCubeIdx].relPos[0] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[0]/2
			jointZ = self.links[parentCubeIdx].relPos[2] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[2]/2

		elif face == "y_minus":
			jointY = self.links[parentCubeIdx].relPos[1] - self.links[parentCubeIdx].dim[1]/2
			jointX = self.links[parentCubeIdx].relPos[0] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[0]/2
			jointZ = self.links[parentCubeIdx].relPos[2] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[2]/2

		elif face == "z_plus":
			jointZ = self.links[parentCubeIdx].relPos[2] + self.links[parentCubeIdx].dim[2]/2
			jointX = self.links[parentCubeIdx].relPos[0] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[0]/2
			jointY = self.links[parentCubeIdx].relPos[1] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[1]/2

		elif face == "z_minus":
			jointZ = self.links[parentCubeIdx].relPos[2] - self.links[parentCubeIdx].dim[2]/2
			jointX = self.links[parentCubeIdx].relPos[0] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[0]/2
			jointY = self.links[parentCubeIdx].relPos[1] + (random.random()*2 -1) *self.links[parentCubeIdx].dim[1]/2


		return [jointX, jointY, jointZ]

	def getCubePosReljoint(self, cubedim, face):
		if face == "x_plus":
			cubeX = cubedim[0]/2
			cubeY = 0
			cubeZ = 0

		elif face == "x_minus":
			cubeX =  - cubedim[0]/2
			cubeY = 0
			cubeZ = 0

		elif face == "y_plus":
			cubeY =  cubedim[1]/2
			cubeX = 0
			cubeZ = 0

		elif face == "y_minus":
			cubeY =  -cubedim[1]/2
			cubeX = 0
			cubeZ = 0

		elif face == "z_plus":
			cubeZ =  cubedim[2]/2
			cubeX = 0
			cubeY = 0

		elif face == "z_minus":
			cubeZ =  -cubedim[2]/2
			cubeX = 0
			cubeY = 0


		return [cubeX, cubeY, cubeZ]


	def Generate_Body(self, fromScratch):
		pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")


		if fromScratch:

			self.links = []
			self.joints = []
			parentCubeIdx = -1

			for i in range(self.numLinks):

				if i != 0:
					# randomly choose face
					parent_cube_idx = random.randint(0, len(self.links)-1)
					rand_face = random.choice(["x_plus", "y_plus", "z_plus", "x_minus", "y_minus", "z_minus"])

					# check if the face is occupied
					while (rand_face in self.links[parent_cube_idx].occupied_face):
						rand_face = random.choice(["x_plus", "y_plus", "z_plus", "x_minus", "y_minus", "z_minus"])
					self.links[parent_cube_idx].occupied_face.append(rand_face)
					# print("random face", rand_face)
					# randomly choose parent cube from already generated cubes
					

					# print("pci", parent_cube_idx)
					# get position on face
					jointCoords = self.getJointPosOnFace(parent_cube_idx, rand_face)

					# print("jointCoords", jointCoords)
					# randAxis = random.choice(["1 0 0", "0 0 1", "0 1 0"])
					if rand_face.startswith("x"):
						randAxis = 	"0 1 0"
					elif rand_face.startswith("y"):
						randAxis = 	"0 0 1"

					elif rand_face.startswith("z"):
						randAxis = 	"0 1 0"

					joint = CREATURE_JOINT(str(parent_cube_idx) + '_' + str(i), jointCoords, randAxis)
					joint.jointGlobalPos[0] += self.links[parent_cube_idx].globalPos[0] + joint.jointPos[0]
					joint.jointGlobalPos[1] += self.links[parent_cube_idx].globalPos[1]  + joint.jointPos[1]
					joint.jointGlobalPos[2] += self.links[parent_cube_idx].globalPos[2]  + joint.jointPos[2]

					self.joints.append(joint)

				if i == 0:
					size_x = random.uniform(self.minCubeDim, self.maxCubeXDim)
					size_y = random.uniform(self.minCubeDim, self.maxCubeYDim)
					size_z = random.uniform(self.minCubeDim, self.maxCubeXDim)
					par = LINK(str(i), None, [size_x, size_y, size_z], [0,0,0])
					par.globalPos = [0, 0, 0]
					if self.keepSensor[i]:
						par.setColor("Green", "0 1.0 0 1.0")
					self.links.append(par)
					# print(par.linkName, par.relPos , par.dim, par.mass, par.color, par.rgba)
				else:
					size_x = max(random.random()*self.maxCubeXDim, self.minCubeDim)
					size_y = max(random.random()*self.maxCubeYDim, self.minCubeDim)
					size_z = max(random.random()*self.maxCubeZDim, self.minCubeDim)
					pos = self.getCubePosReljoint([size_x, size_y, size_z], rand_face)
					par = LINK(str(i), self.links[parent_cube_idx], [size_x, size_y, size_z], pos)
					# par.globalPosX = par.relPos[0] + self.joints[i-1].jointPos[0] + par.parent.globalPos[0] 
					# par.globalPosY = par.relPos[1] + self.joints[i-1].jointPos[1] + par.parent.globalPos[1] 
					# par.globalPosZ = par.relPos[2] + self.joints[i-1].jointPos[2] + par.parent.globalPos[2] 

					par.globalPosX = par.relPos[0] + joint.jointGlobalPos[0] 
					par.globalPosY = par.relPos[1] + joint.jointGlobalPos[1]
					par.globalPosZ = par.relPos[2] + joint.jointGlobalPos[2]

					# par.globalPosX = par.relPos[0]  + par.parent.globalPos[0] 
					# par.globalPosY = par.relPos[1] + par.parent.globalPos[1] 
					# par.globalPosZ = par.relPos[2] + par.parent.globalPos[2]				
					if self.keepSensor[i]:
						par.setColor("Green", "0 1.0 0 1.0")
					self.links.append(par)


			offset = self.cubeTouchingTheGround()
			k = self.maxCubeZDim
			if offset < k:
				offset_new = k - offset
			else:
				offset_new = 0

			# remove
			for i in range(self.numLinks-1):
				self.joints[i].jointGlobalPos[2] += offset_new

			for i in range(self.numLinks):
				self.links[i].globalPos[2]+=offset_new

			self.links[0].relPos[2] += offset_new

			for i in range(self.numLinks-1):
				if self.joints[i].parentLink == "0":
					self.joints[i].jointPos[2] += offset_new


			for i in range(self.numLinks):
				curr = self.links[i]
				pyrosim.Send_Cube(name=curr.linkName, pos = curr.relPos  , size=curr.dim, mass = curr.mass, color = curr.color, rgba = curr.rgba)

			for i in range(self.numLinks-1):
				curr = self.joints[i]
				pyrosim.Send_Joint( name = curr.jointName , parent = curr.parentLink, child = curr.childLink , type = curr.type, position = curr.jointPos, jointAxis = curr.jointAxis)


			pyrosim.End()
			while not os.path.exists("body" + str(self.myID) + ".urdf"):
				time.sleep(0.01)

		else:
			for i in range(self.numLinks):
				curr = self.links[i]
				pyrosim.Send_Cube(name=curr.linkName, pos = curr.relPos  , size=curr.dim, mass = curr.mass, color = curr.color, rgba = curr.rgba)

			for i in range(self.numLinks-1):
				curr = self.joints[i]
				pyrosim.Send_Joint( name = curr.jointName , parent = curr.parentLink, child = curr.childLink , type = curr.type, position = curr.jointPos, jointAxis = curr.jointAxis)


			pyrosim.End()
			while not os.path.exists("body" + str(self.myID) + ".urdf"):
				time.sleep(0.01)

	def Generate_Brain(self):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")


		cnt = 0
		for i in range(len(self.keepSensor)):
			if self.keepSensor[i] == 1:
				pyrosim.Send_Sensor_Neuron(name = cnt , linkName = str(i))
				cnt+=1

		for i in range(self.numMotorNeurons):
			pyrosim.Send_Motor_Neuron( name = i + self.numSensorNeurons, jointName = self.joints[i].parentLink + "_" + self.joints[i].childLink)

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

