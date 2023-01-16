import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import math
import random
import constants as c



physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = np.zeros(c.numSteps)
frontLegSensorValues = np.zeros(c.numSteps)

x = np.linspace(0, 2*np.pi, c.numSteps)
targetAngles_backLeg = np.sin(c.frequency_backLeg*x + c.offset_backLeg) * c.amplitude_backLeg
targetAngles_frontLeg = np.sin(c.frequency_frontLeg*x + c.offset_frontLeg) * c.amplitude_frontLeg
# with open("data/motorSinSignalFrontLeg.npy", 'wb') as f:
# 	np.save(f, targetAngles_frontLeg)

# with open("data/motorSinSignalBackLeg.npy", 'wb') as f:
# 	np.save(f, targetAngles_backLeg)
# exit()
for i in range(c.numSteps):
	p.stepSimulation()
	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
	pyrosim.Set_Motor_For_Joint( bodyIndex = robotId, jointName = b'Torso_BackLeg', controlMode = p.POSITION_CONTROL, \
								targetPosition = targetAngles_backLeg[i], \
								maxForce = 30)
	pyrosim.Set_Motor_For_Joint( bodyIndex = robotId, jointName = b'Torso_FrontLeg', controlMode = p.POSITION_CONTROL, \
								targetPosition = targetAngles_frontLeg[i], \
								maxForce = 30)

	time.sleep(c.waitTime)
	# print("step:", i)
print(backLegSensorValues)
print(frontLegSensorValues)
# with open("data/backLegSensorValues.npy", 'wb') as f:
# 	np.save(f, backLegSensorValues)

# with open("data/frontLegSensorValues.npy", 'wb') as f:
# 	np.save(f, frontLegSensorValues)
p.disconnect()
