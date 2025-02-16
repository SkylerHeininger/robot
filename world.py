class WORLD:
    def __init__(self, p):
        self.p = p

        self.planeId = self.p.loadURDF("plane.urdf")
        self.p.loadSDF("world.sdf")

