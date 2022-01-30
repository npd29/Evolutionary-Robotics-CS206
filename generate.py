import pyrosim.pyrosim as pyrosim


def createWorld():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-5, 5, .5], size=[1, 1, 1])
    pyrosim.End()

def createRobot():
    pyrosim.Start_URDF("body.urdf")
    # pyrosim.Send_Cube(name="link0", pos=[0, 0, .5], size=[1, 1, 1])
    # pyrosim.Send_Joint(name="link0_link1", parent="link0", child="link1", type="revolute", position=[0, 0, 1])
    # pyrosim.Send_Cube(name="link1", pos=[0, 0,.5], size=[1, 1, 1])
    # pyrosim.Send_Joint(name="link1_link2", parent="link1", child="link2", type="revolute", position=[0, 0, 1])
    # pyrosim.Send_Cube(name="link2", pos=[0, 0, .5], size=[1, 1, 1])
    # pyrosim.Send_Joint(name="link2_link3", parent="link2", child="link3", type="revolute", position=[.5, 0, .5])
    # pyrosim.Send_Cube(name="link3", pos=[.5, 0, 0], size=[1, 1, 1])
    # pyrosim.Send_Joint(name="link3_link4", parent="link3", child="link4", type="revolute", position=[1, 0, 0])
    # pyrosim.Send_Cube(name="link4", pos=[.5, 0, 0], size=[1, 1, 1])
    # pyrosim.Send_Joint(name="link4_link5", parent="link4", child="link5", type="revolute", position=[0, 0, -1])
    # pyrosim.Send_Cube(name="link5", pos=[.5, 0, 0], size=[1, 1, 1])
    # pyrosim.Send_Joint(name="link5_link6", parent="link5", child="link6", type="revolute", position=[0, 0, -1])
    # pyrosim.Send_Cube(name="link6", pos=[.5, 0, 0], size=[1, 1, 1])
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[-.5, 0, 1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[-.5, 0, -.5], size=[1, 1, 1])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[.5, 0, 1])
    pyrosim.Send_Cube(name="BackLeg", pos=[.5, 0, -0.5], size=[1, 1, 1])
    pyrosim.End()


createWorld()
createRobot()
