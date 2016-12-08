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
        
    def setValve(self, valveNumber, state):
        #husk at lave input validering
        valveNumber = valveNumber*2
        result = self.__client.write_coil(valveNumber, state)    #Det ser ud som om registrene starter ved nul til 64
        print(result)
        
    def getValvePosition(self, valveNumber):
        
        
        result = self.__client.read_coils(valveNumber*2, 1)
        if(result == None): #Just one retry
            time.sleep(0.2)
            result = self.__client.read_coils(valveNumber, 1)
        if(result != None):
            return result.bits[0]
        else:
            return None