import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
from world import WORLD
from robot import ROBOT
from motor import MOTOR
from sensor import SENSOR

class SIMULATION:
    def __init__(self):
        self.world = WORLD()
        self.robot = ROBOT()
        
        self.physicsClient = p.connect(p.GUI)

        pybullet.configureDebugVisualizer(pybullet.COV_ENABLE_GUI,0)
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        p.setGravity(0,0,-9.8)

        pyrosim.Prepare_To_Simulate(self.robot.robotId)