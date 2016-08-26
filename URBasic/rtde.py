'''
Created on 5. jul. 2016

@author: MartinHuusBjerge
'''

import threading
import socket
import struct
import select
import logging
import numpy as np
import xml.etree.ElementTree as ET
from ctypes.wintypes import UINT

DEFAULT_TIMEOUT = 1.0

class Command:
    RTDE_REQUEST_PROTOCOL_VERSION = 86        # ascii V
    RTDE_GET_URCONTROL_VERSION = 118          # ascii v
    RTDE_TEXT_MESSAGE = 77                    # ascii M
    RTDE_DATA_PACKAGE = 85                    # ascii U
    RTDE_CONTROL_PACKAGE_SETUP_OUTPUTS = 79   # ascii O
    RTDE_CONTROL_PACKAGE_SETUP_INPUTS = 73    # ascii I
    RTDE_CONTROL_PACKAGE_START = 83           # ascii S
    RTDE_CONTROL_PACKAGE_PAUSE = 80           # ascii P


class ConnectionState:
    DISCONNECTED = 0
    CONNECTED = 1
    STARTED = 2
    PAUSED = 3


class RTDE(threading.Thread):
    '''
    Interface to UR robot Real Time Data Exchange interface.
    For more detailes see this site:
    http://www.universal-robots.com/how-tos-and-faqs/how-to/ur-how-tos/real-time-data-exchange-rtde-guide-22229/ 
    '''


    def __init__(self, host='localhost', conf_filename='rtde_configuration.xml'):
        '''
        The constructor takes a hostname.

        Input parameters:
        host (string):  hostname or IP of RTDE server
        '''
        self.logger = logging.getLogger("rtde")
        self.data = DataObject()
        self.running = False
        self.__dataSend = DataObject()
        self.__conf_filename = conf_filename
        self._host = host
        self._stop_event = True
        threading.Thread.__init__(self)
        self._dataEvent = threading.Condition()
        self._dataAccess = threading.Lock()
        self.__conn_state = ConnectionState.DISCONNECTED
        self.__sock = None
        self.__output_config = None
        self.__input_config = {}
        self.__buf = bytes()


    def connect(self):
        '''
        Initialize RTDE connection to host and set up data interfaces based on configuration XML.
        
        Return value:
        success (boolean)
        '''       
        if self.__sock:
            return True

        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            self.__sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)         
            self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__sock.settimeout(DEFAULT_TIMEOUT)
            self.__sock.connect((self._host, 30004))
            self.__conn_state = ConnectionState.CONNECTED
        except (socket.timeout, socket.error):
            self.__sock = None
            raise
            return False
        
        try:        
            self.get_controller_version()
            if not self.negotiate_protocol_version(1):
                self.logger.error('Unable to negotiate protocol version')
                raise
    
        except (socket.timeout, socket.error):
            self.__sock = None
            raise
            return False        
        
        return True

    def disconnect(self):
        '''
        Close the RTDE connection.
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
        open (boolean)
        '''
        return self.__conn_state is not ConnectionState.DISCONNECTED
        
    def is_running(self):
        '''
        Return True if RTDE interface is running 
        '''
        return self.running
    
    def get_controller_version(self):
        '''
        Returns the software version of the robot controller running the RTDE server.

        Return values:        
        major (int)
        minor (int)
        bugfix (int)
        '''
        cmd = Command.RTDE_GET_URCONTROL_VERSION
        (major, minor, bugfix, build) = self.__sendAndReceive(cmd)
        if major and minor and bugfix:
            self.logger.info('Controller version: ' + str(major) + '.' + str(minor) + '.' + str(bugfix) + '-' + str(build))
            if major <= 3 and minor <= 2 and bugfix < 19171:
                self.logger.error("Please upgrade your controller to minimally version 3.2.19171")
                self.stop()
            return major, minor, bugfix
        return None, None, None

    def negotiate_protocol_version(self, protocol):
        '''
        Negotiate the protocol version with the server. 
        Returns True if the controller supports the specified protocol version. 
        We recommend that you use this to ensure full compatibility between your 
        application and future versions of the robot controller.

        Input parameters:        
        protocol (int): protocol version number
        
        Return value:
        success (boolean)
        '''
        cmd = Command.RTDE_REQUEST_PROTOCOL_VERSION
        payload = struct.pack('>H',protocol)
        return bool(self.__sendAndReceive(cmd, payload))
    
    def send_input_setup(self, variables=None, types=[], initValues=None):
        '''
        Configure an input package that the external(this) application will send to the robot controller. 
        An input package is a collection of input variables that the external application will provide 
        to the robot controller in a single update. Variables is a list of variable names and should be 
        a subset of the names supported as input by the RTDE interface.The list of types is optional, 
        but if any types are provided it should have the same length as the variables list. 
        The provided types will be matched with the types that the RTDE interface expects and the 
        function returns None if they are not equal. Multiple input packages can be configured. 
        The returned InputObject has a reference to the recipe id which is used to identify the 
        specific input format when sending an update.
        If variables is empty, xml configuration file is used.

        Input parameters:
        variables (list<string> or Str): [Optional] Variable names from the list of possible RTDE inputs
        types (list<string> or str): [Optional] Types matching the variables
        
        Return value:        
        success (boolean)
        '''
        
        if variables is None:        
            tree = ET.parse(self.__conf_filename)
            root = tree.getroot()

            #setup data that can be send
            recive = root.find('send')
            variables = []
            initValues = []
            for child in recive:
                variables.append(child.attrib['name'])
                initValues.append(float(child.attrib['initValue']))
        
        cmd = Command.RTDE_CONTROL_PACKAGE_SETUP_INPUTS
        if type(variables) is list:
            payload = ','.join(variables)
        elif type(variables) is str:
            payload = variables
        else:
            self.logger.error('Variables must be list of stings or a single string, variables is: ' + str(type(variables)))
            return None
        
        payload = bytes(payload, 'utf-8')
        result = self.__sendAndReceive(cmd, payload)
        if len(types)!=0 and not self.__list_equals(result.types, types):
            self.logger.error('Data type inconsistency for input setup: ' +
                     str(types) + ' - ' +
                     str(result.types))
            return None
        result.names = variables
        self.__input_config[result.id] = result
        self.__dataSend = DataObject.create_empty(variables, result.id)
        if initValues is not None:
            for ii in range(len(variables)):
                if 'UINT8' == result.types[ii]:
                    self.set_data(variables[ii], int(initValues[ii]))
                elif 'UINT32' == result.types[ii]:
                    self.set_data(variables[ii], int(initValues[ii]))
                elif 'INT32' == result.types[ii]:
                    self.set_data(variables[ii], int(initValues[ii]))
                elif 'DOUBLE' == result.types[ii]:
                    self.set_data(variables[ii], (initValues[ii]))
                else:
                    self.logger.error('Unknown data type')
        return True
 
    def send_output_setup(self, variables=None, types=[]):
        '''
        Configure an output package that the robot controller will send to the 
        external(this) application at the control frequency. Variables is a list of 
        variable names and should be a subset of the names supported as output by the 
        RTDE interface. The list of types is optional, but if any types are provided 
        it should have the same length as the variables list. The provided types will 
        be matched with the types that the RTDE interface expects and the function 
        returns False if they are not equal. Only one output package format can be 
        specified and hence no recipe id is used for output.
        If variables is empty, xml configuration file is used.

        Input parameters:        
        variables (list<string> or str): [Optional] Variable names from the list of possible RTDE outputs 
        types (list<string> or str): [Optional] Types matching the variables
        
        Return value:        
        success (boolean)
        '''
        
        if variables is None:        
            tree = ET.parse(self.__conf_filename)
            root = tree.getroot()

            #Setup data to be recived
            recive = root.find('receive')
            variables = []
            for child in recive:
                variables.append(child.attrib['name'])

        
        cmd = Command.RTDE_CONTROL_PACKAGE_SETUP_OUTPUTS
        if type(variables) is list:
            payload = ','.join(variables)
        elif type(variables) is str:
            payload = variables
        else:
            self.logger.error('Variables must be list of stings or a single string, variables is: ' + str(type(variables)))
            return None
        
        payload = bytes(payload, 'utf-8')
        result = self.__sendAndReceive(cmd, payload)
        if len(types)!=0 and not self.__list_equals(result.types, types):
            self.logger.error('Data type inconsistency for output setup: ' +
                     str(types) + ' - ' +
                     str(result.types))
            return False
        result.names = variables
        self.__output_config = result
        return True

    def send_start(self):
        '''
        Sends a start command to the RTDE server to initiate the actual synchronization. 
        Setup of all inputs and outputs should be done before starting the synchronization.

        Return value:
        success (boolean)
        '''
        cmd = Command.RTDE_CONTROL_PACKAGE_START
        success = self.__sendAndReceive(cmd)
        if success:
            self.logger.info('RTDE synchronization started')
            self.__conn_state = ConnectionState.STARTED
        else:
            self.logger.error('RTDE synchronization failed to start')
        return success
        
    def send_pause(self):
        '''
        Sends a pause command to the RTDE server to pause the synchronization. 
        When paused it is possible to change the input and output configurations 
        and start the synchronization again.

        Return value:
        success (boolean)
        '''
        cmd = Command.RTDE_CONTROL_PACKAGE_PAUSE
        success = self.__sendAndReceive(cmd)
        if success:
            self.logger.info('RTDE synchronization paused')
            self.__conn_state = ConnectionState.PAUSED
        else:
            self.logger.error('RTDE synchronization failed to pause')
        return success

    def send(self):
        '''
        Send the contents of a DataObject as input to the RTDE server. 
        Returns True if successful.
                
        Return value:
        success (boolean)
        '''
        if self.__conn_state != ConnectionState.STARTED:
            self.logger.error('Cannot send when RTDE synchronization is inactive')
            return
        if not (self.__dataSend.recipe_id in self.__input_config):
            self.logger.error('Input configuration id not found: ' + str(self.__dataSend.recipe_id))
            return
        config = self.__input_config[self.__dataSend.recipe_id]
        return self.__sendall(Command.RTDE_DATA_PACKAGE, config.pack(self.__dataSend))

    def receive(self):
        '''
        Blocking call to receive next output DataObject from RTDE server.

        Return value:        
        output_data (DataObject): object with member variables matching the names of the configured RTDE variables
        '''
        if self.__output_config is None:
            self.logger.error('Output configuration not initialized')
            return None
        if self.__conn_state != ConnectionState.STARTED:
            self.logger.error('Cannot receive when RTDE synchronization is inactive')
            return None
        return self.__recv(Command.RTDE_DATA_PACKAGE)

    def has_get_data_attr(self,name):
        '''
        Check if RTDE interface is configured with a given variable name.
        
        Input parameter:
        name (str): Name of variable to check.
        '''
        return hasattr(self.data, name)

    def get_data(self, variable_name, wait=False):
        '''
        Get data from RTDE data stream when thread is running
        
        Input parameters:
        variable_name (str):  Variable name from the list of possible RTDE outputs 
        wait (boolean): Wait for next value, default value is False
        
        Return value:        
        output_data (???): Variable(s) matching the names of the requested RTDE variables
        '''
        if not self._stop_event:
            if wait:
                self.wait()
            if self.has_get_data_attr(variable_name):
                return np.array(self.data.__dict__[variable_name])
        return None

    def has_set_data_attr(self,name):
        '''
        Check if RTDE interface is configured with a given variable name.
        
        Input parameter:
        name (str): Name of variable to check.
        '''
        return hasattr(self.__dataSend, name)
    
    def set_data(self, variable_name, value):
        '''
        Set data to be send to the UR controller by the send/recive thread.
        Object is locked while updating to avoid sending half updated values,
        hence send all values as to lists of equal lengths 
        
        Input parameters:
        variable_name (List/str):  Variable name from the list of possible RTDE inputs
        value (list/int/double) 
        
        Return value:        
        Status (Bool): True=Data sucesfull updated, False=Data not updated         
        '''
        
        #check if input is list of equal length
        if type(variable_name) is list:
            if type(variable_name) != type(value):
                return False
            if len(variable_name) != len(value):
                return False
            
            for ii in range(len(value)):
                if self.has_set_data_attr(variable_name[ii]):
                    self.__dataSend.__dict__[variable_name[ii]] = value[ii]
                else:
                    return False
        
        else:
            if hasattr(self.__dataSend, variable_name):
                self.__dataSend.__dict__[variable_name] = value
            else:
                return False
        
        return True
    
    def __sendAndReceive(self, cmd, payload=bytes()):
        '''
        Send command and data (payload) to Robot Controller 
        and receive the respond from the Robot Controller. 

        Input parameters:
        cmd (int)
        payload (bytes)

        Return value(s):
        Output from Robot controller (type is depended on the input parameters)

        '''
        if self.__sendall(cmd, payload):
            return self.__recv(cmd)
        else:
            return None
        
    def __sendall(self, command, payload=bytes()):
        '''
        Send command and data (payload) to Robot Controller 
        and receive the respond from the Robot Controller. 

        Input parameters:
        cmd (int)
        payload (bytes)

        Return value:
        success (boolean)
        '''
        fmt = '>HB'
        size = struct.calcsize(fmt) + len(payload)
        buf = struct.pack(fmt, size, command) + payload
        if self.__sock is None:
            self.logger.error('Unable to send: not connected to Robot')
            return False
        
        (_, writable, _) = select.select([], [self.__sock], [], DEFAULT_TIMEOUT)
        if len(writable):
            self.__sock.sendall(buf)
            return True
        else:
            self.__trigger_disconnected()
            return False

    def __recv(self, command):
        '''
        Receive the respond a send command from the Robot Controller. 

        Input parameters:
        cmd (int)

        Return value(s):
        Output from Robot controller (type is depended on the input parameters)
        '''
        while self.is_connected():
            (readable, _, _) = select.select([self.__sock], [], [], DEFAULT_TIMEOUT)
            if len(readable):
                more = self.__sock.recv(4096)
                if len(more) == 0:
                    self.__trigger_disconnected()
                    return None
                self.__buf +=  more
                
            # unpack_from requires a buffer of at least 3 bytes
            while len(self.__buf) >= 3:
                #Get the packed header
                (size, command) = struct.unpack_from('>HB', self.__buf)

                # Attempts to extract a packet
                if len(self.__buf) >= size:
                    packet, self.__buf = self.__buf[3:size], self.__buf[size:]
                    data = self.__on_packet(command, packet)
                    if command == command and len(self.__buf) == 0:
                        return data
                    if command == command and len(self.__buf) != 0:
                        self.logger.info('skipping package')
                else:
                    break
        return None

    def __trigger_disconnected(self):
        self.logger.info("RTDE disconnected")
        self.disconnect() #clean-up

    def __on_packet(self, cmd, payload):
        '''
        Interpret the data received from the Robot Controller
        Based on the command returned from the Robot Controller different interoperation methods is selected. 

        Input parameters:
        cmd (int)
        payload (bytes)

        Return value(s):
        Output from Robot controller (type is depended on the cmd value)
        '''
        if cmd == Command.RTDE_REQUEST_PROTOCOL_VERSION:
            if len(payload) != 1:
                self.logger.error('RTDE_REQUEST_PROTOCOL_VERSION: Wrong payload size')
                return None
            return struct.unpack_from('>B', payload)[0]
        
        elif cmd == Command.RTDE_GET_URCONTROL_VERSION:
            if 12 == len(payload):
                return np.append(np.array(struct.unpack_from('>III', payload)), 0)
            elif 16 == len(payload):
                return np.array(struct.unpack_from('>IIII', payload))
            else:
                self.logger.error('RTDE_GET_URCONTROL_VERSION: Wrong payload size')
                return None

        
        elif cmd == Command.RTDE_TEXT_MESSAGE:
            if len(payload) < 1:
                self.logger.error('RTDE_TEXT_MESSAGE: No payload')
                return None
            EXCEPTION_MESSAGE = 0
            ERROR_MESSAGE = 1
            WARNING_MESSAGE = 2
            INFO_MESSAGE = 3
            fmt = ">" + str(len(payload)) + "B"
            out = struct.unpack_from(fmt, payload)
            level = out[0]
            message = ''.join(map(chr,out[1:])) 
            if(level == EXCEPTION_MESSAGE or 
               level == ERROR_MESSAGE):
                self.logger.error('Server message: ' + message)
            elif level == WARNING_MESSAGE:
                self.logger.warning('Server message: ' + message)
            elif level == INFO_MESSAGE:
                self.logger.info('Server message: ' + message)
     
        elif cmd == Command.RTDE_CONTROL_PACKAGE_SETUP_OUTPUTS:
            if len(payload) < 1:
                self.logger.error('RTDE_CONTROL_PACKAGE_SETUP_OUTPUTS: No payload')
                return None
            has_recipe_id = False
            output_config = DataConfig.unpack_recipe(payload, has_recipe_id)
            return output_config

        elif cmd == Command.RTDE_CONTROL_PACKAGE_SETUP_INPUTS:
            if len(payload) < 1:
                self.logger.error('RTDE_CONTROL_PACKAGE_SETUP_INPUTS: No payload')
                return None
            has_recipe_id = True
            input_config = DataConfig.unpack_recipe(payload, has_recipe_id)
            return input_config
            
        elif cmd == Command.RTDE_CONTROL_PACKAGE_START:
            if len(payload) != 1:
                self.logger.error('RTDE_CONTROL_PACKAGE_START: Wrong payload size')
                return None
            return bool(struct.unpack_from('>B', payload)[0])
        
        elif cmd == Command.RTDE_CONTROL_PACKAGE_PAUSE:
            if len(payload) != 1:
                self.logger.error('RTDE_CONTROL_PACKAGE_PAUSE: Wrong payload size')
                return None
            return bool(struct.unpack_from('>B', payload)[0])

        elif cmd == Command.RTDE_DATA_PACKAGE:            
            if self.__output_config is None:
                self.logger.error('RTDE_DATA_PACKAGE: Missing output configuration')
                return None
            output = self.__output_config.unpack(payload)
            return output
        
        else:
            self.logger.error('Unknown package command: ' + chr(cmd))


    def __list_equals(self, l1, l2):
        if len(l1) != len(l2):
            return False
        for i in range(len((l1))):
            if l1[i] != l2[i]:
                return False
        return True


    '''Threading Data receive'''
    def close(self):
        if self._stop_event is False:
            self._stop_event = True
            self.wait()
            self.disconnect()
            self.join()
        
    def run(self):
        try:
            self._stop_event = False
            self.connect()
            self.send_output_setup()
            self.send_input_setup()
            self.send_start()
    
            while not self._stop_event:
                self.data = self.receive()
                self.running = True
                with self._dataEvent:
                    self._dataEvent.notifyAll()
            self.disconnect()
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
            #self.logger.warn('Error in RTDE run - Error type: %s', type(inst))
            #self.logger.warn('Error in RTDE run - Error msg: %s', inst)
            if self.running:
                self.running = False
                self.logger.error("RTDE interface stopped running")
         
        self.running = False        
        with self._dataEvent:
            self._dataEvent.notifyAll()
                

    def wait(self):
        '''Wait while the data receiving thread is receiving a new data set.'''
        with self._dataEvent:
            self._dataEvent.wait()



