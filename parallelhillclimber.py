from solution import SOLUTION
import os
import constants as c
import copy
import numpy as np
import pickle


class PARALLEL_HILL_CLIMBER():
    def __init__(self):
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")

        self.parents = {}
        self.children = {}
        self.nextAvailableID = 0
        for i in range(0, c.populationSize): # This is popSize - 1 inclusive
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

        self.matr = np.zeros((c.numberOfGenerations, c.populationSize))
        self.generation = 0

    def Evolve(self):
        # self.parent.Evaluate("GUI")

        # for parent_key in self.parents.keys():
        #     self.parents[parent_key].Start_Simulation("DIRECT")
        #
        # for parent_key in self.parents.keys():
        #     self.parents[parent_key].Wait_For_Simulation_To_End()

        self.Evaluate(self.parents)

        for gen in range(c.numberOfGenerations):
            self.generation = gen
            self.Evolve_For_One_Generation()
            self.Print()

        np.savetxt("A.csv", self.matr, delimiter=",")

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Select()

    def Spawn(self):
        self.children = {}
        for parent_key in self.parents.keys():
            self.children[parent_key] = copy.deepcopy(self.parents[parent_key])
            self.children[parent_key].Set_Id(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child_key in self.children.keys():
            self.children[child_key].Mutate()

    def Select(self):
        for parent_key in self.parents.keys():
            parent = self.parents[parent_key]
            child = self.children[parent_key]
            if child.fitness > parent.fitness:
                self.parents[parent_key] = self.children[parent_key]

    def Print(self):
        for parent_key in self.parents.keys():
            parent = self.parents[parent_key]
            child = self.children[parent_key]
            print("\n", parent.fitness, child.fitness)

    def Show_Best(self):
        min_fitness_parent = self.parents[0]
        for parent_key in self.parents.keys():
            if self.parents[parent_key].fitness > min_fitness_parent.fitness:
                min_fitness_parent = self.parents[parent_key]
        min_fitness_parent.Start_Simulation("GUI")
        min_fitness_parent.Wait_For_Simulation_To_End()

    def Save_Best(self):
        best = max(self.parents.values(), key=lambda p: p.fitness)
        with open("best_robot.pkl", "wb") as f:
            pickle.dump(best, f)

    def Evaluate(self, solutions):
        for solution_key in solutions.keys():
            solutions[solution_key].Start_Simulation("DIRECT")

        for idx, solution_key in enumerate(solutions.keys()):
            temp = solutions[solution_key].Wait_For_Simulation_To_End()
            self.matr[self.generation, idx] = temp



