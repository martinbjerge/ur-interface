'''
Created on 5. jul. 2016

@author: MartinHuusBjerge
'''

import threading
import socket
import struct
import logging
import numpy as np

DEFAULT_TIMEOUT = 1.0

class ConnectionState:
    DISCONNECTED = 0
    CONNECTED = 1
    STARTED = 2
    PAUSED = 3


class RT_CLient(threading.Thread):
    '''
    Interface to UR robot Real Time Client interface.
    For more detailes see this site:
    http://www.universal-robots.com/how-tos-and-faqs/how-to/ur-how-tos/remote-control-via-tcpip-16496/
    
    The constructor takes a UR robot hostname as input.

    Input parameters:
    host (string):  hostname or IP of UR Robot (RT CLient server)
    
    Example:
    rob = RT_CLient('192.168.56.101')
    rob.close 
    '''


    def __init__(self, host='localhost'):
        '''
        The constructor takes a UR robot hostname as input.

        Input parameters:
        host (string):  hostname or IP of UR Robot (RT CLient server)

        Example:
        rob = RT_CLient('192.168.56.101')
        '''
        self.__logger = logging.getLogger("rtde")
        self.__running = False
        self.__host = host
        self.__stop_event = True
        threading.Thread.__init__(self)
        self.__dataEvent = threading.Condition()
        self.__dataAccess = threading.Lock()
        self.__conn_state = ConnectionState.DISCONNECTED
        self.__sock = None
        
    def connect(self):
        '''
        Initialize RT Client connection to host .
        
        Return value:
        success (boolean)
        
        Example:
        rob = RT_CLient('192.168.56.101')
        rob.connect()
        '''       
        if self.__sock:
            return True

        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            self.__sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)         
            self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__sock.settimeout(DEFAULT_TIMEOUT)
            self.__sock.connect((self.__host, 30003))
            self.__conn_state = ConnectionState.CONNECTED
        except (socket.timeout, socket.error):
            self.__sock = None
            raise
            return False
                
        return True

    def disconnect(self):
        '''
        Close the RT Client connection.

        Example:
        rob = RT_CLient('192.168.56.101')
        rob.connect()
        print(rob.is_connected())
        rob.disconnect()
        '''
        if self.__sock:
            self.__sock.close()
            self.__sock = None
        self.__conn_state = ConnectionState.DISCONNECTED
        return True

    def is_connected(self):
        '''
        Returns True if the connection is open.

        Return value:
        status (boolean): True if connected and False of not connected.

        Example:
        rob = RT_CLient('192.168.56.101')
        rob.connect()
        print(rob.is_connected())
        rob.disconnect()
        '''
        return self.__conn_state is not ConnectionState.DISCONNECTED
        
    def send_srt(self,str=''):
        
    
    def is_running(self):
        '''
        Return True if RT Client interface is running 
        '''
        return self.__running
    
        