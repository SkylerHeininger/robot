import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

# pyrosim.Send_Cube(name="Box", pos=[0, 0, .5], size=[1, 2, 3])
# pyrosim.Send_Cube(name="Box", pos=[0, 0, .5], size=[1, 1, 1])
# pyrosim.Send_Cube(name="Box2", pos=[1, 0, 1.5], size=[1, 1, 1])

# Variables for boxes
length, width, height = 1, 1, 1

x = 0
while x < 5:
    y = 0
    while y < 5:
        # Use total height to find height of next box
        total_height = 0
        i = 0
        length, width, height = 1, 1, 1
        while i < 10:
            pyrosim.Send_Cube(name=f"Box{i}{x}{y}", pos=[x, y, total_height + height / 2], size=[length, width, height])
            length *= 0.9
            width *= 0.9
            total_height += height
            height *= 0.9
            i += 1
        y += 1
    x += 1

pyrosim.End()

