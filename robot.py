import os

import pybullet as p
from sensor import SENSOR
from motor import MOTOR
import constants
import pyrosim.pyrosim as pyrosim
import numpy
import math
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import numpy as np
import pandas as pd


class ROBOT:
    def __init__(self, s, m, p, simulationID):
        self.p = p
        self.sensors = {}
        self.motors = {}
        self.nn = NEURAL_NETWORK(f"brain{simulationID}.nndf")
        self.simId = simulationID
        os.system(f"del brain{simulationID}.nndf")

        self.robotId = self.p.loadURDF("body.urdf")

        pyrosim.Prepare_To_Simulate(self.robotId)

        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            # print(linkName)
            self.sensors[linkName] = SENSOR(linkName, self.simId)

    def Sense(self, t):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName].Get_Value(t)

    def Save_Sense(self):
        valid_links = ["LowerBackRightLeg", "LowerBackLeftLeg", "LowerFrontRightLeg", "LowerFrontLeftLeg"]
        for linkName in pyrosim.linkNamesToIndices:
            if linkName in valid_links:
                self.sensors[linkName].Save_Values()

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            # print(jointName)
            self.motors[jointName] = MOTOR(jointName, self.p)

    def Act(self, t):
        # for jointName in pyrosim.jointNamesToIndices:
        #     self.motors[jointName].Set_Value(t, self)
        for neuronName in self.nn.Get_Neuron_Names():
            # print(neuronName)
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode("utf-8")
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(desiredAngle, self)
                jointName = jointName.decode("utf-8")
                # print(neuronName, jointName, desiredAngle)

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        # Save the distance traveled
        robot_info = p.getBasePositionAndOrientation(self.robotId, 0)
        positionOfLink0 = robot_info[0]

        # Get the sensor values
        sensor_files = [f"data/LowerBackLeftLeg_{self.simId}.npy", f"data/LowerBackRightLeg_{self.simId}.npy",
                        f"data/LowerFrontRightLeg_{self.simId}.npy", f"data/LowerFrontLeftLeg_{self.simId}.npy"]

        sensor_data = [np.load(file) for file in sensor_files]
        data_shape = sensor_data[0].shape
        averages = []

        for file in sensor_files:
            if os.path.exists(file):
                os.system(f"del {file}")
            else:
                print(f"File {file} not found.")

        for i in range(data_shape[0]):
            values_at_i = [data[i] for data in sensor_data]
            avg = np.mean(values_at_i)
            averages.append(avg)

        data_dict = {f"Sensor_{i + 1}": sensor_data[i] for i in range(len(sensor_data))}

        # Convert the dictionary to a DataFrame
        df = pd.DataFrame(data_dict)

        # Add the averages column
        df['Average'] = averages

        # Save the DataFrame to a CSV file
        df.to_csv("averages.csv", index=False)

        # print(averages)

        one_periods = []
        zero_periods = []
        num_non_all_4 = 0

        current_one_count = 0
        current_zero_count = 0

        for avg in averages:
            if avg == -1:
                if current_one_count > 0:
                    one_periods.append(current_one_count)
                    current_one_count = 0
                current_zero_count += 1
            elif avg == 1:
                if current_zero_count > 0:
                    zero_periods.append(current_zero_count)
                    current_zero_count = 0
                current_one_count += 1
            else:
                if current_zero_count > 0:
                    zero_periods.append(current_zero_count)
                    current_zero_count = 0
                if current_one_count > 0:
                    one_periods.append(current_one_count)
                    current_one_count = 0
                num_non_all_4 += 1

        # Add any remaining periods that ended at the last element
        if current_zero_count > 0:
            zero_periods.append(current_zero_count)
        if current_one_count > 0:
            one_periods.append(current_one_count)

        if zero_periods:
            average_zero_period = sum(zero_periods) / len(zero_periods)
        else:
            average_zero_period = 0

        if one_periods:
            average_one_period = sum(one_periods) / len(one_periods)
        else:
            average_one_period = 0

        # Number of jumps that weren't just noise
        num_jumps = len([count for count in zero_periods if count > 20])

        # Proportion of time without robot touching all four or in air
        prop_all_4 = num_non_all_4 / c.ITERATIONS

        print(positionOfLink0[0], average_zero_period, average_one_period)

        with open(f"fitness{self.simId}.txt", "w") as f:
            f.write(str(positionOfLink0[0]) + "\n")
            f.write(str(average_zero_period) + "\n")
            f.write(str(average_one_period) + "\n")
            f.write(str(num_jumps) + "\n")
            f.write(str(prop_all_4))







