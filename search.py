import os

numIters = 5
for i in range(numIters):
	os.system("python3 generate.py")
	os.system("python3 simulate.py")