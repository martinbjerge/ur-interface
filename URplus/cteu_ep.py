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

import time
import URBasic
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ModbusException
import rospy
from rr_elsa_controller.srv import *
from rr_elsa_controller.msg import *

class CTEU_EP(object):
    '''
    Controlling the Pneumatics on the robot via a FESTO CTEU-EP that
    is controlling a valveblock - this is via Modbus over TCP. This
    Class acts as an adapter function.
    '''
    def __init__(self, host, robotModel):
        rospy.loginfo("valveblock interface initiated")

        #Get Valve ID:
        pneu_params = rospy.get_param('/pneumatics', dict())
        self.valve_ids = [valve for subset in pneu_params.values() for valve in subset.values()]
        for i in reversed(range(len(self.valve_ids))):
            if type(self.valve_ids[i]) is list:
                self.valve_ids.extend([x for x in self.valve_ids.pop(i)])
            elif type(self.valve_ids[i]) is not int:
                self.valve_ids.pop(i)

        #Publisher
        self._valve_state             = SetValveStatus()
        self._latest_valve_status_msg = None
        self._valveblock_publisher    = rospy.Publisher('hmi/set_valveblock',SetValveStatus,queue_size=1)
        self._valveblock_subscriber   = rospy.Subscriber('hmi/get_valveblock',GetValveStatus,self._get_valve_callback,queue_size=100)

    def _get_valve_callback(self,msg):
        self._latest_valve_status_msg = msg

    def setValve(self, valveNumber, state, blocked=True):
        self._valve_state.valve_id     = int(valveNumber)
        self._valve_state.valve_state  = bool(state)
        self._valveblock_publisher.publish(self._valve_state)
        if blocked:
            while getValvePosition(valveNumber) != state:
                time.sleep(0.05)

    def getValvePosition(self, valveNumber):
        if self._latest_valve_status_msg is not None:
            states=self._latest_valve_status_msg.valve_states
            try:
                return bool(states[valveNumber])
            except ValueError as e:
                rospy.loginfo("Index: "+str(valveNumber)+" out of range")
                return None
        else:
            return None
