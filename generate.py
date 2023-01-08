import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
length, breadth, height = 1, 1, 1
x1, y1, z1 = 0, 0, 0.5
# x2, y2, z2 = 1, 0, 1.5
# pyrosim.Send_Cube(name="Box", pos = [x1, y1, z1]  , size=[length, breadth, height])
# pyrosim.Send_Cube(name="Box2", pos = [x2, y2, z2]  , size=[length, breadth, height])
for i in range(5):
	for j in range(5):
		for k in range(10):
			pyrosim.Send_Cube(name="Box", pos = [x1, y1, z1]  , size=[length, breadth, height])
			z1 += 1
			length *=  0.9
			breadth *=  0.9
			height *=  0.9
		y1+=1
		z1 = 0.5
		length, breadth, height = 1, 1, 1
	x1+=1
	y1 = 0
pyrosim.End()