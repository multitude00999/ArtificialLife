import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import math
import random



physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
numSteps = 1000
waitTime = 1/1000
amplitude_backLeg, frequency_backLeg, offset_backLeg = np.pi/4, 10, 0 
amplitude_frontLeg, frequency_frontLeg, offset_frontLeg = np.pi/4, 50, np.pi/6
# amplitude_frontLeg, frequency_frontLeg, offset_frontLeg = np.pi/4, 10, np.pi
p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = np.zeros(numSteps)
frontLegSensorValues = np.zeros(numSteps)

x = np.linspace(0, 2*np.pi, numSteps)
targetAngles_backLeg = np.sin(frequency_backLeg*x + offset_backLeg) * amplitude_backLeg
targetAngles_frontLeg = np.sin(frequency_frontLeg*x + offset_frontLeg) * amplitude_frontLeg
# with open("data/motorSinSignalFrontLeg.npy", 'wb') as f:
# 	np.save(f, targetAngles_frontLeg)

# with open("data/motorSinSignalBackLeg.npy", 'wb') as f:
# 	np.save(f, targetAngles_backLeg)
# exit()
for i in range(numSteps):
	p.stepSimulation()
	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
	pyrosim.Set_Motor_For_Joint( bodyIndex = robotId, jointName = b'Torso_BackLeg', controlMode = p.POSITION_CONTROL, \
								targetPosition = targetAngles_backLeg[i], \
								maxForce = 30)
	pyrosim.Set_Motor_For_Joint( bodyIndex = robotId, jointName = b'Torso_FrontLeg', controlMode = p.POSITION_CONTROL, \
								targetPosition = targetAngles_frontLeg[i], \
								maxForce = 30)

	time.sleep(waitTime)
	# print("step:", i)
print(backLegSensorValues)
print(frontLegSensorValues)
# with open("data/backLegSensorValues.npy", 'wb') as f:
# 	np.save(f, backLegSensorValues)

# with open("data/frontLegSensorValues.npy", 'wb') as f:
# 	np.save(f, frontLegSensorValues)
p.disconnect()
