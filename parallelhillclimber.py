from solution import SOLUTION
import os
import constants as c
import copy
import numpy as np
import pickle
import platform


class PARALLEL_HILL_CLIMBER():
    def __init__(self):
        if platform.system() == "Windows":
            print("Windows", flush=True)
            os.system("del brain*.nndf")
            os.system("del body*.urdf")
            os.system("del fitness*.txt")
        else:
            print("Linux", flush=True)
            os.system("rm brain*.nndf")
            os.system("rm body*.urdf")
            os.system("rm fitness*.txt")

        self.parents = {}
        self.children = {}
        self.nextAvailableID = 0
        for i in range(0, c.populationSize): # This is popSize - 1 inclusive
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

        self.matr = np.zeros((c.numberOfGenerations, c.populationSize))
        self.parent_scores = [0] * c.populationSize
        self.generation = 0

    def Evolve(self):
        # self.parent.Evaluate("GUI")

        # for parent_key in self.parents.keys():
        #     self.parents[parent_key].Start_Simulation("DIRECT")
        #
        # for parent_key in self.parents.keys():
        #     self.parents[parent_key].Wait_For_Simulation_To_End()

        self.Evaluate(self.parents, parent=True)

        for gen in range(c.numberOfGenerations):
            print(f"GENERATION: {self.generation}", flush=True)
            self.generation = gen
            self.Evolve_For_One_Generation()
            # self.Print()

        np.savetxt("A.csv", self.matr, delimiter=",")

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        scores = self.Evaluate(self.children)
        self.Select(scores)

    def Spawn(self):
        self.children = {}
        for parent_key in self.parents.keys():
            self.children[parent_key] = copy.deepcopy(self.parents[parent_key])
            self.children[parent_key].Set_Id(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child_key in self.children.keys():
            self.children[child_key].Mutate()

    def Select(self, scores):
        for idx, parent_key in enumerate(self.parents.keys()):
            parent = self.parents[parent_key]
            child = self.children[parent_key]
            if child.fitness > parent.fitness:
                self.parents[parent_key] = self.children[parent_key]
                self.parent_scores[idx] = scores[idx]

            self.matr[self.generation, idx] = self.parent_scores[idx]

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

    def Evaluate(self, solutions, parent=False):
        for solution_key in solutions.keys():
            solutions[solution_key].Start_Simulation("DIRECT")

        scores = []
        for idx, solution_key in enumerate(solutions.keys()):
            temp = solutions[solution_key].Wait_For_Simulation_To_End()
            scores.append(temp)
            if parent:
                self.parent_scores[idx] = temp

        return scores



