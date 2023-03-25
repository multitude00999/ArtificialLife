import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import time
import random


numRuns = 10
# exp_number = 0 # evolve only brain
exp_number = 0 # coevolve both brain and body
show_random = True
show_best = True
# fix seed for reproducibiltiy
random = random.Random(123456789)
# rand_seed_list = [672557, 835812, 213623, 456231, 224567] random seeds for final project submission


for i in range(numRuns):
	print("\n\n\n ====== run " + str(i) + " =========== \n \n")

	t1 = time.time()
	rand_seed = random.randrange(1000000)
	# rand_seed = rand_seed_list[i]
	# if i <3:
	# 	print(rand_seed)
	# 	continue
	phc  = PARALLEL_HILL_CLIMBER(show_random = True, randomSeed = rand_seed, exp_number = exp_number, run_number = i)
	phc.Evolve()
	t2 = time.time()
	print("time taken", t2-t1)
	if show_best:
		phc.Show_Best()