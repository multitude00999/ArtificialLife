from solution import SOLUTION
import constants as c
import copy
class PARALLEL_HILL_CLIMBER():
	def __init__(self):
		# self.parent = SOLUTION()
		pass

	def Evolve(self):
		# self.parent.Evaluate("GUI")

		# for currentGeneration in range(c.numberOfGenerations):
		# 	print("====== generation ", currentGeneration , " ================ ")
		# 	self.Evolve_For_One_Generation()
		pass

	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.child.Evaluate("DIRECT")
		print("\n================")
		print("parent fitness", self.parent.fitness)
		print("child fitness", self.child.fitness)
		print("================")
		self.Select()

	def Spawn(self):
		self.child = copy.deepcopy(self.parent)

	def Mutate(self):
		self.child.Mutate()

	def Select(self):
		# print("parent fitness", self.parent.fitness)
		# print("child fitness", self.child.fitness)

		if self.parent.fitness > self.child.fitness:
			self.parent = copy.deepcopy(self.child)

	def Show_Best(self):
		# self.parent.Evaluate("GUI")
		pass
