import pybullet as p
from sensor import SENSOR
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

        backLegSensorValues = numpy.zeros(c.ITERATIONS)
        frontLegSensorValues = numpy.zeros(c.ITERATIONS)
        front_target_angles = numpy.zeros(c.ITERATIONS)
        back_target_angles = numpy.zeros(c.ITERATIONS)

        angles = numpy.linspace(0, 2 * math.pi, c.ITERATIONS)

        # target_angles = math.pi / 4 * numpy.sin(angles)


        front_amplitude = math.pi / 8
        front_frequency = 10 / (c.ITERATIONS / (2 * math.pi))
        front_phaseOffset = math.pi / 4

        back_amplitude = math.pi / 4
        back_frequency = 10 / (c.ITERATIONS / (2 * math.pi))
        back_phaseOffset = 0

        for i in range(0, c.ITERATIONS):
            front_target_angle = front_amplitude * numpy.sin(front_frequency * i + front_phaseOffset)
            front_target_angles[i] = front_target_angle

            back_target_angle = back_amplitude * numpy.sin(back_frequency * i + back_phaseOffset)
            back_target_angles[i] = back_target_angle

        self.front_target_angles = front_target_angles
        self.back_target_angles = back_target_angles
        self.Prepare_To_Sense()

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            print(linkName)
            self.sensors[linkName] = SENSOR(linkName)
