import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")


def buildTower(x,y): #builds 1 of the towers centered at x,y
    scale = 1.0
    for i in range(1,10):
        pyrosim.Send_Cube(name=("Box"+str(i)), pos=[x,y,i-.5] , size=[scale,scale,scale])
        scale *= .9

for i in range(-5,5,2):
    for j in range(-5,5,2):
        buildTower(i/2.0,j/2.0)

pyrosim.End()