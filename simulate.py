import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy


physicsClient = p.connect(p.GUI)
# p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setGravity(0, 0, -9.8)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)


for i in range(0, 1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName=b"Torso_BackLeg",

        controlMode=p.POSITION_CONTROL,

        targetPosition=-numpy.pi/4,

        maxForce=500)

    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName=b"Torso_FrontLeg",

        controlMode=p.POSITION_CONTROL,

        targetPosition=numpy.pi / 4,

        maxForce=500)
    # print(backLegTouch)
    time.sleep(1 / 60)
    # print(i)

p.disconnect()

print(backLegSensorValues)
numpy.save("data/backLegSensor.npy", backLegSensorValues)
numpy.save("data/frontLegSensor.npy", frontLegSensorValues)

