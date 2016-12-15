'''
Python 3.x library to control an UR robot through its TCP/IP interfaces
Copyright (C) 2016  Martin Huus Bjerge, Rope Robotics ApS, Denmark

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software 
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL "Rope Robotics ApS" BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of "Rope Robotics ApS" shall not be used 
in advertising or otherwise to promote the sale, use or other dealings in this Software 
without prior written authorization from "Rope Robotics ApS".
'''

__author__ = "Martin Huus Bjerge"
__copyright__ = "Copyright 2016, Rope Robotics ApS, Denmark"
__license__ = "MIT License"

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
#from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.client.sync import ModbusUdpClient as ModbusClient

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
import time
import struct
from bitstring import Bits
from bitstring import BitArray
import threading
import URBasic

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
    This class is running a JVL - MIS341 motor via Modbus RTU over serial
    In the future we expect to change this over to TCP
    '''
    def __init__(self, host, motorId=1, reversed=False):
        '''
        Constructor - takes comport and the motorId configured in the motor
        '''
        logger = URBasic.dataLogging.DataLogging()
        name = logger.AddEventLogging(__name__,log2Consol=False)        
        self.__logger = logger.__dict__[name]
        self.__motorId = motorId
        self.__client = ModbusClient(host=host)
        #self.__client = ModbusClient(method='rtu', port=comport, baudrate=19200, databits=8, bytesize=8, parity='E', stopbits=1)
        self.__reversed = reversed
        self.__miniumPollTime = 0.004  # see 7.2.5 in ethernet user guide for motor
        self.__clearToSend = True
        self.__minimumPollTimer = threading.Timer(interval=self.__miniumPollTime, function=self.__resetClearToSend)
        
        
    def __safeReadHoldingRegisters(self, registerNumber, length):
        while(not self.__clearToSend):
            pass
        self.__clearToSend=False
        result = self.__client.read_holding_registers(registerNumber,length, unit=self.__motorId)
        self.__minimumPollTimer.start()
        return result
    
    def __safeWriteRegisters(self, registerNumber, commands):
        while(not self.__clearToSend):
            pass
        self.__clearToSend=False
        result = self.__client.write_registers(registerNumber, commands, unit=self.__motorId)
        self.__minimumPollTimer.start()
        return result
        
    def getOperationMode(self):
        '''
        Get the current Operation MOde of the motor 
        Returns OperatingMode - see OperatingMode class for details
        '''
        result = self.__safeReadHoldingRegisters(4, 2)
        return result.registers[0]
    
    def setOperationMode(self, operationMode):
        '''
        Set the current Operation MOde of the motor 
         - see OperatingMode class for details
        '''
        commands = []
        commands.append(operationMode)
        commands.append(0)
        result = self.__safeWriteRegisters(4, commands)
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
        result = self.__safeReadHoldingRegisters(10, 2)
        return self.__getValueFromTwoRegisters(result)
        
    
    def setMaxVelocity(self, rpm):
        '''
        Set maxium velocity in RPM
        '''
        if(rpm < -2100 or rpm > 2100):
            raise ValueError('Overspeed on motor - outside specs')
        
        if(self.__reversed):
            rpm = rpm*(-1)
        
        fullRegister = Bits(int=int(rpm*100), length=32)
        highWord = Bits(bin = fullRegister[0:16].bin)
        lowWord = Bits(bin = fullRegister[16:32].bin)
        commands = []
        commands.append(lowWord.uint)
        commands.append(highWord.uint)
        result = self.__safeWriteRegisters(10, commands)
    
    def getActualVelocity(self):
        '''
        Get current actual velocity
        returns RPM
        '''
        result = self.__safeReadHoldingRegisters(24, 2)
        return self.__getValueFromTwoRegisters(result)
    
    def getTemperature(self):
        '''
        Gets the current temperature in the motor electronics in Celcius
        '''
        result = self.__safeReadHoldingRegisters(52, 2)
        return result.registers[0]*2.27
    
    def __setSubnet(self):
        oldSubnet = self.__safeReadHoldingRegisters(32776, 2)
        firstOctet = Bits(uint=255, length=8)
        secondOctet = Bits(uint=255, length=8)
        thirdOctet = Bits(uint=255, length=8)
        fourthOctet = Bits(uint=0, length=8)
    
        firstWord = BitArray(secondOctet)
        firstWord.insert(firstOctet, 0)
    
        secondWord = BitArray(fourthOctet)
        secondWord.insert(thirdOctet, 0)
        #print(secondWord.bin)
        commands = []
        commands.append(secondWord.uint)
        commands.append(firstWord.uint)
        self.__safeWriteRegisters(32776, commands)
        
    def __setAddress(self):
        oldAddress = self.__safeReadHoldingRegisters(32774,2)
        firstOctet = Bits(uint=192, length=8)
        secondOctet = Bits(uint=168, length=8)
        thirdOctet = Bits(uint=0, length=8)
        fourthOctet = Bits(uint=12, length=8)
    
        firstWord = BitArray(secondOctet)
        firstWord.insert(firstOctet, 0)
    
        secondWord = BitArray(fourthOctet)
        secondWord.insert(thirdOctet, 0)
        
        commands = []
        commands.append(secondWord.uint)
        commands.append(firstWord.uint)
        self.__safeWriteRegisters(32774, commands)
        newAddress = self.__safeReadHoldingRegisters(32774, 2)
        
    def resetModule(self):
        '''
        Reset electronics module - needs to be tested in an actual error condition
        '''
        commands = []
        commands.append(1)
        commands.append(0)
        self.__safeWriteRegisters(32798, commands)
        
    def __saveToFlash(self):
        commands = []
        commands.append(16)
        commands.append(0)
        self.__safeWriteRegisters(32798, commands)
        
    def __resetClearToSend(self):
        self.__clearToSend = True
        self.__minimumPollTimer = threading.Timer(interval=self.__miniumPollTime, function=self.__resetClearToSend)
          
        
    def __getValueFromTwoRegisters(self, registers):
        if(registers.registers[1]==65535):
            temp = 65535-registers.registers[0]
            return (temp)*-1/100
        else: 
            return registers.registers[0]/100
            