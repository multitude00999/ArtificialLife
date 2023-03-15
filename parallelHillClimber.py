from solution_auto_3d import SOLUTION_AUTO_3D
import constants as c
import copy
import time
import os
import pickle
import random
from collections import defaultdict

class PARALLEL_HILL_CLIMBER():
	def __init__(self, show_random, randomSeed, exp_number, run_number):
		for file in os.listdir("."):
			if file.startswith("brain") or file.startswith("fitness") or file.startswith("body"):
				os.system("rm {}".format(file))

		self.parents = {}
		self.run_number = run_number
		self.exp_number = exp_number
		self.mutations = {}
		self.randomSeed = randomSeed
		self.showRandom = show_random
		self.random = random.Random(self.randomSeed)
		self.nextAvailableID = 0
		self.best_creature_fitness = []
		self.averageFitnessVals = []

		if self.exp_number == 0: # evolve only brain
			self.bodyMutationRate = 0
			self.brainMutationRate = 1

		else:
			self.bodyMutationRate = 1
			self.brainMutationRate = 1 - self.bodyMutationRate

		self.lineage = {}
		self.mutations = {}
		for i in range(c.populationSize):
			randomSeed = self.random.randrange(1000000)
			self.parents[i] = SOLUTION_AUTO_3D(self.nextAvailableID, fromScratch = True, randSeed = randomSeed)
			self.nextAvailableID+=1
			self.lineage[i] = []
			self.mutations[i] = []
			self.lineage[i].append(self.parents[i])

	def Evolve(self):
		self.Evaluate(self.parents, fromScratch = True)
		if self.showRandom:
			self.show_random()
		self.get_best_creature_fitness()
		for currentGeneration in range(c.numberOfGenerations):
			print("====== generation ", currentGeneration , " ================ ")
			self.Evolve_For_One_Generation()
			if self.bodyMutationRate > 0.3:
				self.bodyMutationRate = 0.9*self.bodyMutationRate
				self.brainMutationRate = 1 - self.bodyMutationRate

			self.get_best_creature_fitness()
			self.get_average_fitness()

	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children, fromScratch = False)
		# self.Print()
		self.Select()
		# self.show_random_child()

	def Spawn(self):
		self.children = {}
		for parent in self.parents:
			self.children[parent] = copy.deepcopy(self.parents[parent])
			self.children[parent].fromScratch = False
			# self.children[parent].__init__(self.nextAvailableID, fromScratch = False, randSeed = self.random.randrange(1000000))
			self.children[parent].random = random.Random(self.random.randrange(1000000))
			self.children[parent].Set_ID(self.nextAvailableID)
			self.nextAvailableID+=1

	def Mutate(self):
		
		for child in self.children:
			mutation = self.children[child].Mutate(self.bodyMutationRate, self.brainMutationRate)
			self.mutations[child].append(mutation)

	def Evaluate(self, solutions, fromScratch):
		for i in range(c.populationSize):
			solutions[i].Start_Simulation("DIRECT", "1", "1", fromScratch)


		for i in range(c.populationSize):
			solutions[i].Wait_For_Simulation_To_End()


	def Select(self):
		for parent in self.parents:
			if self.parents[parent].fitness > self.children[parent].fitness:
				self.parents[parent] = copy.deepcopy(self.children[parent])
				self.lineage[parent].append(self.parents[parent])
			else:
				self.mutations[parent].pop(-1)

	def Show_Best(self):
		best_parent = 0
		best_fitness = float('inf')
		for parent in self.parents:
			if best_fitness > self.parents[parent].fitness:
				best_parent = parent
				best_fitness = self.parents[parent].fitness
		self.saveCreature(best_parent)
		print("best parent:", best_parent, "fitness:", best_fitness)

		self.parents[best_parent].Start_Simulation("GUI", "1", "1", fromScratch = False)
		self.parents[best_parent].Wait_For_Simulation_To_End() # temporary fix to remove final fitness file

	def get_best_creature_fitness(self):
		best_parent = 0
		best_fitness = float('inf')
		for parent in self.parents:
			if best_fitness > self.parents[parent].fitness:
				best_parent = parent
				best_fitness = self.parents[parent].fitness
		self.best_creature_fitness.append(best_fitness)

	def get_average_fitness(self):
		fitness_list = []
		for parent in self.parents:
			fitness_list.append(self.parents[parent].fitness)
		# std = np.std(fitness_list)
		self.averageFitnessVals.append(sum(fitness_list)/len(fitness_list))



	def show_random(self):
		self.parents[0].Start_Simulation("GUI", "1", "1", fromScratch = False)
		self.parents[0].Wait_For_Simulation_To_End()

	def show_random_child(self):
		self.children[0].Start_Simulation("GUI", "1", "1", fromScratch = False)
		self.children[0].Wait_For_Simulation_To_End()


	def saveCreature(self, i):
		# with open('./bestCreatures/' + str(self.parents[i].myID) + "_" + str(self.randomSeed) + ".pkl", 'wb') as f:
		filename = "./data/exp" + str(self.exp_number) + "/bestCreatures/bestCreatures_run_" + str(self.run_number) + "_seed_" + str(self.randomSeed) + ".pkl"
		with open(filename, 'wb') as f: # temporary 
			pickle.dump(self.parents[i], f)

	# def saveGeneration(self):
	# 	with open('./bestCreatures.pkl', 'wb') as f: # temporary 
	# 		pickle.dump(self.parents[i], f)

	def saveLineage(self):
		filename = "./data/exp" + str(self.exp_number) + "/lineages/lineage_run_" + str(self.run_number) + "_seed_" + str(self.randomSeed) + ".pkl"
		with open(filename, 'wb') as f: # temporary 
			pickle.dump(self.lineage, f)

	def saveMutations(self):
		filename = "./data/exp" + str(self.exp_number) + "/mutations/mutations_run_" + str(self.run_number) + "_seed_"  + str(self.randomSeed) + ".pkl"
		with open(filename, 'wb') as f: # temporary 
			pickle.dump(self.mutations, f)

	def saveBestFitnessValues(self):
		filename = "./data/exp" + str(self.exp_number) + "/bestFitnessVals/bestFitnessVals_run_" + str(self.run_number) + "_seed_" + str(self.randomSeed) + ".pkl"
		with open(filename , 'wb') as f:
			pickle.dump(self.best_creature_fitness, f)

	def saveAverageFitnessValues(self):
		filename = "./data/exp" + str(self.exp_number) + "/averageFitnessVals/averageFitnessVals_run_" + str(self.run_number) + "_seed_"  + str(self.randomSeed) + ".pkl"
		with open(filename , 'wb') as f:
			pickle.dump(self.averageFitnessVals, f)

	def saveBestCreatureIndex(self):
		best_parent = 0
		best_fitness = float('inf')
		for parent in self.parents:
			if best_fitness > self.parents[parent].fitness:
				best_parent = parent
				best_fitness = self.parents[parent].fitness
		filename = "./data/exp" + str(self.exp_number) + "/bestCreatureIndex/bestCreatureIndex_run_" + str(self.run_number) + "_seed_"  + str(self.randomSeed) + ".txt"
		with open(filename , 'w') as f:
			f.write(str(best_parent) + " " + str(best_fitness))


	def Print(self):
		for parent in self.parents:
			print("\nparent fitness:", self.parents[parent].fitness, "child fitness:", self.children[parent].fitness )

	def __del__(self):
		# with open('./bestFitnessVals/bestCreatureFitnessVals_' + str(self.randomSeed) + '.pkl' , 'wb') as f:
		# 	pickle.dump(self.best_creature_fitness, f)
		self.saveBestCreatureIndex()
		self.saveBestFitnessValues()
		self.saveAverageFitnessValues()
		self.saveLineage()
		self.saveMutations()
		for file in os.listdir("."):
			if file.startswith("brain") or file.startswith("fitness") or file == "1" or file.startswith("body"):
				os.system("rm {}".format(file))
	# 	# os.system("rm fitness*.txt")
	# 	# os.system("rm brain*.nndf")
	# 	# os.system("rm 1")
