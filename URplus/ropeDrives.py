'''
Created on Dec 8, 2016

@author: MartinHuusBjerge
'''

from URplus.mis341 import MIS341

class RopeDrives(object):
    '''
    Controlling the rope drives on the robot
    '''
    def __init__(self, comport):
        '''
        Constructor see class description for more info.
        '''
        self.__motorLeft = MIS341(comport=comport, motorId=1)
        self.__motorRight = MIS341(comport=comport, motorId=2)
        
    def up(self, velocity):
        pass            
    
    def down(self, velocity):
        pass
    
    def turnClockwise(self):
        pass
    
    def turnCounterClockwise(self):
        pass
    
    def leftUp(self, velocity):
        #Test moment styring
        pass
    
    def rightUp(self, velocity):
        #Test moment styring
        pass
    
    def leftDown(self, velocity):
        #Test moment styring
        pass
    
    def rightDown(self, velocity):
        #Test moment styring
        pass
    
    