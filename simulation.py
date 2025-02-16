from world import WORLD
from robot import ROBOT
import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy


class SIMULATION:
    def __init__(self):

        self.physicsClient = p.connect(p.GUI)

        # p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setGravity(0, 0, c.GRAVITY)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        self.world = WORLD(p)
        self.robot = ROBOT(2, 2, p)

        self.run()

    def run(self):
        backLegSensorValues = numpy.zeros(c.ITERATIONS)
        frontLegSensorValues = numpy.zeros(c.ITERATIONS)
        for i in range(0, c.ITERATIONS):
            p.stepSimulation()
            backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            pyrosim.Set_Motor_For_Joint(

                bodyIndex=self.robot.robotId,

                jointName=b"Torso_BackLeg",

                controlMode=p.POSITION_CONTROL,

                # targetPosition=-math.pi / 4 + math.pi / 2 * random.random(),
                targetPosition=self.robot.front_target_angles[i],

                maxForce=c.MAX_FORCE)

            pyrosim.Set_Motor_For_Joint(

                bodyIndex=self.robot.robotId,

                jointName=b"Torso_FrontLeg",

                controlMode=p.POSITION_CONTROL,

                # targetPosition=-math.pi / 4 + math.pi / 2 * random.random(),
                targetPosition=self.robot.back_target_angles[i],

                maxForce=c.MAX_FORCE)
            # print(backLegTouch)
            time.sleep(1 / 60)
            # print(i)

    def __del__(self):
        p.disconnect()

