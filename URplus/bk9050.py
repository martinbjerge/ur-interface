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

class BK9050(object):
    '''
    Controlling the additional inputs and outputs on the robot
    This class is setup to use the Beckhoff-BK9050 model via Modbus over TCP
    '''
    def __init__(self, host):
        '''
        Constructor takes the ip address off the BK9050 box
        '''
        if host is None: #Only for enable code completion
            self.connected = False
            return

        self._client = ModbusClient(host=host)
        self._client.write_register(0x1120, 0)      #Turn off watchdog
        self.connected = self._client.connect()

    def getAnalogInputs(self):
        '''
        Get the raw value of all the analog inputs at once in raw
        registers and values
        '''
        reading = self._client.read_holding_registers(0x0000, 16)
        result  = [0 for i in range(8)]
        for x in range(0,8):
            result[x] = self._getValueFromReading(reading=reading.registers[x*2+1])
        return result

    def getAnalogInput(self,inputNumber):
        '''
        Get the value of an analog input by input number 0 to 7
        Returns a value in mA or V depening on InputRange set on port
        note - currently only tested with range 4-20mA
        '''
        result = self._client.read_holding_registers(0x0000+inputNumber*2+1)
        return self._getValueFromReading(reading=result.registers[0])

    def setRelay(self,inputNumber,state):
        '''
        Set the state of a relay
        '''
        return self._client.write_coil(inputNumber, state)

    def getRelay(self,inputNumber,state):
        '''
        Get the state of a relay
        '''
        return self._client.read_coil(inputNumber)

    def _getValueFromReading(self,reading):
        '''
        Convert raw value to V
        '''
        convert_ratio = 10.0/np.power(2,15)
        return convert_ratio*reading

    def close(self):
        self._client.close()
