from world import WORLD
from robot import ROBOT
import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy


class SIMULATION:
    def __init__(self, directOrGUI, simulationID):
        if directOrGUI == "GUI":
            self.physicsClient = p.connect(p.GUI)
            self.GUI = True
        else:
            self.physicsClient = p.connect(p.DIRECT)
            self.GUI = False

        # p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setGravity(0, 0, c.GRAVITY)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        self.world = WORLD(p)
        self.robot = ROBOT(2, 2, p, simulationID)

        self.run()

    def run(self):
        for i in range(0, c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            # print(backLegTouch)
            if self.GUI:
                time.sleep(1 / 60)
            # print(i)

        # self.robot.Save_Sense()

    def __del__(self):
        p.disconnect()

    def Get_Fitness(self):
        self.robot.Get_Fitness()