class DataConfig(object):
    __slots__ = ['id', 'names', 'types', 'fmt']
    @staticmethod
    def unpack_recipe(buf, has_recipe_id):
        rmd = DataConfig();
        if has_recipe_id:
            rmd.id = struct.unpack_from('>B', buf)[0]
            fmt = ">" + str(len(buf)) + "B"
            buf = struct.unpack_from(fmt, buf)
            buf = ''.join(map(chr,buf[1:])) 
            rmd.types = buf.split(',')
            rmd.fmt = '>B'
        else:
            fmt = ">" + str(len(buf)) + "B"
            buf = struct.unpack_from(fmt, buf)
            buf = ''.join(map(chr,buf[:])) 
            rmd.types = buf.split(',')
            rmd.fmt = '>'
        for i in rmd.types:
            if i=='INT32':
                rmd.fmt += 'i'
            elif i=='UINT32':
                rmd.fmt += 'I'
            elif i=='VECTOR6D':
                rmd.fmt += 'd'*6
            elif i=='VECTOR3D':
                rmd.fmt += 'd'*3
            elif i=='VECTOR6INT32':
                rmd.fmt += 'i'*6
            elif i=='VECTOR6UINT32':
                rmd.fmt += 'I'*6
            elif i=='DOUBLE':
                rmd.fmt += 'd'
            elif i=='UINT64':
                rmd.fmt += 'Q'
            elif i=='UINT8':
                rmd.fmt += 'B'
            elif i=='IN_USE':
                raise ValueError('An input parameter is already in use.')
            else:
                raise ValueError('Unknown data type: ' + i)
        return rmd
        
    def pack(self, state):
        l = state.pack(self.names, self.types)
        return struct.pack(self.fmt, *l)

    def unpack(self, data):
        li =  struct.unpack_from(self.fmt, data)
        return DataObject.unpack(li, self.names, self.types)

