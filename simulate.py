import pybullet as p
import time
import pybullet_data
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
numSteps = 1000
waitTime = 1/60
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
p.loadSDF("boxes.sdf")
for i in range(numSteps):
	p.stepSimulation()
	time.sleep(waitTime)
	print("step:", i)
p.disconnect()
