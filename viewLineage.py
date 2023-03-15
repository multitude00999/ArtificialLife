from solution_auto_3d import SOLUTION_AUTO_3D
import constants as c
import copy
import time
import os
import pickle
import random
import sys



# # display lineage
bestCreatureExp1 = "./data/exp1/lineages/lineage_run_4_seed_224567.pkl"
with open(bestCreatureExp1, 'rb') as f:
	lineage = pickle.load(f)

print(lineage)


c.numSteps = 1000

cnt = 0
parentIdx = 6
for j in lineage[parentIdx]:
	print(" ====== branch ==== ", cnt)
	cnt+=1
	j.Start_Simulation("GUI", "1", "1", fromScratch = False)
	j.Wait_For_Simulation_To_End()
	