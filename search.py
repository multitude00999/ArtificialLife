import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import time

t1 = time.time()
phc  = PARALLEL_HILL_CLIMBER()
phc.Evolve()
t2 = time.time()
print("time taken", t2-t1)
phc.Show_Best()