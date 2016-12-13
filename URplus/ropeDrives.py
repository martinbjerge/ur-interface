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
        '''
        Move the entire robot up at a given velocity - velocity is meters/second 
        '''
        pass            
    
    def down(self, velocity):
        '''
        Move the entire robot down at a given velocity - velocity is meters/second 
        '''
        pass
    
    '''
    def turnClockwise(self):
        pass
    
    def turnCounterClockwise(self):
        pass
    '''
   
    def leftUp(self, velocity):
        '''
        Rotate the entire robot by lifting the lefthand side up at a given velocity
        while the righthand side is stationary - velocity is meters/second 
        '''
        #Test moment styring
        pass
    
    def rightUp(self, velocity):
        '''
        Rotate the entire robot by lifting the righthand side up at a given velocity
        while the lefthand side is stationary - velocity is meters/second 
        '''
        #Test moment styring
        pass
    
    def leftDown(self, velocity):
        '''
        Rotate the entire robot by lowering the lefthand side at a given velocity
        while the righthand side is stationary - velocity is meters/second 
        '''
        #Test moment styring
        pass
    
    def rightDown(self, velocity):
        '''
        Rotate the entire robot by lowering the righthand side at a given velocity
        while the lefthand side is stationary - velocity is meters/second 
        '''
        #Test moment styring
        pass
    
    def stop(self):
        '''
        Stop the robot
        '''
        pass
    