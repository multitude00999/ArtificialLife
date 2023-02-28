import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import time
import random
numRuns = 5

for i in range(numRuns):
	t1 = time.time()
	show_random = True
	rand_seed = random.randrange(1000000)
	phc  = PARALLEL_HILL_CLIMBER(show_random = False, randomSeed = rand_seed)
	phc.Evolve()
	t2 = time.time()
	print("time taken", t2-t1)
	# phc.Show_Best()