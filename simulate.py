import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
numSteps = 1000
waitTime = 1/60
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = np.zeros(numSteps)
frontLegSensorValues = np.zeros(numSteps)

for i in range(numSteps):
	p.stepSimulation()
	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
	print(backLegSensorValues[i] )
	time.sleep(waitTime)
	# print("step:", i)
# print(backLegSensorValues)
# print(frontLegSensorValues)
# with open("data/backLegSensorValues.npy", 'wb') as f:
# 	np.save(f, backLegSensorValues)

# with open("data/frontLegSensorValues.npy", 'wb') as f:
# 	np.save(f, frontLegSensorValues)
# p.disconnect()
