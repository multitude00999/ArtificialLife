import pyrosim.pyrosim as pyrosim
import random

length, breadth, height = 1, 1, 1
x1, y1, z1 = -3, 3, 0.5
x2, y2, z2 = -0.5, 0, -0.5
x3, y3, z3 = 1.5, 0, 1.5
x4, y4, z4 = 0.5, 0, -0.5
def Create_World():
	pyrosim.Start_SDF("world.sdf")
	pyrosim.Send_Cube(name="Box", pos = [x1, y1, z1]  , size=[length, breadth, height])
	pyrosim.End()

def Generate_Body():
	pyrosim.Start_URDF("body.urdf")
	pyrosim.Send_Cube(name="Torso", pos = [x3, y3, z3]  , size=[length, breadth, height])
	pyrosim.Send_Cube(name="BackLeg", pos = [x4, y4, z4]  , size=[length, breadth, height])
	pyrosim.Send_Cube(name="FrontLeg", pos = [x2, y2, z2]  , size=[length, breadth, height])
	pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [2, 0, 1])
	pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [1, 0, 1])

	pyrosim.End()

def Generate_Brain():
	pyrosim.Start_NeuralNetwork("brain.nndf")
	pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
	pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
	pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
	pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
	pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

	# motion towards right
	for i in range(3):
		for j in range(3,5):
			pyrosim.Send_Synapse( sourceNeuronName = i , targetNeuronName = j , weight = random.uniform(-1,1) )
	
	pyrosim.End()

Create_World()
Generate_Body()
Generate_Brain()