import random
import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import constants as c


class SOLUTION():
    def __init__(self, myId):
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
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
            lines = f.readlines()
            xpos = float(lines[0].strip())
            jump_fitness = float(lines[1].strip())
            self.fitness = -xpos * jump_fitness
        os.system(f"del {fitnessFileName}")
        # print(f"Fitness: {self.fitness}")

    def Create_World(self):
        pyrosim.Start_SDF(f"world.sdf")

        pyrosim.Send_Cube(name="Box", pos=[-2, 2, .5], size=[1, 1, 1])

        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF(f"body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])
        pyrosim.Send_Cube(name="BackRightLeg", pos=[0.5, -0.5, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Cube(name="BackLeftLeg", pos=[-0.5, -0.5, 0], size=[1, 0.2, 0.2])

        pyrosim.Send_Cube(name="FrontRightLeg", pos=[0.5, 0.5, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Cube(name="FrontLeftLeg", pos=[-0.5, 0.5, 0], size=[1, 0.2, 0.2])
        # pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])
        # pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])

        pyrosim.Send_Cube(name="LowerBackRightLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Cube(name="LowerBackLeftLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Cube(name="LowerFrontRightLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Cube(name="LowerFrontLeftLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        # pyrosim.Send_Cube(name="LowerLeftLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        # pyrosim.Send_Cube(name="LowerRightLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_BackRightLeg", parent="Torso", child="BackRightLeg", type="revolute",
                           position=[0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="Torso_BackLeftLeg", parent="Torso", child="BackLeftLeg", type="revolute",
                           position=[-0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="Torso_FrontRightLeg", parent="Torso", child="FrontRightLeg", type="revolute",
                           position=[0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="Torso_FrontLeftLeg", parent="Torso", child="FrontLeftLeg", type="revolute",
                           position=[-0.5, 0, 1], jointAxis="0 1 0")
        # pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute",
        #                    position=[-0.5, 0, 1], jointAxis="0 1 0")
        # pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute",
        #                    position=[0.5, 0, 1], jointAxis="0 1 0")

        pyrosim.Send_Joint(name="BackRightLeg_LowerBackRightLeg", parent="BackRightLeg", child="LowerBackRightLeg", type="revolute",
                           position=[1.0, -0.5, 0], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="BackLeftLeg_LowerBackLeftLeg", parent="BackLeftLeg", child="LowerBackLeftLeg", type="revolute",
                           position=[-1.0, -0.5, 0], jointAxis="0 1 0")

        pyrosim.Send_Joint(name="FrontRightLeg_LowerFrontRightLeg", parent="FrontRightLeg", child="LowerFrontRightLeg", type="revolute",
                           position=[1.0, 0.5, 0], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="FrontLeftLeg_LowerFrontLeftLeg", parent="FrontLeftLeg", child="LowerFrontLeftLeg", type="revolute",
                           position=[-1.0, 0.5, 0], jointAxis="0 1 0")

        # pyrosim.Send_Joint(name="LeftLeg_LowerLeftLeg", parent="LeftLeg", child="LowerLeftLeg", type="revolute",
        #                    position=[-1.0, 0, 0], jointAxis="0 1 0")
        #
        # pyrosim.Send_Joint(name="RightLeg_LowerRightLeg", parent="RightLeg", child="LowerRightLeg", type="revolute",
        #                    position=[1.0, 0, 0], jointAxis="0 1 0")

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myId}.nndf")

        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackRightLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="BackLeftLeg")

        pyrosim.Send_Sensor_Neuron(name=3, linkName="FrontRightLeg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="FrontLeftLeg")

        # pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        # pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="LowerBackRightLeg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="LowerBackLeftLeg")

        pyrosim.Send_Sensor_Neuron(name=7, linkName="LowerFrontRightLeg")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="LowerFrontLeftLeg")
        # pyrosim.Send_Sensor_Neuron(name=7, linkName="LowerLeftLeg")
        # pyrosim.Send_Sensor_Neuron(name=8, linkName="LowerRightLeg")

        pyrosim.Send_Motor_Neuron(name=9, jointName="Torso_BackRightLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="Torso_BackLeftLeg")

        pyrosim.Send_Motor_Neuron(name=11, jointName="Torso_FrontRightLeg")
        pyrosim.Send_Motor_Neuron(name=12, jointName="Torso_FrontLeftLeg")

        pyrosim.Send_Motor_Neuron(name=13, jointName="BackLeftLeg_LowerBackLeftLeg")
        pyrosim.Send_Motor_Neuron(name=14, jointName="BackRightLeg_LowerBackRightLeg")

        pyrosim.Send_Motor_Neuron(name=15, jointName="FrontRightLeg_LowerFrontRightLeg")
        pyrosim.Send_Motor_Neuron(name=16, jointName="FrontLeftLeg_LowerFrontLeftLeg")


        # pyrosim.Send_Motor_Neuron(name=11, jointName="Torso_LeftLeg")
        # pyrosim.Send_Motor_Neuron(name=12, jointName="Torso_RightLeg")
        # pyrosim.Send_Motor_Neuron(name=13, jointName="BackLeg_LowerBackLeg")
        # pyrosim.Send_Motor_Neuron(name=14, jointName="FrontLeg_LowerFrontLeg")
        # pyrosim.Send_Motor_Neuron(name=15, jointName="LeftLeg_LowerLeftLeg")
        # pyrosim.Send_Motor_Neuron(name=16, jointName="RightLeg_LowerRightLeg")

        for current_row in range(0, c.numSensorNeurons):
            for current_col in range(0, c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=current_row, targetNeuronName=current_col + c.numSensorNeurons,
                                     weight=self.weights[current_row][current_col])

        pyrosim.End()

    def Mutate(self):
        row = random.randint(0, c.numSensorNeurons - 1)
        col = random.randint(0, c.numMotorNeurons - 1)
        self.weights[row][col] = random.random() * 2 - 1

    def Set_Id(self, myId):
        self.myId = myId