class DataObject(object):
    '''
    Data container for data send to or received from the Robot Controller.
    The Object will have attributes for each of that data tags received or send.
    e.g.  obj.actual_digital_output_bits
    '''
    recipe_id = None
    def pack(self, names, types):
        if len(names) != len(types):
            raise ValueError('List sizes are not identical.')
        l = []
        if(self.recipe_id is not None):
            l.append(self.recipe_id)
        for i in range(len(names)):
            if self.__dict__[names[i]] is None:
                raise ValueError('Uninitialized parameter: ' + names[i])
            if types[i].startswith('VECTOR'):
                l.extend(self.__dict__[names[i]])
            else:
                l.append(self.__dict__[names[i]])
        return l
    
    @staticmethod
    def unpack(data, names, types):
        if len(names) != len(types):
            raise ValueError('List sizes are not identical.')
        obj = DataObject()
        offset = 0
        for i in range(len(names)):
            obj.__dict__[names[i]] = DataObject.unpack_field(data, offset, types[i])
            offset += DataObject.get_item_size(types[i])
        return obj

    @staticmethod
    def create_empty(names, recipe_id):
        obj = DataObject()
        for i in range(len(names)):
            obj.__dict__[names[i]] = None
        obj.recipe_id = recipe_id
        return obj

    @staticmethod
    def get_item_size(data_type):
        if data_type.startswith('VECTOR6'):
            return 6
        elif data_type.startswith('VECTOR3'):
            return 3
        return 1

    @staticmethod
    def unpack_field(data, offset, data_type):
        size = DataObject.get_item_size(data_type)
        if(data_type == 'VECTOR6D' or
           data_type == 'VECTOR3D'):
            return np.array([float(data[offset+i]) for i in range(size)])
        elif(data_type == 'VECTOR6UINT32'):
            return np.array([int(data[offset+i]) for i in range(size)])
        elif(data_type == 'DOUBLE'):
            return float(data[offset])
        elif(data_type == 'UINT32' or
             data_type == 'UINT64'):
            return int(data[offset])
        elif(data_type == 'VECTOR6INT32'):
            return np.array([int(data[offset+i]) for i in range(size)])
        elif(data_type == 'INT32' or
             data_type == 'UINT8'):
            return int(data[offset])
        raise ValueError('unpack_field: unknown data type: ' + data_type)
    
    
