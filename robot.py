import pybullet as p
from sensor import SENSOR
from motor import MOTOR
import constants
import pyrosim.pyrosim as pyrosim
import numpy
import math
import constants as c


class ROBOT:
    def __init__(self, s, m, p):
        self.p = p
        self.sensors = {}
        self.motors = {}

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
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName].Set_Value(t, self)
