import pybullet as p
import time
physicsClient = p.connect(p.GUI)
numSteps = 1000
waitTime = 1/60
p.loadSDF("box.sdf")
for i in range(numSteps):
	p.stepSimulation()
	time.sleep(waitTime)
	print("step:", i)
p.disconnect()
