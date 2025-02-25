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
        self.p = p

    def Set_Value(self, desiredAngle, robot):
        pyrosim.Set_Motor_For_Joint(

            bodyIndex=robot.robotId,

            jointName=self.jointName,

            controlMode=self.p.POSITION_CONTROL,

            # targetPosition=-math.pi / 4 + math.pi / 2 * random.random(),
            targetPosition=desiredAngle,

            maxForce=c.MAX_FORCE)

