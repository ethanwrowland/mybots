import os
import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:
    def __init__(self, id, symmetric):
        self.myID = id
        self.symmetric = bool(symmetric)
        if(not self.symmetric):
            self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
            self.weights = self.weights * 2 - 1
        else:
            #this is when it is symmetric
            self.weights = np.random.rand(2, c.numMotorNeurons)
            self.weights = self.weights * 2 - 1
        

        

    def Start_Simulation(self, dirOrGUI, toDelete):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py " + dirOrGUI + " " + str(self.myID)+ " " + str(toDelete) + " 2&>1 &")
    
    def Wait_For_Simulation_To_End(self, toDelete):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.1)
        time.sleep(0.5)
        f = open(fitnessFileName, "r")
        self.fitness = float(f.read())
        #print("fitness for:", str(self.myID), ":", str(self.fitness))
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
        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 5 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 6 , jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name = 7 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name = 8 , jointName = "FrontLeg_LowerFrontLeg")
        pyrosim.Send_Motor_Neuron(name = 9 , jointName = "BackLeg_LowerBackLeg")
        pyrosim.Send_Motor_Neuron(name = 10 , jointName = "RightLeg_LowerRightLeg")
        pyrosim.Send_Motor_Neuron(name = 11 , jointName = "LeftLeg_LowerLeftLeg")
        
        if(not self.symmetric):
            for currRow in range(c.numSensorNeurons):
                for currCol in range(c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName = currRow , targetNeuronName = currCol + c.numSensorNeurons, weight = self.weights[currRow][currCol])

                    #print(str(currRow) + str(currCol) + str(self.weights[currRow][currCol]))
        
        else:
            for row in [0,1]:
                for col in range(c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName = row , targetNeuronName = col + c.numSensorNeurons, weight = self.weights[row][col])
                    mni = c.numSensorNeurons + col
                    #messy bc bilateral symmetry
                    if(mni == 4 or mni == 5 or mni == 8 or mni ==9):
                        pyrosim.Send_Synapse(sourceNeuronName = row + 2, targetNeuronName = col + c.numSensorNeurons + 2, weight = self.weights[row][col])
                    else:
                        pyrosim.Send_Synapse(sourceNeuronName = row + 2, targetNeuronName = col + c.numSensorNeurons - 2, weight = self.weights[row][col])  

        pyrosim.End()

    def Mutate(self):
        if(not self.symmetric):
            randomRow = random.randint(0,c.numSensorNeurons-1) #this won't work for symmetric case
        else:
            randomRow = random.randint(0,1)
            
        randomCol = random.randint(0,c.numMotorNeurons-1)
        self.weights[randomRow][randomCol] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id

    def Print(self):
        print("solution id:", str(self.myID), "fitness:", str(self.fitness))