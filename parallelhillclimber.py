from solution import SOLUTION
import os
import constants as c
import copy


class PARALLEL_HILL_CLIMBER():
    def __init__(self):
        # self.parent = SOLUTION()
        # self.child = None
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(0, c.populationSize): # This is popSize - 1 inclusive
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        # self.parent.Evaluate("GUI")
        # for gen in range(c.numberOfGenerations):
        #     self.Evolve_For_One_Generation()
        #     self.Print()

        for parent_key in self.parents.keys():
            self.parents[parent_key].Start_Simulation("DIRECT")

        for parent_key in self.parents.keys():
            self.parents[parent_key].Wait_For_Simulation_To_End()


    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        self.child.Set_Id(self.nextAvailableID)
        self.nextAvailableID += 1

    def Mutate(self):
        self.child.Mutate()


    def Select(self):
        if self.child.fitness < self.parent.fitness:
            self.parent = self.child

    def Print(self):
        print("\n", self.parent.fitness, self.child.fitness)

    def Show_Best(self):
        # self.parent.Evaluate("GUI")
        pass


