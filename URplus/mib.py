'''
Python 3.x library to control an UR robot through its TCP/IP interfaces
Copyright (C) 2017  Martin Huus Bjerge, Rope Robotics ApS, Denmark

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
__copyright__ = "Copyright 2017, Rope Robotics ApS, Denmark"
__license__ = "MIT License"

import URBasic
import threading
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import numpy as np


class Mib(object):
    '''
    Driver for controlling DEIF MIB 7000C electical multi meter Modbus serial
    
    Example how to use (in my case COM3):
    
    mib = URplus.mib.Mib(host='COM3')
    print(mib.GetVoltage())
    
    
    Note: If using BarinBoxes ES-313 Ethernet to serial device, 
    remember to remove the tag in port default settings that ignores the application settings.
    http://[IP]/serialport1.html
    '''
    
    
    def __init__(self, host):
        '''
        Constructor - takes the serial port of the sander
        '''
        logger = URBasic.dataLogging.DataLogging()
        name = logger.AddEventLogging(__name__,log2Consol=False)        
        self.__logger = logger.__dict__[name]
        self.client = ModbusClient(port=host, baudrate='19200', parity='N', stopbits=1, method='RTU')
        self.__serialUnit = 17
        self.__PT1 = 400
        self.__PT2 = 400
        self.__CT1 = 12
        self.__CT2 = 5
        self.__stopRunningFlag = False
        
    def close(self):
        pass
        

    def GetFrequency(self):
        return np.array(self.client.read_holding_registers(304, 1, unit=self.__serialUnit).registers)/100

    def GetVoltage(self):
        return np.array(self.client.read_holding_registers(305, 6, unit=self.__serialUnit).registers)*self.__PT1/self.__PT2/10

    def GetCurrent(self):
        return np.array(self.client.read_holding_registers(311, 3, unit=self.__serialUnit).registers)*self.__CT1/self.__CT2/1000

    def GetPower(self):
        return np.array(self.client.read_holding_registers(315, 3, unit=self.__serialUnit).registers)*self.__PT1/self.__PT2*self.__CT1/self.__CT2

    def GetEnergy(self):
        return np.array(self.client.read_holding_registers(156, 1, unit=self.__serialUnit).registers)/10
    
    def GetMaxCurrent(self):
        return np.array(self.client.read_holding_registers(1126, 3, unit=self.__serialUnit).registers)*self.__CT1/self.__CT2/1000