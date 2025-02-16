import constants as c
import math
import numpy
import pyrosim.pyrosim as pyrosim


class MOTOR:
    def __init__(self, jointName, p):
        self.jointName = jointName
        self.amplitude = None
        self.frequency = None
        self.phaseoffset = None
        self.target_angles = None
        self.Prepare_To_Act()
        self.p = p

    def Prepare_To_Act(self):
        self.amplitude = c.FRONT_A
        self.frequency = c.FRONT_F
        self.phaseoffset = c.FRONT_P

        if self.jointName == b'Torso_BackLeg':
            self.frequency /= 2

        self.target_angles = numpy.zeros(c.ITERATIONS)

        for i in range(0, c.ITERATIONS):
            target_angle = self.amplitude * numpy.sin(self.frequency * i + self.phaseoffset)
            self.target_angles[i] = target_angle

    def Set_Value(self, t, robot):
        pyrosim.Set_Motor_For_Joint(

            bodyIndex=robot.robotId,

            jointName=self.jointName,

            controlMode=self.p.POSITION_CONTROL,

            # targetPosition=-math.pi / 4 + math.pi / 2 * random.random(),
            targetPosition=self.target_angles[t],

            maxForce=c.MAX_FORCE)

