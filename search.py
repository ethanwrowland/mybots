import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import sys

#os.system("python3 generate.py")
#os.system("python3 simulate.py")

symmetric = bool(sys.argv[1])

phc = PARALLEL_HILL_CLIMBER(symmetric)

phc.Evolve()
phc.Show_Best()