class URRTDElogger(RTDE, threading.Thread):
 
    def __init__(self, rtdemon):
        threading.Thread.__init__(self)
        self.dataLog = logging.getLogger("RTDE_Data_Log")
        self._stop_event = True
        self.rtdemon = rtdemon
         
    def logdata(self):
        self.rtdemon.wait()        
        for tagname in self.rtdemon.data.__dict__.keys():
            if tagname != 'timestamp':
                tp = type(self.rtdemon.data.__dict__[tagname])
                if tp is np.ndarray:
                    if 6==len(self.rtdemon.data.__dict__[tagname]):
                        self.dataLog.info((tagname+';%s;%s;%s;%s;%s;%s;%s'), self.rtdemon.data.__dict__['timestamp'], *self.rtdemon.data.__dict__[tagname])
                    elif 3==len(self.rtdemon.data.__dict__[tagname]):
                        self.dataLog.info((tagname+';%s;%s;%s;%s'), self.rtdemon.data.__dict__['timestamp'], *self.rtdemon.data.__dict__[tagname])
                    else:
                        self.rtdemon.logger.warning('Logger data unexpected type in rtde.py - class URRTDElogger - def logdata Type: ' + str(tp) + ' - Len: ' + str(len(self.rtdemon.data.__dict__[tagname])))
                elif tp is bool or tp is float or tp is int: 
                    self.dataLog.info((tagname+';%s;%s'), self.rtdemon.data.__dict__['timestamp'], self.rtdemon.data.__dict__[tagname])
                else:
                    self.rtdemon.logger.warning('Logger data unexpected type in rtde.py - class URRTDElogger - def logdata Type: ' + str(tp))
                    
    def close(self):
        if self._stop_event is False:
            self._stop_event = True
            self.join()
 
    def run(self):
        self._stop_event = False
        while not self._stop_event:
            self.logdata()
