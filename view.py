from solution_auto_3d import SOLUTION_AUTO_3D
import constants as c
import copy
import time
import os
import pickle
import random
import sys

# display best creature
# with open('./data/exp0/bestCreatures/bestCreatures_run_2_seed_213623.pkl', 'rb') as f:
# 	bestCreature = pickle.load(f)

# bestCreature.Start_Simulation("GUI", "1", "1", fromScratch = False)
# bestCreature.Wait_For_Simulation_To_End() # temporary fix to remove final fitness file

# display mutations

# with open('./mutations.pkl', 'rb') as f:
# 	mutations = pickle.load(f)


# # display lineage
bestCreatureExp1 = "./data/exp1/lineages/lineage_run_3_seed_456231.pkl"
with open(bestCreatureExp1, 'rb') as f:
	lineage = pickle.load(f)

print(lineage)
# print(mutations)

# for i in lineage:
# 	print("displaying linege", i)
# 	cnt = 0
# 	for j in lineage[i]:
# 		print(" ====== branch", cnt+1)
# 		cnt+=1
# 		j.Start_Simulation("GUI", "1", "1", fromScratch = False)
# 		j.Wait_For_Simulation_To_End()


i = int(sys.argv[1])
c.numSteps = 1000

cnt = 0
# print("yo")
# for i in lineage:
for j in lineage[i]:


	print(" ====== branch ==== ", cnt+1)
	cnt+=1
	# if cnt < len(lineage[i]):
	# 	continue


	j.Start_Simulation("GUI", "1", "1", fromScratch = False)
	j.Wait_For_Simulation_To_End()
	# break
	