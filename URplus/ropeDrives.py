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
        
    def robotUp(self):
        pass            
    
    def robotDown(self):
        pass