import os
from hillclimber import HILL_CLIMBER

hc  = HILL_CLIMBER()
hc.Evolve()
hc.Show_Best()
# numIters = 5
# for i in range(numIters):
# 	os.system("python3 generate.py")
# 	os.system("python3 simulate.py")