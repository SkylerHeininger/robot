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

        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

        p.setGravity(0, 0, c.GRAVITY)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        self.world = WORLD(p)
        self.robot = ROBOT(2, 2, p, simulationID)

        self.simId = simulationID

        self.run()

    def run(self):
        # if self.GUI:
        #     print("Ready")
        #     while True:
        #         try:
        #             if keyboard.is_pressed('esc'):
        #                 print("Exiting...")
        #                 break
        #         except:
        #             break
        max_jump_height = 0
        for i in range(0, c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            # print(backLegTouch)
            if self.GUI:
                time.sleep(1 / 60)
            # print(i)
            robot_info = p.getBasePositionAndOrientation(self.robot.robotId, 0)
            positionOfLink0 = robot_info[0][2]
            if positionOfLink0 > max_jump_height:
                max_jump_height = positionOfLink0

        self.robot.Save_Sense()
        with open(f"height_{self.simId}.txt", "w") as f:
            f.write(str(max_jump_height))

    def __del__(self):
        p.disconnect()

    def Get_Fitness(self):
        self.robot.Get_Fitness()

