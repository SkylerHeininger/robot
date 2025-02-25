import pybullet as p
from sensor import SENSOR
from motor import MOTOR
import constants
import pyrosim.pyrosim as pyrosim
import numpy
import math
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK


class ROBOT:
    def __init__(self, s, m, p):
        self.p = p
        self.sensors = {}
        self.motors = {}
        self.nn = NEURAL_NETWORK("brain.nndf")

        self.robotId = self.p.loadURDF("body.urdf")

        pyrosim.Prepare_To_Simulate(self.robotId)

        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            # print(linkName)
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName].Get_Value(t)

    def Save_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName].Save_Values()

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            print(jointName)
            self.motors[jointName] = MOTOR(jointName, self.p)

    def Act(self, t):
        # for jointName in pyrosim.jointNamesToIndices:
        #     self.motors[jointName].Set_Value(t, self)
        for neuronName in self.nn.Get_Neuron_Names():
            # print(neuronName)
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode("utf-8")
                jointName = jointName.decode("utf-8")
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(desiredAngle, self)
                print(neuronName, jointName, desiredAngle)



    def Think(self):
        self.nn.Update()
        self.nn.Print()


