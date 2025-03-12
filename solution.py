import random
import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import os


class SOLUTION():
    def __init__(self, myId):
        self.weights = np.random.rand(3, 2) * 2 - 1
        self.fitness = None
        self.myId = myId

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        # os.system(f"venv\\Scripts\\python simulate.py {directOrGUI} &")
        os.system("start /B venv\\Scripts\\python simulate.py " + directOrGUI + " " + str(self.myId) + " &")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = f"fitness{self.myId}.txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        with open(fitnessFileName, "r") as f:
            self.fitness = float(f.read())
        os.system(f"del {fitnessFileName}")
        # print(f"Fitness: {self.fitness}")

    def Create_World(self):
        pyrosim.Start_SDF(f"world.sdf")

        pyrosim.Send_Cube(name="Box", pos=[-2, 2, .5], size=[1, 1, 1])

        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF(f"body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-.5, 0, -.5], size=[1, 1, 1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[.5, 0, -.5], size=[1, 1, 1])

        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                           position=[-0.5, 0, 1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position=[0.5, 0, 1])
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myId}.nndf")

        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for current_row in range(0, 3):
            for current_col in range(0, 2):
                pyrosim.Send_Synapse(sourceNeuronName=current_row, targetNeuronName=current_col + 3, weight=self.weights[current_row][current_col])

        pyrosim.End()

    def Mutate(self):
        row = random.randint(0, 2)
        col = random.randint(0, 1)
        self.weights[row][col] = random.random() * 2 - 1

    def Set_Id(self, myId):
        self.myId = myId
