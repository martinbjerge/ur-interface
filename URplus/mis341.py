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
    This class is running a MIS341 motor via Modbus over to TCP
    '''
    Mode_Reg = 2
    P_SOLL = 3
    V_SOLL = 5
    P_IST = 10
    V_IST = 12
    STATUSBITS = 25
    TEMP = 26
    ERR_BITS = 35
    WARN_BITS = 36
    STARTMODE = 37
    
    SETUP_BITS = 124    #Direction can be inversed here
    
    
    
    def __init__(self, host, motorId=1, reversed=False):
        '''
        Constructor - takes comport and the motorId configured in the motor
        '''
        logger = URBasic.dataLogging.DataLogging()
        name = logger.AddEventLogging(__name__,log2Consol=False)        
        self.__logger = logger.__dict__[name]
        self.__motorId = motorId
        self.__client = ModbusClient(host=host)
        self.__reversed = reversed
        self.__miniumPollTime = 0.004  # see 7.2.5 in ethernet user guide for motor
        self.__clearToSend = True
        self.__minimumPollTimer = threading.Timer(interval=self.__miniumPollTime, function=self.__resetClearToSend)
        
        
    
        
    def getOperationMode(self):
        '''
        Get the current Operation MOde of the motor 
        Returns OperatingMode - see OperatingMode class for details
        '''
        result = self.__safeReadHoldingRegisters(MIS341.Mode_Reg*2, 2)
        return result.registers[0]
    
    def setOperationMode(self, operationMode):
        '''
        Set the current Operation MOde of the motor 
         - see OperatingMode class for details
        '''
        commands = []
        commands.append(operationMode)
        commands.append(0)
        result = self.__safeWriteRegisters(MIS341.Mode_Reg*2, commands)
        #print(result.function_code)
    
    def getDesiredPosition(self):
        result = self.__safeReadHoldingRegisters(MIS341.P_SOLL*2, 2)
        return self.__getValueFromTwoRegisters(result.registers)
    
    def setDesiredPosition(self, position):
        commands = self.__getTwoRegistersFromValue(position)
        result = self.__safeWriteRegisters(MIS341.P_SOLL*2, commands)
    
    def getMaxVelocity(self):
        '''
        Get the currently configured MaxVelocity
        returns RPM
        '''
        result = self.__safeReadHoldingRegisters(MIS341.V_SOLL*2, 2)
        return self.__getValueFromTwoRegisters(result)/100
        
    
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
        result = self.__safeWriteRegisters(MIS341.V_SOLL*2, commands)
    
    def stopInPosition(self):
        self.setMaxVelocity(0)
        time.sleep(1)
        actualPosition = self.getActualPosition()
        self.setDesiredPosition(actualPosition)
        self.setOperationMode(OperatingMode.Position)
        self.setMaxVelocity(50)
    
    def getStatus(self):
        result = self.__safeReadHoldingRegisters(MIS341.STATUSBITS*2, 2)
        bitArray = BitArray(uint = result.registers[0], length=16)
        if(bitArray[14]):
            print("Status - Motor " + str(self.__motorId) + " Auto Correction Active")
        if(bitArray[13]):
            print("Status - Motor " + str(self.__motorId) + " In Physical Position")
        if(bitArray[12]):
            print("Status - Motor " + str(self.__motorId) + " At velocity")
        if(bitArray[11]):
            print("Status - Motor " + str(self.__motorId) + " In Position")
        if(bitArray[10]):
            print("Status - Motor " + str(self.__motorId) + " Accelerating")
        if(bitArray[9]):
            print("Status - Motor " + str(self.__motorId) + " Decelerating")
        if(bitArray[12]):
            print("Status - Motor " + str(self.__motorId) + " General Error")
        
    
    def getWarnings(self):
        result = self.__safeReadHoldingRegisters(MIS341.WARN_BITS*2, 2)
        bitArray = BitArray(uint = result.registers[0], length=16)
        if(bitArray[15]):
            print("Warning - Motor " + str(self.__motorId) + " Positive limit Active")
        if(bitArray[14]):
            print("Warning - Motor " + str(self.__motorId) + " Negative limit Active")
        if(bitArray[13]):
            print("Warning - Motor " + str(self.__motorId) + " Positive limit has been Active")
        if(bitArray[12]):
            print("Warning - Motor " + str(self.__motorId) + " Negative limit has been Active")
        if(bitArray[11]):
            print("Warning - Motor " + str(self.__motorId) + " Low Bus Voltage")
        if(bitArray[14]):
            print("Warning - Motor " + str(self.__motorId) + " Temperature has been above 80C")
    
    
    def getErrors(self):
        result = self.__safeReadHoldingRegisters(MIS341.ERR_BITS*2, 2)
        bitArray = BitArray(uint = result.registers[0], length=16)
        if(bitArray[15]):
            print("Error - Motor " + str(self.__motorId) + " General Error")
        if(bitArray[13]):
            print("Error - Motor " + str(self.__motorId) + " Output driver Error - Output is short circuited")
        if(bitArray[12]):
            print("Error - Motor " + str(self.__motorId) + " Position Limit Error")
        if(bitArray[11]):
            print("Error - Motor " + str(self.__motorId) + " Low bus voltage Error")
        if(bitArray[10]):
            print("Error - Motor " + str(self.__motorId) + " Over voltage Error")
        if(bitArray[9]):
            print("Error - Motor " + str(self.__motorId) + " Temperature too high (above 90C)")
        if(bitArray[8]):
            print("Error - Motor " + str(self.__motorId) + " Internal Error")
        if(bitArray[7]):
            print("Error - Motor " + str(self.__motorId) + " Encoder Lost position")
    
    
    def getActualVelocity(self):
        '''
        Get current actual velocity
        returns RPM
        '''
        result = self.__safeReadHoldingRegisters(MIS341.V_IST*2, 2)
        return self.__getValueFromTwoRegisters(result)/100
    
    def getTemperature(self):
        '''
        Gets the current temperature in the motor electronics in Celcius
        '''
        result = self.__safeReadHoldingRegisters(MIS341.TEMP*2, 2)
        return result.registers[0]*2.27
    
    def resetControlModule(self):
        '''
        Reset electronics module - needs to be tested in an actual error condition
        '''
        commands = []
        commands.append(1)
        commands.append(0)
        self.__safeWriteRegisters(32798, commands)
    
    def resetMotorAndControlModule(self):
        '''
        Reset both motor and electronics module in one call - needs to be tested in an actual error condition
        '''
        commands = []
        commands.append(257)
        commands.append(0)
        self.__safeWriteRegisters(32798, commands)
    
    def __getStartMode(self):
        pass
    
    def __setStartMode(self):
        pass
    
    def getActualPosition(self):
        result = self.__safeReadHoldingRegisters(MIS341.P_IST*2, 2)
        return self.__getValueFromTwoRegisters(result.registers)
    
    '''
    def __getTargetPosition(self):
        result = self.__safeReadHoldingRegisters(MIS341.P_SOLL*2, 2)
        return self.__getValueFromTwoRegisters(result.registers)
    
    def __setTargetPosition(self, position):
        commands = []
        commands.append(position)   #todo - must fix two registers
        commands.append(0)
        self.__safeWriteRegisters(MIS341.P_SOLL*2, commands)
    '''
    
    def __reverseDirection(self):
        pass
        
        
        
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
        
    
        
    def __saveToFlash(self):
        commands = []
        commands.append(16)
        commands.append(0)
        self.__safeWriteRegisters(32798, commands)
        
    def __resetClearToSend(self):
        self.__clearToSend = True
        self.__minimumPollTimer = threading.Timer(interval=self.__miniumPollTime, function=self.__resetClearToSend)
    
    def __getTwoRegistersFromValue(self, value):
        commands = []
        value = int(value)
        b = Bits(int=value, length=32)
        
        lowWord = Bits(bin = b[16:32].bin)
        commands.append(lowWord.uint)
        
        highWord = Bits(bin = b[0:16].bin)
        commands.append(highWord.uint) 
        return commands      
        
    def __getValueFromTwoRegisters(self, registers):
        #if(registers.registers[1]==65535):
        #    temp = 65535-registers.registers[0]
        #    return (temp)*-1/100
        #else: 
        #    return registers.registers[0]/100
        lowWord = BitArray(uint=registers[0], length=16)
        highWord = BitArray(uint=registers[1], length=16)
        total = BitArray(lowWord)
        total.insert(highWord, 0)
        return total.int
            
