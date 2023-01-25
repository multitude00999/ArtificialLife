import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc  = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()
# numIters = 5
# for i in range(numIters):
# 	os.system("python3 generate.py")
# 	os.system("python3 simulate.py")