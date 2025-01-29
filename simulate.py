import pybullet as p
import time
import pybullet_data


physicsClient = p.connect(p.GUI)
# p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setGravity(0, 0, -9.8)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")



p.loadSDF("world.sdf")

for i in range(0, 1000):
    p.stepSimulation()
    time.sleep(1 / 60)
    print(i)

p.disconnect()
