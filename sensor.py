import numpy
import constants as c
import pyrosim.pyrosim as pyrosim


class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = None
        self.Prepare_To_Sense()
        # print(self.values)

    def Prepare_To_Sense(self):
        self.values = numpy.zeros(c.ITERATIONS)

    def Get_Value(self, t):
        value = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        self.values[t] = value
        # if t == c.ITERATIONS - 1:
        #     print(self.values)

    def Save_Values(self):
        numpy.save(f"data/{self.linkName}.npy", self.values)

