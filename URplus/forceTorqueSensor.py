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
import threading
import socket
import struct
import select
import logging
import time
import numpy as np

import URBasic.dataLogging

DEFAULT_TIMEOUT = 2.0

class ConnectionState:
    ERROR = 0
    DISCONNECTED = 1
    CONNECTED = 2
    PAUSED = 3
    STARTED = 4

class Singleton(type):
    _instances = {}
    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


class ForceTorqueSensor(threading.Thread, metaclass=Singleton):
    '''
    Interface to the Robotiq FT 300 Sensor
    http://support.robotiq.com/display/FTS2
    '''


    def __init__(self, host='localhost'):
        '''
        Constructor
        '''     
        self.last_respond = None
        logger = URBasic.dataLogging.DataLogging()
        name = logger.AddEventLogging(__name__)        
        self._logger = logger.__dict__[name]
        self.__host = host
        self.__reconnectTimeout = 60 #Seconds (while in run)

        self.__conn_state = ConnectionState.DISCONNECTED
        self.__sock = None
        threading.Thread.__init__(self)
        self.__dataEvent = threading.Condition()
        self.__dataAccess = threading.Lock()
        self.start()
        self.__dataLogObj = ForceTorqueSensorLogger(self,logger)
        self.wait_ft()
        self._logger.info('FT constructor done')


    def get_forceTorqueSignal(self,Wait=False):
        if Wait:
            self.wait_ft()
        return self.last_respond
    
    def __connect(self):
        '''
        Initialize DashBoard connection to host.
        
        Return value:
        success (boolean)
        '''       
        if self.__sock:
            return True

        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            self.__sock.setblocking(0)
            self.__sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)         
            self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__sock.settimeout(DEFAULT_TIMEOUT)
            self.__sock.connect((self.__host, 63351))
            self.__conn_state = ConnectionState.CONNECTED
        except (socket.timeout, socket.error):
            self.__sock = None
            self.__conn_state = ConnectionState.ERROR
            return False
        return True

    def close_ft(self):
        '''
        Close the connection to the force torque sensor.
        '''
        self.__dataLogObj.close_ftLog()
        self.__stop_event = True
        self.join()
        if self.__sock:
            self.__sock.close()
            self.__sock = None
        self.__conn_state = ConnectionState.DISCONNECTED
        return True

    def is_running(self):
        '''
        Return True if Force Torque sensor data interface is running
        '''
        return self.__conn_state >= ConnectionState.STARTED        


    def run(self):
        t0 = time.time()
        self.__stop_event = False
        while (time.time()-t0<self.__reconnectTimeout) and self.__conn_state < ConnectionState.CONNECTED:
            if not self.__connect():
                self._logger.warning("FT connection failed!")

        if self.__conn_state < ConnectionState.CONNECTED:
            self._logger.error("FT interface not able to connect and timed out!")
            return

        while (not self.__stop_event) and (time.time()-t0<self.__reconnectTimeout):
            try:
                # Read Data:
                (readable, _, _) = select.select([self.__sock], [], [], DEFAULT_TIMEOUT)
                tmpstr=''
                if len(readable):
                    continue_recv = True
                    while continue_recv:
                        out = struct.unpack_from('>B',self.__sock.recv(1))
                        tmpstr += chr(out[0]) 
                        if tmpstr[-1] == ')':
                            continue_recv = False
                    self.last_respond = np.array([float(x) for x in tmpstr[1:-1].split(' , ')]) 

                    #Notify that new data have been read 
                    with self.__dataEvent:
                        self.__dataEvent.notifyAll()
                    t0 = time.time()
                    self.__conn_state = ConnectionState.STARTED

                else:
                    self.__conn_state = ConnectionState.ERROR
                
            except Exception:
                if self.__conn_state >= ConnectionState.CONNECTED:
                    self.__conn_state = ConnectionState.ERROR
                    self._logger.error("FT interface stopped running")

                    try:
                        self.__sock.close()
                    except:
                        pass
                    self.__sock = None
                    self.__connect()

                if self.__conn_state >= ConnectionState.CONNECTED:
                    self._logger.info("FT interface reconnected")
                else:
                    self._logger.warning("FT reconnection failed!")

        self.__conn_state = ConnectionState.PAUSED
        with self.__dataEvent:
            self.__dataEvent.notifyAll()
        self._logger.info("FT interface is stopped")
        
    def wait_ft(self):
        '''Wait while the data receiving thread is receiving a new data set.'''
        cnt = 0
        while self.__conn_state < ConnectionState.STARTED:
            time.sleep(1)
            cnt +=1
            if cnt>5:
                self._logger.warning('wait_ft timed out while FT interface not running')
                return False
            
        with self.__dataEvent:
            self.__dataEvent.wait()
        return True

class ForceTorqueSensorLogger(threading.Thread):
 
    def __init__(self, ft_obj, logger = URBasic.dataLogging.DataLogging()):
        threading.Thread.__init__(self)
        name = logger.AddDataLogging(__name__)
        self.__dataLogger = logger.__dict__[name]
        self.__stop_event = True
        self.__ftDemon = ft_obj
        self.start()
        self.__ftDemon._logger.info('ForceTorqueSensorLogger constructor done')
           
    def close_ftLog(self):
        self.__stop_event = True
        self.join()
 
    def run(self):
        self.__stop_event = False
        t = time.time()
        while not self.__stop_event:
            if self.__ftDemon.wait_ft():
                self.__dataLogger.info(('ForceTorqueSensor;%s;%s;%s;%s;%s;%s;%s'), (time.time()-t), *self.__ftDemon.last_respond)
        