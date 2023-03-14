from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time

class SIMULATION:
	def __init__(self, directOrGUI, solutionID, deleteBrain, deleteBody):
		self.directOrGUI = directOrGUI
		self.solutionID = solutionID
		self.deleteBrain = deleteBrain
		self.deleteBody = deleteBody
		if self.directOrGUI == "DIRECT":
			self.physicsClient = p.connect(p.DIRECT)
		else:
			self.physicsClient = p.connect(p.GUI)
			p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
		p.setAdditionalSearchPath(pybullet_data.getDataPath())
		p.setGravity(0, 0, -9.8)

		self.world = WORLD(self.physicsClient)
		self.robot = ROBOT(self.solutionID, self.world.objects, self.deleteBrain, self.deleteBody)

	def Run(self):
		for t in range(c.numSteps):
			p.stepSimulation()
			self.robot.Prepare()
			self.robot.Sense(t)
			self.robot.Think()
			self.robot.Act(t)
			
			if self.directOrGUI == "GUI":
				basePos, baseOrn = p.getBasePositionAndOrientation(self.robot.robotId) # Get model position
				p.resetDebugVisualizerCamera( cameraDistance = 5, cameraYaw=75, cameraPitch=-20, cameraTargetPosition=basePos) # fix camera onto model
				time.sleep(c.waitTime)
			# if t%100 ==0:
			# 	print("step:", t)

	def Get_Fitness(self):
		self.robot.Get_Fitness()


	def __del__(self):
		p.disconnect()

