from solution_auto_3d import SOLUTION_AUTO_3D
import random

for i in range(7):
	numlinks = random.randint(5,8)
	solution = SOLUTION_AUTO_3D(0, numlinks)
	solution.Start_Simulation("GUI", "0")
	solution.Wait_For_Simulation_To_End()