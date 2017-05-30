# coding: latin-1
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

__author__ = "Steffen Østergaard Jacobsen"
__copyright__ = "Copyright 2017, Rope Robotics ApS, Denmark"
__license__ = "MIT License"


from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import numpy as np

class BECKHOFF(object):
    '''
    Controlling the additional inputs and outputs on the robot
    This class is setup to use the Beckhoff-BC9050 model via Modbus over TCP
    '''
    def __init__(self, host):
        '''
        Constructor takes the ip address off the BC9050 box
        '''
        if host is None: #Only for enable code completion
            self.connected = False
            return
        self.__client = ModbusClient(host=host)
        self.connected = self.__client.connect()

    def getAnalogInputs(self):
        '''
        Get the raw value of all the analog inputs at once in raw
        registers and values
        '''

        result = self.__client.read_holding_registers(0x4000, 8)
        for x in range(0,8):
            result.registers[x] = self.__getValueFromReading(reading=result.registers[x])
        return result.registers

    def getAnalogInput(self, inputNumber):
        '''
        Get the value of an analog input by input number 0 to 7
        Returns a value in mA or V depening on InputRange set on port
        note - currently only tested with range 4-20mA
        '''
        result = self.__client.read_holding_registers(0x4000+inputNumber)
        return self.__getValueFromReading(reading=result.registers[0])

    def __getValueFromReading(self,reading):
        '''
        Convert raw value to V
        '''

        convert_ratio = 10.0/np.power(2,15)
        return convert_ratio*reading
