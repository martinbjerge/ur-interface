'''
Created on Dec 8, 2016

@author: MartinHuusBjerge
'''

from URplus.mis341 import MIS341
from URplus.mis341 import OperatingMode
import time
import numpy as np

class   RopeDrives(object):
    '''
    Controlling the rope drives on the robot
    '''
    def __init__(self):
        '''
        Constructor see class description for more info.
        '''
        self.__motorLeft = MIS341(host='192.168.0.11', motorId=1, reversed=True)
        self.__motorRight = MIS341(host='192.168.0.12', motorId=1, reversed=False)
        self.__motorLeft.setMaxVelocity(0)
        self.__motorRight.setMaxVelocity(0)
        self.__motorLeft.setOperationMode(OperatingMode.Velocity)
        self.__motorRight.setOperationMode(OperatingMode.Velocity)
        self.__drumRadius = 0.08
        self.__gearRatio = 50
        
    def up(self, velocity):
        '''
        Move the entire robot up at a given velocity - velocity is meters/second
        note - max velocity is 0.35 m/s - be careful - thats quick 
        '''
        if(velocity>0.35):
            raise ValueError('Velocity not allowed')
        
        self.__motorLeft.setMaxVelocity(self.__getMotorRPMFromVelocity(velocity))
        self.__motorRight.setMaxVelocity(self.__getMotorRPMFromVelocity(velocity))
        time.sleep(0.1)
                
    
    def down(self, velocity):
        '''
        Move the entire robot down at a given velocity - velocity is meters/second
        note - max velocity is 0.35 m/s - be careful - thats quick  
        '''
        if(velocity>0.35):
            raise ValueError('Velocity not allowed')
        
        self.__motorLeft.setMaxVelocity(self.__getMotorRPMFromVelocity(velocity)*(-1))
        self.__motorRight.setMaxVelocity(self.__getMotorRPMFromVelocity(velocity)*(-1))
        time.sleep(0.1)
    
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
        note - max velocity is 0.35 m/s - be careful - thats quick  
        '''
        if(velocity>0.35 or velocity < 0):
            raise ValueError('Velocity not allowed')
        
        self.__motorLeft.setMaxVelocity(self.__getMotorRPMFromVelocity(velocity))
        self.__motorRight.setMaxVelocity(0)
        
    
    def rightUp(self, velocity):
        '''
        Rotate the entire robot by lifting the righthand side up at a given velocity
        while the lefthand side is stationary - velocity is meters/second 
        note - max velocity is 0.35 m/s - be careful - thats quick 
        '''
        if(velocity>0.35 or velocity < 0):
            raise ValueError('Velocity not allowed')
        
        self.__motorLeft.setMaxVelocity(0)
        self.__motorRight.setMaxVelocity(self.__getMotorRPMFromVelocity(velocity))
    
    def leftDown(self, velocity):
        '''
        Rotate the entire robot by lowering the lefthand side at a given velocity
        while the righthand side is stationary - velocity is meters/second 
        note - max velocity is 0.35 m/s - be careful - thats quick 
        '''
        if(velocity>0.35 or velocity < 0):
            raise ValueError('Velocity not allowed')
        
        self.__motorLeft.setMaxVelocity(self.__getMotorRPMFromVelocity(velocity)*(-1))
        self.__motorRight.setMaxVelocity(0)
    
    def rightDown(self, velocity):
        '''
        Rotate the entire robot by lowering the righthand side at a given velocity
        while the lefthand side is stationary - velocity is meters/second 
        note - max velocity is 0.35 m/s - be careful - thats quick 
        '''
        if(velocity>0.35 or velocity < 0):
            raise ValueError('Velocity not allowed')
        
        self.__motorLeft.setMaxVelocity(0)
        self.__motorRight.setMaxVelocity(self.__getMotorRPMFromVelocity(velocity)*(-1))
    
    def stop(self):
        '''
        Stop the robot
        '''
        self.__motorLeft.setMaxVelocity(0)
        self.__motorRight.setMaxVelocity(0)
        time.sleep(0.1)
        
    def __getMotorRPMFromVelocity(self, velocity):
        drumRPM = (velocity*60) / ( 2*np.pi*self.__drumRadius)
        motorRPM = self.__gearRatio * drumRPM
        return motorRPM
    