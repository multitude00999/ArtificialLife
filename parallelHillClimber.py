from solution_auto_3d import SOLUTION_AUTO_3D
import constants as c
import copy
import time
import os
import pickle

class PARALLEL_HILL_CLIMBER():
	def __init__(self, show_random):
		for file in os.listdir("."):
			if file.startswith("brain") or file.startswith("fitness") or file.startswith("body"):
				os.system("rm {}".format(file))

		self.parents = {}
		self.nextAvailableID = 0
		self.best_creature_fitness = []
		for i in range(c.populationSize):
			self.parents[i] = SOLUTION_AUTO_3D(self.nextAvailableID, fromScratch = True)
			self.nextAvailableID+=1

		if show_random:
			self.show_random()

	def Evolve(self):
		self.Evaluate(self.parents, fromScratch = True)
		self.get_best_creature_fitness()
		for currentGeneration in range(c.numberOfGenerations):
			print("====== generation ", currentGeneration , " ================ ")
			self.Evolve_For_One_Generation()
			self.get_best_creature_fitness()

	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children, fromScratch = False)
		self.Print()
		self.Select()
		

	def Spawn(self):
		self.children = {}
		for parent in self.parents:
			self.children[parent] = copy.deepcopy(self.parents[parent])
			self.children[parent].Set_ID(self.nextAvailableID)
			self.nextAvailableID+=1

	def Mutate(self):
		
		for child in self.children:
			self.children[child].Mutate()

	def Evaluate(self, solutions, fromScratch):
		for i in range(c.populationSize):
			solutions[i].Start_Simulation("DIRECT", "1", "1", fromScratch)


		for i in range(c.populationSize):
			solutions[i].Wait_For_Simulation_To_End()


	def Select(self):
		for parent in self.parents:
			if self.parents[parent].fitness > self.children[parent].fitness:
				self.parents[parent] = copy.deepcopy(self.children[parent])

	def Show_Best(self):
		best_parent = 0
		best_fitness = float('inf')
		for parent in self.parents:
			if best_fitness > self.parents[parent].fitness:
				best_parent = parent
				best_fitness = self.parents[parent].fitness

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

	def show_random(self):
		self.parents[0].Start_Simulation("GUI", "1", "1", fromScratch = True)
		self.parents[0].Wait_For_Simulation_To_End()
		

	def Print(self):
		for parent in self.parents:
			print("\nparent fitness:", self.parents[parent].fitness, "child fitness:", self.children[parent].fitness )

	def __del__(self):
		with open('best_creature_fitness_vals.pkl' , 'wb') as f:
			pickle.dump(self.best_creature_fitness, f)
		for file in os.listdir("."):
			if file.startswith("brain") or file.startswith("fitness") or file == "1" or file.startswith("body"):
				os.system("rm {}".format(file))
	# 	# os.system("rm fitness*.txt")
	# 	# os.system("rm brain*.nndf")
	# 	# os.system("rm 1")
