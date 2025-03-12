import pyrosim.pyrosim as pyrosim
import random


def Create_World():
    pyrosim.Start_SDF("world.sdf")

    pyrosim.Send_Cube(name="Box", pos=[-2, 2, .5], size=[1, 1, 1])

    pyrosim.End()


Create_World()


def Generate_Body():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-.5, 0, -.5], size=[1, 1, 1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[.5, 0, -.5], size=[1, 1, 1])

    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[-0.5, 0, 1])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0.5, 0, 1])
    pyrosim.End()


Generate_Body()


def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")

    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

    for sense in range(0, 3):
        for motor in range(3, 5):
            pyrosim.Send_Synapse(sourceNeuronName=sense, targetNeuronName=motor, weight=random.random() * 2 - 1)

    pyrosim.End()


Generate_Brain()


def Create_Robot():




    # pyrosim.Send_Cube(name="Link0", pos=[0, 0, .5], size=[1, 1, 1])
    # pyrosim.Send_Cube(name="Link1", pos=[0, 0, .5], size=[1, 1, 1])
    # pyrosim.Send_Cube(name="Link2", pos=[0, 0, .5], size=[1, 1, 1])
    # pyrosim.Send_Cube(name="Link3", pos=[0, .5, 0], size=[1, 1, 1])
    # pyrosim.Send_Cube(name="Link4", pos=[0, .5, 0], size=[1, 1, 1])
    # pyrosim.Send_Cube(name="Link5", pos=[0, 0, -.5], size=[1, 1, 1])
    # pyrosim.Send_Cube(name="Link6", pos=[0, 0, -.5], size=[1, 1, 1])
    #
    # pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[0, 0, 1])
    # pyrosim.Send_Joint(name="Link1_Link2", parent="Link1", child="Link2", type="revolute", position=[0, 0, 1])
    # pyrosim.Send_Joint(name="Link2_Link3", parent="Link2", child="Link3", type="revolute", position=[0, .5, .5])
    # pyrosim.Send_Joint(name="Link3_Link4", parent="Link3", child="Link4", type="revolute", position=[0, 1, 0])
    # pyrosim.Send_Joint(name="Link4_Link5", parent="Link4", child="Link5", type="revolute", position=[0, .5, -.5])
    # pyrosim.Send_Joint(name="Link5_Link6", parent="Link5", child="Link6", type="revolute", position=[0, 0, -1])

    pyrosim.End()


# Create_Robot()
# pyrosim.Send_Cube(name="Box", pos=[0, 0, .5], size=[1, 1, 1])
# pyrosim.Send_Cube(name="Box2", pos=[1, 0, 1.5], size=[1, 1, 1])

# Variables for boxes
# length, width, height = 1, 1, 1
#
# x = 0
# while x < 5:
#     y = 0
#     while y < 5:
#         # Use total height to find height of next box
#         total_height = 0
#         i = 0
#         length, width, height = 1, 1, 1
#         while i < 10:
#             pyrosim.Send_Cube(name=f"Box{i}{x}{y}", pos=[x, y, total_height + height / 2], size=[length, width, height])
#             length *= 0.9
#             width *= 0.9
#             total_height += height
#             height *= 0.9
#             i += 1
#         y += 1
#     x += 1
#


