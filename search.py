import os
from parallelhillclimber import PARALLEL_HILL_CLIMBER
import platform

# for _ in range(5):
#     os.system("venv\\Scripts\\python generate.py")
#     os.system("venv\\Scripts\\python simulate.py")

import gc
gc.collect()

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
if platform.system() == "Windows":
    phc.Show_Best()
else:
    phc.Save_Best()

