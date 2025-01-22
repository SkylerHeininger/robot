import pybullet as p
import time
import pybullet_data


physicsClient = p.connect(p.GUI)
# p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setGravity(0, 0, -9.8)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
planeId = p.loadURDF("plane.urdf")


p.loadSDF("boxes.sdf")

for i in range(0, 1000):
    p.stepSimulation()
    time.sleep(1 / 60)
    print(i)

p.disconnect()
