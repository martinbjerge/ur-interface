'''
Created on 5. jul. 2016

@author: MartinHuusBjerge
'''

import URBasic.dataLogging
import URBasic.rtde
import socket
import re
import numpy as np
import time

DEFAULT_TIMEOUT = 1.0

class ConnectionState:
    DISCONNECTED = 0
    CONNECTED = 1
    STARTED = 2
    PAUSED = 3


class RT_CLient(URBasic.rtde.RTDE):
    '''
    Interface to UR robot Real Time Client interface.
    For more detailes see this site:
    http://www.universal-robots.com/how-tos-and-faqs/how-to/ur-how-tos/remote-control-via-tcpip-16496/
    
    The constructor takes a UR robot hostname as input.

    Input parameters:
    host (string):  hostname or IP of UR Robot (RT CLient server)
    
    Example:
    rob = URBasic.realTimeClient.RT_CLient('192.168.56.101')
    rob.close 
    '''


    def __init__(self, host='localhost', conf_filename='rtde_configuration.xml', logger = URBasic.dataLogging.DataLogging()):
        '''
        The constructor takes a UR robot hostname as input.

        Input parameters:
        host (string):  hostname or IP of UR Robot (RT CLient server)

        Example:
        rob = URBasic.realTimeClient.RT_CLient('192.168.56.101')
        '''
        super().__init__(host, conf_filename, logger) 
        name = logger.AddEventLogging(__name__)        
        self.__logger = logger.__dict__[name]
        self.__host = host
        self.__conn_state = ConnectionState.DISCONNECTED
        self.__sock = None
        self.connect()
        self.__logger.info('RT_CLient constructor done')
        
    def connect(self):
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

        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            self.__sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)         
            self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__sock.settimeout(DEFAULT_TIMEOUT)
            self.__sock.connect((self.__host, 30003))
            self.__conn_state = ConnectionState.CONNECTED
            time.sleep(0.5)
        except (socket.timeout, socket.error):
            self.__sock = None
            self.__logger.error('Error connecting')
            raise
            return False
                
        self.__logger.info('Connected')
        return True

    def disconnect(self):
        '''
        Close the RT Client connection.

        Example:
        rob = URBasic.realTimeClient.RT_CLient('192.168.56.101')
        rob.connect()
        print(rob.is_connected())
        rob.disconnect()
        '''
        
        if self.is_running():
            self.close()
        
        if self.__sock:
            self.__sock.close()
            self.__sock = None
            self.__logger.info('Disconnected')
        self.__conn_state = ConnectionState.DISCONNECTED
        return True

    def is_connected(self):
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
        return self.__conn_state is not ConnectionState.DISCONNECTED
        
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
        
        if wait:
            if self.has_get_data_attr('output_bit_registers0_to_31'):
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

        if self.is_connected():
            prg = prg+'\n'
            self.__logger.info('Send new program to Robot:\n' + prg)
            self.__sock.send(prg.encode())
        else:
            self.__logger.warning('Send_program: Not connected to robot')
            return False

        t = time.time()
        notrun = 0
        prg = 'def resetRegister():\n  write_output_boolean_register(0, False)\n  write_output_boolean_register(1, False)\nend'
        while wait:
            ctrlBits = self.get_data('output_bit_registers0_to_31', wait=True)
            if (time.time()-t) > timeout:
                self.__logger.warning('send_program: Program timed out')
                self.send_program(prg, wait=False)
                return False
            elif (3&ctrlBits) == 0:
                self.__logger.debug('send_program: Program not started')
                notrun += 1
                if notrun > 10:
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

        
        