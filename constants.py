import math

ITERATIONS = 500
GRAVITY = -9.8
MAX_FORCE = 40

FRONT_A = math.pi / 8
FRONT_F = 10 / (ITERATIONS / (2 * math.pi))
FRONT_P = math.pi / 4

BACK_A = math.pi / 4
BACK_F = 10 / (ITERATIONS / (2 * math.pi))
BACK_P = 0

numberOfGenerations = 10
populationSize = 10
