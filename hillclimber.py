from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()
    
    def Evolve(self):
        self.parent.Evaluate("DIRECT")
        for currentGeneration in range(c.numberOfGenerations-1):
            print("current gen: " + str(currentGeneration) + "\n")
            self.Evolve_For_One_Generation()
            if(currentGeneration == 0):
                self.child.Evaluate("GUI")
    

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Select()
        self.Print()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
    
    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        #print("parent fitness" + str(self.parent.fitness))
        #print("child fitness" + str(self.child.fitness))

        if(self.parent.fitness > self.child.fitness):
            self.parent = self.child

    def Print(self):
        print("\n\nparent fitness: " + str(self.parent.fitness) + " child fitness: " + str(self.child.fitness)+ "\n")

    def Show_Best(self):
        self.parent.Evaluate("GUI")
        
