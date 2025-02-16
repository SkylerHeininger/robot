import numpy
import constants as c


class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(c.ITERATIONS)
        # print(self.values)
