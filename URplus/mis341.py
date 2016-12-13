'''
Created on Dec 8, 2016

@author: MartinHuusBjerge
'''
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.client.sync import ModbusUdpClient as ModbusClient

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
import logging
import time
import struct
from bitstring import Bits
from bitstring import BitArray

class OperatingMode:
    Passive = 0
    Velocity = 1
    Position = 2
    Gear = 3
    ZeroSearchType1 = 13
    ZeroSearchType2 = 14
    SafeMode = 15


class MIS341(object):
    '''
    This class is running a MIS341 motor via Modbus RTU over serial
    In the future we expect to change this over to TCP
    '''
    def __init__(self, comport, motorId):
        '''
        Constructor - takes comport and the motorId configured in the motor
        '''
        logging.basicConfig()
        log = logging.getLogger()
        log.setLevel(logging.ERROR)
        
        self.__motorId = motorId
        #self.__client = ModbusClient(host='192.168.0.23')
        self.__client = ModbusClient(method='rtu', port=comport, baudrate=19200, databits=8, bytesize=8, parity='E', stopbits=1)
        
        
    def getOperationMode(self):
        '''
        Get the current Operation MOde of the motor 
        Returns OperatingMode - see OperatingMode class for details
        '''
        result = self.__client.read_holding_registers(40004,1, unit=self.__motorId)
        return result.registers[0]
    
    def setOperationMode(self, operationMode):
        '''
        Set the current Operation MOde of the motor 
         - see OperatingMode class for details
        '''
        commands = []
        commands.append(operationMode)
        result = self.__client.write_registers(40004, commands, unit=self.__motorId)
        #print(result.function_code)
    
    def getDesiredPosition(self):
        pass
    
    def setDesiredPosition(self, position):
        pass
    
    def getMaxVelocity(self):
        '''
        Get the currently configured MaxVelocity
        returns RPM
        '''
        result = self.__client.read_holding_registers(40010,2, unit=self.__motorId)
        return self.__getValueFromTwoRegisters(result)
        
    
    def setMaxVelocity(self, rpm):
        '''
        Set maxium velocity in RPM
        '''
        if(rpm < -3000 or rpm > 3000):
            raise ValueError('Overspeed on motor - outside specs')
        
        commands = []
        #if(rpm>=0):
        #    commands.append(int(rpm*100))
        #    commands.append(int(0))
        #else:
        #    commands.append(int(65535-(rpm*100*-1)))
        #    commands.append(int(65535))
        
        fullRegister = Bits(int=rpm*100, length=32)
        highWord = Bits(bin = fullRegister[0:16].bin)
        lowWord = Bits(bin = fullRegister[16:32].bin)
        commands.append(lowWord.uint)
        commands.append(highWord.uint)
        result = self.__client.write_registers(40010, commands, unit=self.__motorId)
        #print(result.function_code)
    
    def getActualVelocity(self):
        '''
        Get current actual velocity
        returns RPM
        '''
        result = self.__client.read_holding_registers(40024,2, unit=self.__motorId)
        return self.__getValueFromTwoRegisters(result)
        
        
    def __getValueFromTwoRegisters(self, registers):
        if(registers.registers[1]==65535):
            temp = 65535-registers.registers[0]
            return (temp)*-1/100
        else: 
            return registers.registers[0]/100
            