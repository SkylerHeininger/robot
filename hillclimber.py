from solution import SOLUTION
import os
import constants as c
import copy


class HILL_CLIMBER():
    def __init__(self):
        self.parent = SOLUTION()
        self.child = None

    def Evolve(self):
        self.parent.Evaluate("GUI")
        for gen in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
            self.Print()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()


    def Select(self):
        if self.child.fitness < self.parent.fitness:
            self.parent = self.child

    def Print(self):
        print("\n", self.parent.fitness, self.child.fitness)

    def Show_Best(self):
        self.parent.Evaluate("GUI")


