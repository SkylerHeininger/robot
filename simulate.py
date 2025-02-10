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
front_target_angles = numpy.zeros(iterations)
back_target_angles = numpy.zeros(iterations)

angles = numpy.linspace(0, 2 * math.pi, iterations)

# target_angles = math.pi / 4 * numpy.sin(angles)


front_amplitude = math.pi / 8
front_frequency = 10 / (iterations / (2 * math.pi))
front_phaseOffset = math.pi / 4

back_amplitude = math.pi / 4
back_frequency = 10 / (iterations / (2 * math.pi))
back_phaseOffset = 0

for i in range(0, iterations):
    front_target_angle = front_amplitude * numpy.sin(front_frequency * i + front_phaseOffset)
    front_target_angles[i] = front_target_angle

    back_target_angle = back_amplitude * numpy.sin(back_frequency * i + back_phaseOffset)
    back_target_angles[i] = back_target_angle

# numpy.save("data/frontAngles.npy", front_target_angles)
# numpy.save("data/backAngles.npy", back_target_angles)
#
# exit()

for i in range(0, iterations):

    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName=b"Torso_BackLeg",

        controlMode=p.POSITION_CONTROL,

        # targetPosition=-math.pi / 4 + math.pi / 2 * random.random(),
        targetPosition=back_target_angles[i],

        maxForce=40)

    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName=b"Torso_FrontLeg",

        controlMode=p.POSITION_CONTROL,

        # targetPosition=-math.pi / 4 + math.pi / 2 * random.random(),
        targetPosition=front_target_angles[i],

        maxForce=40)
    # print(backLegTouch)
    time.sleep(1 / 60)
    # print(i)

p.disconnect()

# print(backLegSensorValues)
# numpy.save("data/backLegSensor.npy", backLegSensorValues)
# numpy.save("data/frontLegSensor.npy", frontLegSensorValues)

