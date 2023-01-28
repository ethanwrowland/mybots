import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("box.sdf")
pyrosim.Send_Cube(name="Box", pos=[0,0,1.5] , size=[1,2,3])

pyrosim.End()