from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        #delete all the left over stuff
        idToDelete = 0
        fitnessFileName = "fitness" + str(idToDelete) +".txt"
        while(os.path.exists(fitnessFileName)):
            os.system("rm " + fitnessFileName)
            idToDelete +=1 
        idToDelete = 0
        brainFileName = "brain" + str(idToDelete) +".nndf"
        while(os.path.exists(brainFileName)):
            os.system("rm " + brainFileName)
            idToDelete +=1         

        #create the initial population of parents
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
    
    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations-1):
            print("current gen: " + str(currentGeneration))
            self.Evolve_For_One_Generation()
    
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
        
    def Spawn(self):
        self.children = {}
        for p in self.parents:
            self.children[p] = copy.deepcopy(self.parents[p])
            self.children[p].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for c in self.children:
            self.children[c].Mutate()
            #print("mutated" + str(self.children[c].myID))

    def Select(self):
        #print("parent fitness" + str(self.parent.fitness))
        #print("child fitness" + str(self.child.fitness))
        
        for p in self.parents:
            if(self.parents[p].fitness > self.children[p].fitness):
                self.parents[p] = self.children[p]

    def Print(self):
        print("\n\nParents:")
        for p in self.parents:
            self.parents[p].Print()
        print("\nChildren:")
        for c in self.children:
            self.children[c].Print()
        print()

    def Show_Best(self):
        #find the best one:
        mostFitScore = self.parents[0].fitness
        mostFitSpot = 0
        for p in self.parents:
            if (self.parents[p].fitness < mostFitScore):
                mostFitScore = self.parents[p].fitness
                mostFitSpot = p
        self.parents[mostFitSpot].Start_Simulation("GUI")
        self.parents[mostFitSpot].Wait_For_Simulation_To_End()

    def Evaluate(self, solutions):
        for s in solutions:
            solutions[s].Start_Simulation("DIRECT")
        for s in solutions:
            solutions[s].Wait_For_Simulation_To_End()
    
        
