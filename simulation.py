from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time

class SIMULATION:
	def __init__(self, directOrGUI):
		if directOrGUI == "DIRECT":
			self.physicsClient = p.connect(p.DIRECT)
		else:
			self.physicsClient = p.connect(p.GUI)
		p.setAdditionalSearchPath(pybullet_data.getDataPath())
		p.setGravity(0, 0, -9.8)

		self.world = WORLD(self.physicsClient)
		self.robot = ROBOT()

	def Run(self):

		for t in range(c.numSteps):
			p.stepSimulation()
			self.robot.Sense(t)
			self.robot.Think()
			self.robot.Act(t)
			time.sleep(c.waitTime)

	def Get_Fitness(self):
		self.robot.Get_Fitness()


	def __del__(self):
		p.disconnect()

