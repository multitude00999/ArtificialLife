from simulation import SIMULATION
import sys
directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
deleteBrain = sys.argv[3]
deleteBody = sys.argv[4]
simulation = SIMULATION(directOrGUI, solutionID, deleteBrain, deleteBody)
simulation.Run()
simulation.Get_Fitness()