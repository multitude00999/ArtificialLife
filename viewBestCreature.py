from solution_auto_3d import SOLUTION_AUTO_3D
import constants as c
import copy
import time
import os
import pickle
import random
import sys


# display best creature
with open('./data/exp1/bestCreatures/bestCreatures_run_7_seed_851164.pkl', 'rb') as f:
	bestCreature = pickle.load(f)

bestCreature.Start_Simulation("GUI", "1", "1", fromScratch = False)
bestCreature.Wait_For_Simulation_To_End() # temporary fix to remove final fitness file

	