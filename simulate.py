import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import random
import math


physicsClient = p.connect(p.GUI)
# p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setGravity(0, 0, -9.8)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

iterations = 1000

backLegSensorValues = numpy.zeros(iterations)
frontLegSensorValues = numpy.zeros(iterations)
target_angles = numpy.zeros(iterations)

angles = numpy.linspace(0, 2 * math.pi, iterations)

# target_angles = math.pi / 4 * numpy.sin(angles)


amplitude = math.pi / 4
frequency = 10 / (iterations / (2 * math.pi))
phaseOffset = 0

for i in range(0, iterations):
    target_angle = amplitude * numpy.sin(frequency * i + phaseOffset)
    target_angles[i] = target_angle

    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName=b"Torso_BackLeg",

        controlMode=p.POSITION_CONTROL,

        # targetPosition=-math.pi / 4 + math.pi / 2 * random.random(),
        targetPosition=target_angles[i],

        maxForce=40)

    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName=b"Torso_FrontLeg",

        controlMode=p.POSITION_CONTROL,

        # targetPosition=-math.pi / 4 + math.pi / 2 * random.random(),
        targetPosition=target_angles[i],

        maxForce=40)
    # print(backLegTouch)
    time.sleep(1 / 60)
    # print(i)

p.disconnect()

print(backLegSensorValues)
# numpy.save("data/backLegSensor.npy", backLegSensorValues)
# numpy.save("data/frontLegSensor.npy", frontLegSensorValues)
# numpy.save("data/manualAngles.npy", targetAngles)

