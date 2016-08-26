'''
Created on 7. jul. 2016

@author: MartinHuusBjerge
'''

import logging
import socket
import struct
import select
import threading

DEFAULT_TIMEOUT = 2.0

class DashBoard(threading.Thread):
    '''
    A Universal Robot can be controlled from remote by sending simple commands to the 
    GUI over a TCP/IP socket. This interface is called the "DashBoard server". 
    The server is running on port 29999 on the robots IP address.
    See more at: http://www.universal-robots.com/how-tos-and-faqs/how-to/ur-how-tos/dashboard-server-port-29999-15690/
    '''

    def __init__(self, host='localhost'):
        '''
        The constructor takes a hostname.

        Input parameters:
        host (string):  hostname or IP of RTDE server
        '''
        self.logger = logging.getLogger("DashBoard")
        self.running = False
        self._host = host
        self.last_respond = None
        self.__sock = None
        self.__conneted = False
        threading.Thread.__init__(self)
        self._dataEvent = threading.Condition()
        self._dataAccess = threading.Lock()

    def ur_load(self, file):
        '''
        Load the specified program. Return when loading has completed.
        
        Return value to Log file:
        "Loading program: <program.urp>" OR "File not found: <program.urp>"
        '''
        self.__sendall('load ' + file + '\n')

    def ur_play(self):
        '''
        Starts program, if any program is loaded and robot is ready. Return when the program execution has been started.

        Return value to Log file:
        "Starting program"
        '''
        self.__sendall('play\n')
        
    def ur_stop(self):
        '''
        Stops running program and returns when stopping is completed.
        
        Return value to Log file:
        "Stopped"
        '''
        self.__sendall('stop\n')


    def ur_pause(self):
        '''
        Pauses the running program and returns when pausing is completed.
        
        Return value to Log file:
        "Pausing program"
        '''
        self.__sendall('pause\n')


    def ur_shutdown(self):
        '''
        Shuts down and turns off robot and controller.
        
        Return value to Log file:
        "Shutting down"
        '''
        self.__sendall('shutdown\n')
        
    def ur_running(self):
        '''
        Execution state enquiry.
        
        Return value to Log file:
        "Robot running: True" OR "Robot running: False"
        '''
        self.__sendall('running\n')
        
    def ur_robotmode(self):
        '''
        Robot mode enquiry
        
        Return value to Log file:
        "Robotmode: <mode>", where <mode> is:        
        NO_CONTROLLER
        DISCONNECTED
        CONFIRM_SAFETY
        BOOTING
        POWER_OFF
        POWER_ON
        IDLE
        BACKDRIVE
        RUNNING
        '''
        self.__sendall('robotmode\n')

    def ur_get_loaded_program(self):
        '''
        Which program is loaded.
        
        Return value to Log file:
        "Program loaded: <path to loaded program file>" OR "No program loaded"
        '''
        self.__sendall('get loaded program\n')

    def ur_popup(self,  popupText=''):
        '''
        The popup-text will be translated to the selected language, if the text exists in the language file.
        
        Return value to Log file:
        "showing popup"
        '''
        self.__sendall('popup ' + popupText + '\n')

    def ur_close_popup(self):
        '''
        Closes the popup.
        
        Return value to Log file:
        "closing popup"
        '''
        self.__sendall('close popup\n')

    def ur_addToLog(self, logMessage):
        '''
        Adds log-message to the Log history.

        Return value to Log file:
        "Added log message" Or "No log message to add"
        '''
        self.__sendall('addToLog ' + logMessage + '\n')

    def ur_setUserRole(self, role):
        '''
        Simple control of user privileges: controls the available options on the Welcome screen.
        
        Return value to Log file:
        "Setting user role: <role>" OR "Failed setting user role: <role>"
        '''
        self.__sendall('setUserRole ' + role + '\n')

    def ur_isProgramSaved(self):
        '''
        Returns the save state of the active program.
        
        Return value to Log file:
        "True" OR "False"
        '''
        self.__sendall('isProgramSaved\n')

    def ur_programState(self):
        '''
        Returns the state of the active program, or STOPPED if no program is loaded.
        
        Return value to Log file:
        "STOPPED" if no program is running OR "PLAYING" if program is running
        '''
        self.__sendall('programState\n')

    def ur_polyscopeVersion(self):
        '''
        Returns the version of the Polyscope software.
        
        Return value to Log file:
        version number, like "3.0.15547"
        '''
        self.__sendall('polyscopeVersion\n')

    def ur_setUserRole_where(self, role, level):
        '''
        "setUserRole <role>, where <role> is"
        programmer = "SETUP Robot" button is disabled, "Expert Mode" is available (if correct password is supplied)
        operator = Only "RUN Program" and "SHUTDOWN Robot" buttons are enabled, "Expert Mode" cannot be activated
        none ( or send setUserRole) = All buttons enabled, "Expert Mode" is available (if correct password is supplied)
        locked = All buttons disabled and "Expert Mode" cannot be activated
        Control of user privileges: controls the available options on the Welcome screen.
        
        Note: If the Welcome screen is not active when the command is sent, 
        the user privileges defined by the new user role will not be effective 
        until the user switches to the Welcome screen.

        Return value to Log file:
        "Setting user role: <role>" OR "Failed setting user role: <role>"
        '''
        self.__sendall('setUserRole '+ role + ', where ' + role + ' is' + level +'\n')

    def ur_power_on(self):
        '''
        Powers on the robot arm.
        
        Return value to Log file:
        "Powering on"
        '''
        self.__sendall('power on\n')

    def ur_power_off(self):
        '''
        Powers off the robot arm.
        
        Return value to Log file:
        "Powering off"
        '''
        self.__sendall('power off\n')

    def ur_brake_release(self):
        '''
        Releases the brakes.
        
        Return value to Log file:
        "Brake releasing"        
        '''
        self.__sendall('brake release\n')

    def ur_safetymode(self):
        '''
        Safety mode enquiry.
        
        Return value to Log file:
        "safety mode: <mode>", where <mode> is
        
        NORMAL
        REDUCED
        PROTECTIVE_STOP
        RECOVERY
        SAFEGUARD_STOP
        SYSTEM_EMERGENCY_STOP
        ROBOT_EMERGENCY_STOP
        VIOLATION
        FAULT        
        '''
        return self.__sendall('safetymode\n')

    def ur_unlock_protective_stop(self):
        '''
        Closes the current popup and unlocks protective stop.
        
        Return value to Log file:
        "Protective stop releasing"
        '''
        self.__sendall('unlock protective stop\n')

    def ur_close_safety_popup(self):
        '''
        Closes a safety popup.
        
        Return value to Log file:
        "closing safety popup"        
        '''
        self.__sendall('close safety popup\n')

    def ur_load_installation(self, instal='default.installation'):
        '''
        Loads the specified installation file.
        
        Return value to Log file:
        "Loading installation: <default.installation>" OR "File not found: <default.installation>"
        '''
        self.__sendall('load installation '+ instal +'\n')

        
    
        
        



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
            self.__sock.connect((self._host, 29999))
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
        if self._stop_event is False:
            self._stop_event = True
            self.__conneted = False
            self.join()
        if self.__sock:
            self.__sock.close()
            self.__sock = None
        return True

    def is_running(self):
        '''
        Return True if Dash Board server is running
        '''
        return self.running

    
    def run(self):
        try:
            self._stop_event = False
            self.connect()
            while not self._stop_event:
                dat = self.__recv()
                if dat is not None:
                    self.logger.info(dat)
                self.running = True
                with self._dataEvent:
                    self._dataEvent.notifyAll()
        except:
            if self.running:
                self.running = False
                self.logger.error("Dash Board Server stopped running")
        
        self.running = False        
        with self._dataEvent:
            self._dataEvent.notifyAll()
                
    def wait(self):
        '''Wait while the data receiving thread is receiving a new message.'''
        with self._dataEvent:
            self._dataEvent.wait()
        
    def __sendall(self, cmd):
        '''
        Send command to Robot Controller. 

        Input parameters:
        cmd (str)

        Return value:
        success (boolean)
        '''
        buf = bytes(cmd, 'utf-8')
        if self.__sock is None:
            self.logger.error('Unable to send: not connected to Robot')
            return False
        
        (_, writable, _) = select.select([], [self.__sock], [], DEFAULT_TIMEOUT)
        if len(writable):
            self.__sock.sendall(buf)
            self.wait()
            return True
        else:
            self.disconnect()
            return False

    def __recv(self):
        '''
        Receive the respond a send command from the Robot Controller. 

        Return value:
        Output from Robot controller (type is depended on the input parameters)
        '''
        (readable, _, _) = select.select([self.__sock], [], [], DEFAULT_TIMEOUT)
        if len(readable):
            data = self.__sock.recv(1024)
            if len(data) == 0:
                return None
            
            fmt = ">" + str(len(data)) + "B"
            out =  struct.unpack_from(fmt, data)        
            self.last_respond = ''.join(map(chr,out[:-1]))
            return self.last_respond
            