from solution_auto_3d import SOLUTION_AUTO_3D
import constants as c
import copy
import time
import os
import pickle
import random

# with open('./bestCreatures.pkl', 'rb') as f:
# 	bestCreature = pickle.load(f)

# bestCreature.Start_Simulation("GUI", "1", "1", fromScratch = False)
# bestCreature.Wait_For_Simulation_To_End() # temporary fix to remove final fitness file

with open('./lineage.pkl', 'rb') as f:
	lineage = pickle.load(f)

for i in lineage:
	print("displaying linege", i)
	cnt = 0
	for j in lineage[i]:
		print(" ====== branch", cnt+1)
		cnt+=1
		j.Start_Simulation("GUI", "1", "1", fromScratch = False)
		j.Wait_For_Simulation_To_End()
	