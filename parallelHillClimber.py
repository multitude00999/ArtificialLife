from solution import SOLUTION
import constants as c
import copy
import time
import os
class PARALLEL_HILL_CLIMBER():
	def __init__(self, show_random):
		for file in os.listdir("."):
			if file.startswith("brain") or file.startswith("fitness"):
				os.system("rm {}".format(file))

		self.parents = {}
		self.nextAvailableID = 0
		for i in range(c.populationSize):
			self.parents[i] = SOLUTION(self.nextAvailableID)
			self.nextAvailableID+=1

		if show_random:
			self.show_random()

	def Evolve(self):
		self.Evaluate(self.parents)
		for currentGeneration in range(c.numberOfGenerations):
			print("====== generation ", currentGeneration , " ================ ")
			self.Evolve_For_One_Generation()

	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children)
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

	def Evaluate(self, solutions):
		for i in range(c.populationSize):
			solutions[i].Start_Simulation("DIRECT", "1")


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

		self.parents[best_parent].Start_Simulation("GUI", "0")
		self.parents[best_parent].Wait_For_Simulation_To_End() # temporary fix to remove final fitness file

	def show_random(self):
		self.parents[0].Start_Simulation("GUI", "1")
		self.parents[0].Wait_For_Simulation_To_End()
		

	def Print(self):
		for parent in self.parents:
			print("\nparent fitness:", self.parents[parent].fitness, "child fitness:", self.children[parent].fitness )

	def __del__(self):
		for file in os.listdir("."):
			if file.startswith("brain") or file.startswith("fitness") or file == "1":
				os.system("rm {}".format(file))
	# 	# os.system("rm fitness*.txt")
	# 	# os.system("rm brain*.nndf")
	# 	# os.system("rm 1")
