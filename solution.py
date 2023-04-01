import os
import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:
    def __init__(self, id):
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
        #print(self.weights)
        self.weights = self.weights * 2 - 1
        #print(self.weights)
        self.myID = id

    def Start_Simulation(self, dirOrGUI, toDelete):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py " + dirOrGUI + " " + str(self.myID)+ " " + str(toDelete) + " 2&>1 &")
    
    def Wait_For_Simulation_To_End(self, toDelete):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        time.sleep(0.1)
        f = open(fitnessFileName, "r")
        self.fitness = float(f.read())
        print("fitness for:", str(self.myID), ":", str(self.fitness))
        f.close
        if(toDelete):
            sysCallText = "rm fitness" + str(self.myID) + ".txt"
            #print(sysCallText)
            os.system(sysCallText)


    def Get_Fitness(self):
        print(self.fitness)
        return self.fitness

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()


    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name=("Torso"), pos=[0,0,1] , size=[1,1,1])


        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,.5,1.0], jointAxis= "1 0 0")
        pyrosim.Send_Cube(name=("FrontLeg"), pos=[0,.5,0] , size=[.2,1,.2])

        pyrosim.Send_Joint( name = "FrontLeg_LowerFrontLeg" , parent= "FrontLeg" , child = "LowerFrontLeg" , type = "revolute", position = [0, 1, 0], jointAxis= "1 0 0")
        pyrosim.Send_Cube(name=("LowerFrontLeg"), pos=[0,0,-.5] , size=[.2,.2,1])
##############

        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0,-0.5,1.0],jointAxis= "1 0 0")
        pyrosim.Send_Cube(name=("BackLeg"), pos=[0,-.5,0] , size=[.2,1,.2])

        pyrosim.Send_Joint( name = "BackLeg_LowerBackLeg" , parent= "BackLeg" , child = "LowerBackLeg" , type = "revolute", position = [0,-1,0],jointAxis= "1 0 0")
        pyrosim.Send_Cube(name=("LowerBackLeg"), pos=[0,0,-.5] , size=[.2,.2,1])
##############

        pyrosim.Send_Joint( name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-.5,0,1.0],jointAxis= "0 1 0")
        pyrosim.Send_Cube(name=("LeftLeg"), pos=[-.5,0,0] , size=[1,.2,.2])

        pyrosim.Send_Joint( name = "LeftLeg_LowerLeftLeg" , parent= "LeftLeg" , child = "LowerLeftLeg" , type = "revolute", position = [-1,0,0],jointAxis= "0 1 0")
        pyrosim.Send_Cube(name=("LowerLeftLeg"), pos=[0,0,-.5] , size=[.2,.2,1])
##############

        pyrosim.Send_Joint( name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [.5,0,1.0],jointAxis= "0 1 0")
        pyrosim.Send_Cube(name=("RightLeg"), pos=[.5,0,0] , size=[1,.2,.2])

        pyrosim.Send_Joint( name = "RightLeg_LowerRightLeg" , parent= "RightLeg" , child = "LowerRightLeg" , type = "revolute", position = [1.0,0,0],jointAxis= "0 1 0")
        pyrosim.Send_Cube(name=("LowerRightLeg"), pos=[0,0,-.5] , size=[.2,.2,1])
##############

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        #sensors
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "LowerFrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "LowerBackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LowerRightLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LowerLeftLeg")

        #motors
        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 5 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 6 , jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name = 7 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name = 7 , jointName = "FrontLeg_LowerFrontLeg")
        pyrosim.Send_Motor_Neuron(name = 8 , jointName = "BackLeg_LowerBackLeg")
        pyrosim.Send_Motor_Neuron(name = 9 , jointName = "RightLeg_LowerRightLeg")
        pyrosim.Send_Motor_Neuron(name = 10 , jointName = "LeftLeg_LowerLeftLeg")

        for currRow in range(c.numSensorNeurons):
            for currCol in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currRow , targetNeuronName = currCol + c.numSensorNeurons , weight = self.weights[currRow][currCol])

                #print(str(currRow) + str(currCol) + str(self.weights[currRow][currCol]))

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0,c.numSensorNeurons-1)
        randomCol = random.randint(0,c.numMotorNeurons-1)
        self.weights[randomRow][randomCol] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id

    def Print(self):
        print("solution id:", str(self.myID), "fitness:", str(self.fitness))