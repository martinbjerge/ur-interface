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
import URBasic.urScript
import URBasic.dashboard
import xml.etree.ElementTree as ET
import os.path

class UrScriptExt(URBasic.urScript.UrScript):
    '''
    Interface to remote access UR script commands, and add some extended features as well.
    For more details see the script manual at this site:
    http://www.universal-robots.com/download/
    
    Beside the implementation of the script interface, this class also inherits from the 
    Real Time Client and RTDE interface and thereby also open a connection to these data interfaces.
    The Real Time Client in this version is only used to send program and script commands 
    to the robot, not to read data from the robot, all data reading is done via the RTDE interface.
    
    This class also opens a connection to the UR Dashboard server and enables you to 
    e.g. reset error and warnings from the UR controller.
    
    The constructor takes a UR robot hostname as input, and a RTDE configuration file, and optional a logger object.
    
    Input parameters:
    host (string):  hostname or IP of UR Robot (RT CLient server)
    rtde_conf_filename (string):  Path to xml file describing what channels to activate
    logger (URBasis_DataLogging obj): A instance if a logger object if common logging is needed.
    
    
    Example:
    rob = URBasic.urScriptExt.UrScriptExt('192.168.56.101', rtde_conf_filename='rtde_configuration.xml')
    self.close_rtc()
    '''


    def __init__(self, host='localhost', rtde_conf_filename='rtde_configuration.xml', hw_Profile_filename='HwProfiles.xml', profile='UR5'):
        '''
        Constructor see class description for more info.
        '''
        super().__init__(host, rtde_conf_filename)        
        logger = URBasic.dataLogging.DataLogging()
        name = logger.AddEventLogging(__name__)        
        self.__logger = logger.__dict__[name]
        self.dbh_demon = URBasic.dashboard.DashBoard(host)
        self.hwProfile = HardwareProfile(profile, hw_Profile_filename )
        self.__logger.info('Init done')
        
    def close_urScriptExt(self):
        self.close_rtc()
        self.dbh_demon.close_dbs()
        
    def send_program(self, prg='', wait=True, timeout=300.):
        status =  URBasic.urScript.UrScript.send_program(self, prg=prg, wait=wait, timeout=timeout)
        if not prg == 'def resetRegister():\n  write_output_boolean_register(0, False)\n  write_output_boolean_register(1, False)\nend':
            if self.get_safety_status()['StoppedDueToSafety']:
                return False
            else:
                return status
        
        return True
    
    def reset_error(self):
        '''
        Check if the UR controller is powered on and ready to run.
        If controller isn’t power on it will be power up. 
        If there is a safety error, it will be tried rest it once.

        Return Value:
        state (boolean): True of power is on and no safety errors active.
        
        '''
        
        if not self.get_robot_status()['PowerOn']:
            self.dbh_demon.ur_power_on()
            self.dbh_demon.wait_dbs()
            self.dbh_demon.ur_brake_release()
            self.dbh_demon.wait_dbs()
        if self.get_safety_status()['StoppedDueToSafety']:
            self.dbh_demon.ur_unlock_protective_stop()
            self.dbh_demon.wait_dbs()
            self.dbh_demon.ur_close_safety_popup()
            self.dbh_demon.wait_dbs()
            self.dbh_demon.ur_brake_release()
            self.dbh_demon.wait_dbs()
            
        return self.get_robot_status()['PowerOn'] & (not self.get_safety_status()['StoppedDueToSafety'])
            
    def get_in(self, port, wait=True):
        '''
        Get input signal level
        
        Parameters:
        n: Hardware profile tag
        
        Return Value:
        boolean, The signal level.
        '''
        if 'BCI' == port[:3]:
            return self.get_conﬁgurable_digital_in(int(port[4:]), wait)
        elif 'BDI' == port[:3]:
            return self.get_standard_digital_in(int(port[4:]), wait)
        elif 'BAI' == port[:3]:
            return self.get_standard_analog_in(int(port[4:]), wait)
    
    def get_safety_status(self):
        '''
        Return the safety state of the UR robot as a dict.
        
        Bits 0-10: 
        0:  Is normal mode
        1:  Is reduced mode
        2:  Is protective stopped
        3:  Is recovery mode
        4:  Is safeguard stopped
        5:  Is system emergency stopped
        6:  Is robot emergency stopped
        8:  Is emergency stopped
        9:  Is violation
        10: Is fault
        11: Is stopped due to safety
        '''
        
        SafetyState = { 'NormalMode'             : False, 
                        'ReducedMode'            : False, 
                        'ProtectiveStopped'      : False, 
                        'RecoveryMode'           : False, 
                        'SafeguardStopped'       : False, 
                        'SystemEmergencyStopped' : False, 
                        'RobotEmergencyStopped'  : False,
                        'EmergencyStopped'       : False,
                        'Violation'              : False,
                        'Fault'                  : False,
                        'StoppedDueToSafety'     : False}
         
        statbit = self.get_rtde_data('safety_status_bits', wait=True)
        if statbit is None:
            return None 
        
        if statbit & (1 << 0):
            SafetyState['NormalMode'] = True
        if statbit & (1 << 1):
            SafetyState['ReducedMode'] = True
        if statbit & (1 << 2):
            SafetyState['ProtectiveStopped'] = True
        if statbit & (1 << 3):
            SafetyState['RecoveryMode'] = True
        if statbit & (1 << 4):
            SafetyState['SafeguardStopped'] = True
        if statbit & (1 << 5):
            SafetyState['SystemEmergencyStopped'] = True
        if statbit & (1 << 6):
            SafetyState['RobotEmergencyStopped'] = True
        if statbit & (1 << 7):
            SafetyState['EmergencyStopped'] = True
        if statbit & (1 << 8):
            SafetyState['Violation'] = True
        if statbit & (1 << 9):
            SafetyState['Fault'] = True
        if statbit & (1 << 10):
            SafetyState['StoppedDueToSafety'] = True

        return SafetyState
        

    def get_robot_status(self):
        '''
        Return the robot state of the UR robot as a dict.
        
        Bits 0-3: 
        0:  Is power on
        1:  Is program running
        2:  Is teach button pressed
        3:  Is power button pressed
        '''
        
        RobotState = { 'PowerOn'            : False, 
                        'ProgramRunning'     : False, 
                        'TeachButtonPressed' : False, 
                        'PowerButtonPressed' : False}
         
        statbit = self.get_rtde_data('robot_status_bits', wait=True)
        if statbit is None:
            return None 
        
        if statbit & (1 << 0):
            RobotState['PowerOn'] = True
        if statbit & (1 << 1):
            RobotState['ProgramRunning'] = True
        if statbit & (1 << 2):
            RobotState['TeachButtonPressed'] = True
        if statbit & (1 << 3):
            RobotState['PowerButtonPressed'] = True

        return RobotState



class HardwareProfile():
    '''
    Load a hardware / IO profile of a robot
    '''


    def __init__(self, profile, hw_Profile_filename='HwProfiles.xml'):
        '''
        Constructor
        '''
        logger = URBasic.dataLogging.DataLogging()
        name = logger.AddEventLogging(__name__)        
        self.__logger = logger.__dict__[name]
        self.__HwProfilesFile = hw_Profile_filename
        self.loadHwProfile(profile)
        self.__logger.info('Init done')

        
    def loadHwProfile(self, profile):
        if not os.path.isfile(self.__HwProfilesFile):        
            self._logger.error("Configuration file don't exist : " + self.__HwProfilesFile)
            return False
        
        tree = ET.parse(self.__HwProfilesFile)
        root = tree.getroot()
        
        #setup data that can be send
        prof = root.find(profile)
        if prof is None:
            self.__logger.error('Hardware profile not found')
            return False
        
        for modu in prof:
            if modu is not None:
                for child in modu:
                    self.__dict__[child.attrib['use']] = (modu.tag + '_' + child.attrib['id'])
                    if modu.tag[-1] == 'O':
                        self.__dict__['safeState_' + child.attrib['use']] = (child.attrib['safeState'])
                            

        
