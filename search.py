import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import sys

#os.system("python3 generate.py")
#os.system("python3 simulate.py")

if(sys.argv[1] == "true"):
    print("symmetric from phc")
    symmetric = True
else:
    print("non symmetric from phc")
    symmetric = False

phc = PARALLEL_HILL_CLIMBER(symmetric)

phc.Evolve()
phc.Show_Best()
phc.Write_Fitness_Vec()
phc.Show_Fitness_Graph()