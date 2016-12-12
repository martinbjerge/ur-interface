'''
Created on Dec 8, 2016

@author: MartinHuusBjerge
'''
import time

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

class CTEU_EP(object):
    '''
    Controlling the Pneumatics on the robot via a FESTO CTEU-EP that
    is controlling a valveblock - this is via Modbus over TCP
    '''
    def __init__(self, host):
        '''
        Constructor see class description for more info.
        '''
        self.__client = ModbusClient(host=host)
        connected = self.__client.connect()
        if(connected):
            print("Modbus connected to CTEU-EP")
        else:
            pass    #todo - nice error handling and reconnect
        
    def setValve(self, valveNumber, state):
        #Valves are 0 to 11 - todo make input validation
        #valveNumber = valveNumber*2
        result = self.__client.write_coil(valveNumber, state)
        if(result == None): #Just one retry
            time.sleep(0.2)
            result = self.__client.write_coil(valveNumber, state)
        
    def getValvePosition(self, valveNumber):
        #Valves are 0 to 11 - todo make input validation
        result = self.__client.read_coils(valveNumber, 1)
        if(result == None): #Just one retry
            time.sleep(0.2)
            result = self.__client.read_coils(valveNumber, 1)
        if(result != None):
            return result.bits[0]
        else:
            return None
        
        