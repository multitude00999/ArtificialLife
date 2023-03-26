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
	def __init__(self, myID, fromScratch, randSeed):
		self.random = random.Random(randSeed)
		self.fromScratch = fromScratch
		if fromScratch:
			self.minLinks = 3
			self.maxLinks = 5
			self.numLinks = self.random.randint(self.minLinks, self.maxLinks)
			self.sensor_prob = 50
			self.keepSensor = self.random.choices([0,1], weights = [100 - self.sensor_prob, self.sensor_prob], k=self.numLinks)
			self.numSensorNeurons = np.sum(self.keepSensor)
			self.minSensor = 1
			# atleast one sensor
			if self.numSensorNeurons == 0:
				randIdx = self.random.randint(0,len(self.keepSensor)-1)
				self.keepSensor[randIdx] = 1
				self.numSensorNeurons +=1

			# add as many motors as number of joints
			self.numMotorNeurons = self.numLinks-1

			# seed numpy
			np.random.seed(randSeed)

			# initialize brain weights
			self.weights = np.random.rand(self.numSensorNeurons, self.numMotorNeurons)
			self.weights = self.weights*2 - 1

			# unique solution Id
			self.myID = myID

			# max and min cube dim
			self.maxCubeXDim = 1
			self.maxCubeYDim = 1
			self.maxCubeZDim = 1
			self.minCubeDim = 0.2

			# probability of adding and removing a sensor
			self.addSensorProb = 0.5
			self.removeSensorProb = 0.5

			# probability of adding or removing link
			self.addLinkProb = 0.5
			self.removeLinkProb = 1 - self.addLinkProb

			# probability of mutating body and brain
			self.mutateBodyProb = 1
			self.mutateBrainProb = 1 - self.mutateBodyProb 

		# else:
		# 	self.mutateBodyProb = 0.8*self.mutateBodyProb
		# 	self.mutateBrainProb = 1 - self.mutateBodyProb
		# 	print("body mutation rate", self.mutateBodyProb)
		# 	print("brain mutation rate", self.mutateBrainProb) 

		

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
			# normalize by length
			self.length = self.getCreatureLength()
			self.fitness /= self.length

		os.system("rm " + fitnessFile)
		

	def Create_World(self):
		pyrosim.Start_SDF("world.sdf")
		# pyrosim.Send_Cube(name="Box", pos = [-5, 5, 2.5]  , size=[1, 1, 1], mass=10000)
		pyrosim.Send_Sphere(name="Ball", pos = [-10, 10,0.5], size = [0.5], mass=1)
		pyrosim.End()
		while not os.path.exists("world.sdf"):
			time.sleep(0.01)



	def cubeTouchingTheGround(self):

		# find the lowest hanging cube
		low = float('inf')
		for i in range(len(self.links)):
			if self.links[i].globalPos[2]-self.links[i].dim[2]/2 < low:
				low = self.links[i].globalPos[2]-self.links[i].dim[2]/2
		return low

	def getJointPosOnFace(self, parentCubeIdx, face):
		if face == "x_plus":
			jointX = self.links[parentCubeIdx].relPos[0] + self.links[parentCubeIdx].dim[0]/2
			jointY = self.links[parentCubeIdx].relPos[1] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[1]/2
			jointZ = self.links[parentCubeIdx].relPos[2] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[2]/2

		elif face == "x_minus":
			jointX = self.links[parentCubeIdx].relPos[0] - self.links[parentCubeIdx].dim[0]/2
			jointY = self.links[parentCubeIdx].relPos[1] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[1]/2
			jointZ = self.links[parentCubeIdx].relPos[2] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[2]/2

		elif face == "y_plus":
			jointY = self.links[parentCubeIdx].relPos[1] + self.links[parentCubeIdx].dim[1]/2
			jointX = self.links[parentCubeIdx].relPos[0] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[0]/2
			jointZ = self.links[parentCubeIdx].relPos[2] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[2]/2

		elif face == "y_minus":
			jointY = self.links[parentCubeIdx].relPos[1] - self.links[parentCubeIdx].dim[1]/2
			jointX = self.links[parentCubeIdx].relPos[0] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[0]/2
			jointZ = self.links[parentCubeIdx].relPos[2] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[2]/2

		elif face == "z_plus":
			jointZ = self.links[parentCubeIdx].relPos[2] + self.links[parentCubeIdx].dim[2]/2
			jointX = self.links[parentCubeIdx].relPos[0] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[0]/2
			jointY = self.links[parentCubeIdx].relPos[1] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[1]/2

		elif face == "z_minus":
			jointZ = self.links[parentCubeIdx].relPos[2] - self.links[parentCubeIdx].dim[2]/2
			jointX = self.links[parentCubeIdx].relPos[0] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[0]/2
			jointY = self.links[parentCubeIdx].relPos[1] + (self.random.random()*2 -1) *self.links[parentCubeIdx].dim[1]/2


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


	def checkOverlapInDim(self, dMin1, dMax1, dMin2, dMax2):
		return (dMin2 <= dMax1 and dMin2 >= dMin1) or (dMax2 <= dMax1 and dMax2 >= dMin1) or (dMin1 <= dMax2 and dMin1 >= dMin2) or (dMax1 <= dMax2 and dMax1 >= dMin2)


	def checkOverLapBetween2Cube(self, cube1, cube2):
		cube1GlobalPos = cube1.globalPos
		cube2GlobalPos = cube2.globalPos
		cube1Dim = cube1.dim
		cube2Dim = cube2.dim
		# print("cube1", cube1GlobalPos, cube1Dim)
		# print("cube2", cube2GlobalPos, cube2Dim)
		xOverlap = self.checkOverlapInDim(cube1GlobalPos[0] - cube1Dim[0]/2, cube1GlobalPos[0] + cube1Dim[0]/2, \
											cube2GlobalPos[0] - cube2Dim[0]/2, cube2GlobalPos[0] + cube2Dim[0]/2)

		yOverlap = self.checkOverlapInDim(cube1GlobalPos[1] - cube1Dim[1]/2, cube1GlobalPos[1] + cube1Dim[1]/2, \
											cube2GlobalPos[1] - cube2Dim[1]/2, cube2GlobalPos[1] + cube2Dim[1]/2)

		zOverlap = self.checkOverlapInDim(cube1GlobalPos[2] - cube1Dim[2]/2, cube1GlobalPos[2] + cube1Dim[2]/2, \
											cube2GlobalPos[2] - cube2Dim[2]/2, cube2GlobalPos[2] + cube2Dim[2]/2)

		return xOverlap and yOverlap and zOverlap


	def checkOverlap(self, currCube):

		for link in self.links:
			if self.checkOverLapBetween2Cube(currCube, link):
				return True
		return False

	def addJoint(self, i):
		parent_cube_idx = self.random.randint(0, len(self.links)-1)
		rand_face = self.random.choice(["x_plus", "y_plus", "z_plus", "x_minus", "y_minus", "z_minus"])
		self.links[parent_cube_idx].occupied_face.append(rand_face)

		# get position on face
		jointCoords = self.getJointPosOnFace(parent_cube_idx, rand_face)
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

		return joint, parent_cube_idx, rand_face

	def addLink(self, i, joint, rand_face, parent_cube_idx):
		size_x = self.random.uniform(self.minCubeDim, self.maxCubeXDim)
		size_y = self.random.uniform(self.minCubeDim, self.maxCubeYDim)
		size_z = self.random.uniform(self.minCubeDim, self.maxCubeXDim)
		pos = self.getCubePosReljoint([size_x, size_y, size_z], rand_face)

		par = LINK(str(i), self.links[parent_cube_idx], [size_x, size_y, size_z], pos)
		par.globalPos[0] = par.relPos[0] + joint.jointGlobalPos[0] 
		par.globalPos[1] = par.relPos[1] + joint.jointGlobalPos[1]
		par.globalPos[2] = par.relPos[2] + joint.jointGlobalPos[2]

		return par

	def Generate_Body(self, fromScratch):
		pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")


		if fromScratch:

			self.links = []
			self.joints = []
			parentCubeIdx = -1

			for i in range(self.numLinks):

				if i != 0:
					joint, parent_cube_idx, rand_face = self.addJoint(i)

				if i == 0:
					size_x = self.random.uniform(self.minCubeDim, self.maxCubeXDim)
					size_y = self.random.uniform(self.minCubeDim, self.maxCubeYDim)
					size_z = self.random.uniform(self.minCubeDim, self.maxCubeXDim)
					par = LINK(str(i), None, [size_x, size_y, size_z], [0,0,0])
					par.globalPos = [0, 0, 0]
					if self.keepSensor[i]:
						par.setColor("Green", "0 1.0 0 1.0")
					self.links.append(par)
					# print(par.linkName, par.relPos , par.dim, par.mass, par.color, par.rgba)
				else:
					par = self.addLink(i, joint, rand_face, parent_cube_idx)
					# print("rand face", rand_face)
					while self.checkOverlap(par):
						joint, parent_cube_idx, rand_face = self.addJoint(i)
						par = self.addLink(i, joint, rand_face, parent_cube_idx)
					self.links[parent_cube_idx].isDangling = False			
					if self.keepSensor[i]:
						par.setColor("Green", "0 1.0 0 1.0")
					self.links.append(par)
					self.joints.append(joint)


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
			for i in range(len(self.keepSensor)):
				if self.keepSensor[i]:
					self.links[i].setColor("Green", "0 1.0 0 1.0")
				else:
					self.links[i].setColor("Blue", "0 0 1.0 1.0")
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
		for i in range(len(self.links)):
			if self.keepSensor[i] == 1:
				pyrosim.Send_Sensor_Neuron(name = cnt , linkName = str(i))
				cnt+=1
		self.numMotorNeurons = self.numLinks - 1
		for i in range(self.numMotorNeurons):
			pyrosim.Send_Motor_Neuron( name = i + self.numSensorNeurons, jointName = self.joints[i].parentLink + "_" + self.joints[i].childLink)

		for currentRow in range(self.numSensorNeurons):
			for currentCol in range(self.numMotorNeurons):
				pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentCol+self.numSensorNeurons , weight = self.weights[currentRow][currentCol])
		
		pyrosim.End()
		while not os.path.exists("brain" + str(self.myID) + ".nndf"):
			time.sleep(0.01)


	def addSensorRandom(self):
		noSensorInd = []
		for i in range(len(self.keepSensor)):
			if self.keepSensor[i] == 0:
				noSensorInd.append(i)
		if len(noSensorInd) == 0:
			return False
		randInd = self.random.choices(noSensorInd)[0]
		# print(randInd)
		self.keepSensor[randInd] = 1
		
		newWeights = np.random.rand(self.numSensorNeurons + 1, self.numMotorNeurons)
		newWeights[:self.numSensorNeurons, :] = self.weights
		newWeights[self.numSensorNeurons:] = np.random.rand(1, self.numMotorNeurons)
		self.weights = newWeights
		self.numSensorNeurons += 1
		return True
		
	def removeSensorRandom(self):
		hasSensorInd = []
		for i in range(len(self.keepSensor)):
			if self.keepSensor[i] == 1:
				hasSensorInd.append(i)

		if len(hasSensorInd) < 2 : # do not remove sensor if there are less than 2 sensors
			return False
		randInd = self.random.choices(hasSensorInd)[0]
		# print(randInd)
		self.keepSensor[randInd] = 0
		
		newWeights = np.random.rand(self.numSensorNeurons - 1, self.numMotorNeurons)
		newWeights = self.weights[:self.numSensorNeurons-1, :]
		self.weights = newWeights
		self.numSensorNeurons -= 1
		return True

	def addLinkMutation(self):
		self.numLinks += 1
		i = self.numLinks - 1
		joint, parent_cube_idx, rand_face = self.addJoint(i)
		par = self.addLink(i, joint, rand_face, parent_cube_idx)
			# print("rand face", rand_face)
		while self.checkOverlap(par):
			joint, parent_cube_idx, rand_face = self.addJoint(i)
			par = self.addLink(i, joint, rand_face, parent_cube_idx)

		self.links[parent_cube_idx].isDangling = False

		newWeights = np.random.rand(self.numSensorNeurons, self.numMotorNeurons + 1)
		newWeights[:, :self.numMotorNeurons] = self.weights
		newWeights[:, self.numMotorNeurons:] = np.random.rand(self.numSensorNeurons, 1)
		self.weights = newWeights
		self.numMotorNeurons += 1

		self.keepSensor.append(self.random.randint(0,1))			
		if self.keepSensor[i]:
			par.setColor("Green", "0 1.0 0 1.0")
			newWeights = np.random.rand(self.numSensorNeurons + 1, self.numMotorNeurons)
			newWeights[:self.numSensorNeurons, :] = self.weights
			newWeights[self.numSensorNeurons:] = np.random.rand(1, self.numMotorNeurons)
			self.weights = newWeights
			self.numSensorNeurons += 1
		self.links.append(par)
		self.joints.append(joint)
		# print("link added")

	def getAllDanglingLinks(self):
		result = []
		for link in self.links:
			if link.isDangling:
				result.append(link)
		return result

	def returnIndexOfElement(self, container, val):
		for i in range(len(container)):
			if container[i] == val:
				return i
		# print("element not found")
		return -1


	def removeLinkMutation(self):
		# allDanglingLinks = self.getAllDanglingLinks()
		# choosenOne = self.random.choice(allDanglingLinks)
		# ind = self.returnIndexOfElement(self.links, choosenOne)
		ind = len(self.links)-1 # temporary fix for removing link
		choosenOne = self.links[ind]
		# print("link index", ind)
		if self.numSensorNeurons == self.minSensor:
			# don't remove it
			if self.keepSensor[ind]:
				return
		# remove link
		self.links.pop(ind)
		self.numLinks -=1

		# remove joint with the link as child
		ind_joint = -1
		for i in range(len(self.joints)):
			if self.joints[i].childLink == choosenOne.linkName:
				# print("link joint found")
				self.joints.pop(i)
				ind_joint = i
				break

		# print("before", self.weights.shape)
		# remove motor neuron from brain
		self.weights = np.delete(self.weights, ind_joint, 1)
		self.numMotorNeurons -= 1
		# print("after 1 ", self.weights.shape)

		ind_w = sum(self.keepSensor[:ind]) - 1
		# print(ind_w)
		# if link had sensor remove it from the brain
		if self.keepSensor[ind]:
			self.weights = np.delete(self.weights, ind_w, 0)
			self.numSensorNeurons -=1
		self.keepSensor.pop(ind)

		# print("link removed")
	
	def getCreatureLength(self):

		# get end points in x, y and z dir
		x_max, y_max, z_max = -float('inf'), -float('inf'), -float('inf')
		x_min, y_min, z_min = float('inf'), float('inf'), float('inf')
		for link in self.links:
			x, y, z = link.globalPos[0], link.globalPos[1], link.globalPos[2]
			x_max = max(x_max, x)
			y_max = max(y_max, y)
			z_max = max(z_max, z)

			x_min = min(x_min, x)
			y_min = min(y_min, y)
			z_min = min(z_min, z)

		x_len = x_max - x_min
		y_len = y_max - y_min
		z_len = z_max - z_min

		return max(x_len, y_len, z_len)





	def Mutate(self, mutateBodyProb, mutateBrainProb):
		self.mutateBodyProb = mutateBodyProb
		self.mutateBrainProb = mutateBrainProb
		# print(self.mutateBodyProb, self.mutateBrainProb)
		# change body
		if self.random.random() < self.mutateBodyProb:
			# print("changing body")

			if self.random.random() < self.addLinkProb and self.numLinks < self.maxLinks:
				self.addLinkMutation()
				return "link added"

			if self.random.random() < self.removeLinkProb and self.numLinks > self.minLinks:
				self.removeLinkMutation()
				return "link removed"

			# randomly add sensor to a link without sensor
			if self.random.random() < self.addSensorProb:
				self.addSensorRandom()
				# print("sensor added")
				return "sensor added"

			# randomly remove sensor from a link with sensor
			if self.random.random() < self.removeSensorProb:
				self.removeSensorRandom()
				# print("sensor removed")
				return "sensor removed"



		# change brain
		if self.random.random() < self.mutateBrainProb:
			# print("changing brain")
			randomRow = self.random.randint(0,self.weights.shape[0]-1)
			randomCol = self.random.randint(0,self.weights.shape[1]-1)
			self.weights[randomRow][randomCol] = random.random()*2 - 1
			return "brain mutated"

