import pyrosim.pyrosim as pyrosim


def createWorld():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-5, 5, .5], size=[1, 1, 1])
    pyrosim.End()

def createRobot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[-.5, 0, 1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[-.5, 0, -.5], size=[1, 1, 1])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[.5, 0, 1])
    pyrosim.Send_Cube(name="BackLeg", pos=[.5, 0, -0.5], size=[1, 1, 1])
    pyrosim.End()


createWorld()
createRobot()
