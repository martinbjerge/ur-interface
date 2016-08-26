'''
Created on 18. jul. 2016

@author: MartinHuusBjerge
'''
import threading
import socket
import struct
import select
import logging
import numpy as np

DEFAULT_TIMEOUT = 2.0

class ForceTorqueSensor(threading.Thread):
    '''
    Interface to the Robotiq FT 300 Sensor
    http://support.robotiq.com/display/FTS2
    '''


    def __init__(self, host):
        '''
        Constructor
        '''     
        self.logger = logging.getLogger("ForceTorqueSensor")
        self.running = False
        self._host = host
        self.last_respond = None
        self.__sock = None
        self.__conneted = False
        threading.Thread.__init__(self)
        self._dataEvent = threading.Condition()
        self._dataAccess = threading.Lock()

    def get_forceTorqueSignal(self,Wait=False):
        if Wait:
            self.wait()
        return self.last_respond
    
    def connect(self):
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
            self.__sock.connect((self._host, 63351))
            self.__conneted = True
        except (socket.timeout, socket.error):
            self.__sock = None
            self.__conneted = False
            raise
            return False
        return True

    def close(self):
        '''
        Close the DashBoard connection.
        '''
        self._stop_event = True
        self.__conneted = False
        self.join()
        if self.__sock:
            self.__sock.close()
            self.__sock = None
        return True

    def is_running(self):
        '''
        Return True if Force Torque sensor data interface is running
        '''
        return self.running        


    def run(self):
        try:
            self.connect()
            self._stop_event = False
            while not self._stop_event:            
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
                    self.running = True
                else:
                    print('FT sensor data len 0 (stopped Running)')
                    self.running = False
                with self._dataEvent:
                    self._dataEvent.notifyAll()                
        except:
            if self.running:
                self.running = False
                self.logger.error("RTDE interface stopped running")
        
        self.running = False        
        with self._dataEvent:
            self._dataEvent.notifyAll()


    def wait(self):
        '''Wait while the data receiving thread is receiving a new message.'''
        with self._dataEvent:
            self._dataEvent.wait()

class ForceTorqueSensorLogger(threading.Thread):
 
    def __init__(self, demon):
        threading.Thread.__init__(self)
        self.dataLog = logging.getLogger("ForceTorqueSensor_Data_Log")
        self._stop_event = True
        self.demon = demon
           
    def close(self):
        self._stop_event = True
        self.join()
 
    def run(self):
        self._stop_event = False
        while not self._stop_event:
            self.demon.wait()
            print("Here: ",self.demon.last_respond)
            self.dataLog.info(('ForceTorqueSensor;NA;%s;%s;%s;%s;%s;%s'), *self.demon.last_respond)
        