import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
x=1
for i in range(9):
    pyrosim.Send_Cube(name="Box", pos=[0, 0, i+.5], size=[x, x, x])
    x *= .9

pyrosim.End()
