import pybullet as p
import pybullet_data
class WORLD():
	def __init__(self, physicsClient):
		self.physicsClient = physicsClient
		self.planeId = p.loadURDF("plane.urdf")
		self.objects = p.loadSDF("world.sdf") 