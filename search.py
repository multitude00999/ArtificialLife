import os
from hillclimber import HILL_CLIMBER
import time

t1 = time.time()
hc  = HILL_CLIMBER()
hc.Evolve()
t2 = time.time()
print("time taken", t2-t1)
hc.Show_Best()
