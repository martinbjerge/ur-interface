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

import URBasic.dataLogging
import URBasic.rtde
import socket
import select
import re
import numpy as np
import time

DEFAULT_TIMEOUT = 1.0

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


class RT_CLient(URBasic.rtde.RTDE, metaclass=Singleton):
    '''
    Interface to UR robot Real Time Client interface.
    For more detailes see this site:
    http://www.universal-robots.com/how-tos-and-faqs/how-to/ur-how-tos/remote-control-via-tcpip-16496/
    
    Beside the Real Time Client, this inherits from the RTDE interface and thereby also open a 
    connection to this data interface.
    The Real Time Client in this version is only used to send program and script commands 
    to the robot, not to read data from the robot, all data reading is done via the RTDE interface.
    
    The constructor takes a UR robot hostname as input, and a RTDE configuration file, and optional a logger object.

    Input parameters:
    host (string):  hostname or IP of UR Robot (RT CLient server)
    conf_filename (string):  Path to xml file describing what channels to activate
    logger (URBasis_DataLogging obj): A instance if a logger object if common logging is needed.

    
    Example:
    rob = URBasic.realTimeClient.RT_CLient('192.168.56.101')
    self.close_rtc()
    '''


    def __init__(self, host='localhost', rtde_conf_filename='rtde_configuration.xml'):
        '''
        Constructor see class description for more info.
        '''
        super().__init__(host, rtde_conf_filename) 
        logger = URBasic.dataLogging.DataLogging()
        name = logger.AddEventLogging(__name__)        
        self.__logger = logger.__dict__[name]
        self.__host = host
        self.__conn_state = ConnectionState.DISCONNECTED
        self.__reconnectTimeout = 60
        self.__sock = None
        if self.__connect():
            self.__logger.info('RT_CLient constructor done')
        else:
            self.__logger.info('RT_CLient constructor done but not connected')
        
    def __connect(self):
        '''
        Initialize RT Client connection to host .
        
        Return value:
        success (boolean)
        
        Example:
        rob = URBasic.realTimeClient.RT_CLient('192.168.56.101')
        rob.connect()
        '''       
        if self.__sock:
            return True

        t0 = time.time()
        while (time.time()-t0<self.__reconnectTimeout) and self.__conn_state < ConnectionState.CONNECTED:
            try:
                self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
                self.__sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)         
                self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.__sock.settimeout(DEFAULT_TIMEOUT)
                self.__sock.connect((self.__host, 30003))
                self.__conn_state = ConnectionState.CONNECTED
                time.sleep(0.5)
                self.__logger.info('Connected')
                return True
            except (socket.timeout, socket.error):
                self.__sock = None
                self.__logger.error('RTC connecting')

        return False
                

    def __disconnect(self):
        '''
        Disconnect the RT Client connection.
        '''        
        if self.__sock:
            self.__sock.close()
            self.__sock = None
            self.__logger.info('Disconnected')
        self.__conn_state = ConnectionState.DISCONNECTED
        return True

    def close_rtc(self):
        '''
        Close the RT Client connection.

        Example:
        rob = URBasic.realTimeClient.RT_CLient('192.168.56.101')
        rob.close_rtc()
        '''
        if self.is_rt_client_connected():
            self.close_rtde()
            self.__disconnect()


    def is_rt_client_connected(self):
        '''
        Returns True if the connection is open.

        Return value:
        status (boolean): True if connected and False of not connected.

        Example:
        rob = URBasic.realTimeClient.RT_CLient('192.168.56.101')
        rob.connect()
        print(rob.is_connected())
        rob.disconnect()
        '''
        return self.__conn_state > ConnectionState.DISCONNECTED
        
    def send_program(self,prg='', wait=True, timeout=300.):
        '''
        Send a new command or program (string) to the UR controller. 
        The command or program will be executed as soon as it’s received by the UR controller. 
        Sending a new command or program while stop and existing running command or program and start the new one.
        The program or command will also bee modified to include some control signals to be used
        for monitoring if a program execution is successful and finished.  

        Input parameters:
        prg (string): A string containing a single command or a whole program.
        wait (bool): should this function wait for returning until the program have finished in the UR controller
        timeout (float): If the program has nor finished within this time it will be terminated and this function will return  

        Return value:
        status (boolean): True if connected and False of not connected.

        Example:
        rob = URBasic.realTimeClient.RT_CLient('192.168.56.101',logger=logger)
        rob.connect()
        rob.send_srt('set_digital_out(0, True)')
        rob.disconnect()        
        '''
        if not self.is_rt_client_connected():
            if not self.__connect():
                self.__logger.error('Send_program: Not connected to robot')
                return False
 
        
        if wait:
            if self.has_get_rtde_data_attr('output_bit_registers0_to_31'):
                def1 = prg.find('def ')
                if def1>=0:
                    prglen = len(prg)
                    prg = prg.replace('):\n', '):\n  write_output_boolean_register(0, True)\n',1)
                    if len(prg) == prglen:
                        self.__logger.warning('Send_program: Syntax error in program')
                        return False
                        
                    if (len(re.findall('def ', prg)))>1:
                        mainprg = prg[0:prg[def1+4:].find('def ')+def1+4]
                        mainPrgEnd = (np.max([mainprg.rfind('end '), mainprg.rfind('end\n')]))
                        prg = prg.replace(prg[0:mainPrgEnd], prg[0:mainPrgEnd] + '\n  write_output_boolean_register(1, True)\n',1)
                    else:
                        mainPrgEnd = prg.rfind('end')
                        prg = prg.replace(prg[0:mainPrgEnd], prg[0:mainPrgEnd] + '\n  write_output_boolean_register(1, True)\n',1)
                        
                else:
                    prg = 'def script():\n  write_output_boolean_register(0, True)\n  ' + prg + '\n  write_output_boolean_register(1, True)\nend\n'
            else:
                self.__logger.warning('Send_program: RTDE signal "output_bit_registers0_to_31" not configured')
                return False


            
        t0 = time.time()
        programSend = False
        prg = prg+'\n'
        while (time.time()-t0<self.__reconnectTimeout) and not programSend:
            try:
                (_, writable, _) = select.select([], [self.__sock], [], DEFAULT_TIMEOUT)
                if len(writable):
                    self.__sock.send(prg.encode())
                    self.__logger.info('Program send to Robot:\n' + prg)
                    programSend = True
            except:
                self.__sock = None
                self.__conn_state = ConnectionState.ERROR
                self.__logger.error('Could not send program!')
                self.__connect()                
        if not programSend:
            self.__logger.error('Program re-sending timed out - Could not send program!')
            return False

        wait_for_program_start = 10 + len(prg)/50
        t = time.time()
        notrun = 0
        prg = 'def resetRegister():\n  write_output_boolean_register(0, False)\n  write_output_boolean_register(1, False)\nend'
        while wait:
            ctrlBits = self.get_rtde_data('output_bit_registers0_to_31', wait=True)
            if (time.time()-t) > timeout:
                self.__logger.warning('send_program: Program timed out')
                self.send_program(prg, wait=False)
                return False
            elif (3&ctrlBits) == 0:
                self.__logger.debug('send_program: Program not started')
                notrun += 1
                if notrun > wait_for_program_start:
                    self.__logger.warning('send_program: Program not able to run')
                    self.send_program(prg, wait=False)
                    return False
            elif (3&ctrlBits) == 1:
                self.__logger.debug('send_program: UR running')
            elif (3&ctrlBits) == 3:
                self.__logger.info('send_program: Finished')
                self.send_program(prg, wait=False)
                time.sleep(0.1)
                return True
            else:
                self.__logger.warning('Send_program: Unknown error: ' + bin(ctrlBits))
                self.send_program(prg, wait=False)
                return False

        return True

        
        