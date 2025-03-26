import os
import keyboard
from parallelhillclimber import PARALLEL_HILL_CLIMBER

# for _ in range(5):
#     os.system("venv\\Scripts\\python generate.py")
#     os.system("venv\\Scripts\\python simulate.py")

import gc
gc.collect()

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()

