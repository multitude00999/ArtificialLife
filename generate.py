import pyrosim.pyrosim as pyrosim

length, breadth, height = 1, 1, 1
x1, y1, z1 = -3, 3, 0.5
x2, y2, z2 = -0.5, 0, -0.5
x3, y3, z3 = 1.5, 0, 1.5
x4, y4, z4 = 0.5, 0, -0.5
def Create_World():
	pyrosim.Start_SDF("world.sdf")
	pyrosim.Send_Cube(name="Box", pos = [x1, y1, z1]  , size=[length, breadth, height])
	pyrosim.End()

def Create_Robot():
	pyrosim.Start_URDF("body.urdf")
	pyrosim.Send_Cube(name="Torso", pos = [x3, y3, z3]  , size=[length, breadth, height])
	pyrosim.Send_Cube(name="BackLeg", pos = [x4, y4, z4]  , size=[length, breadth, height])
	pyrosim.Send_Cube(name="FrontLeg", pos = [x2, y2, z2]  , size=[length, breadth, height])
	pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [2, 0, 1])
	pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [1, 0, 1])

	pyrosim.End()

Create_World()
Create_Robot()