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


    def __init__(self, host='localhost', rtde_conf_filename='rtde_configuration.xml'):
        '''
        Constructor see class description for more info.
        '''
        super().__init__(host, rtde_conf_filename)        
        logger = URBasic.dataLogging.DataLogging()
        name = logger.AddEventLogging(__name__)        
        self.__logger = logger.__dict__[name]
        self.dbh_demon = URBasic.dashboard.DashBoard(host)
        self.__logger.info('Init done')
        
    def close_urScriptExt(self):
        self.close_rtc()
        self.dbh_demon.close_dbs()
        
    def send_program(self, prg='', wait=True, timeout=300.):
        status =  URBasic.urScript.UrScript.send_program(self, prg=prg, wait=wait, timeout=timeout)
        if not prg == 'def resetRegister():\n  write_output_boolean_register(0, False)\n  write_output_boolean_register(1, False)\nend':
            self.dbh_demon.ur_safetymode()
            self.dbh_demon.wait_dbs()
            if self.dbh_demon.last_respond != 'Safetymode: NORMAL':
                return False
            else:
                return status
        
        return True
    
    def reset_error(self):
        self.dbh_demon.ur_robotmode()
        self.dbh_demon.wait_dbs()
        if self.dbh_demon.last_respond != 'Robotmode: RUNNING': #  'Robotmode: POWER_OFF': 
            self.dbh_demon.ur_power_on()
            self.dbh_demon.wait_dbs()
            self.dbh_demon.ur_brake_release()
            self.dbh_demon.wait_dbs()
        self.dbh_demon.ur_safetymode()
        self.dbh_demon.wait_dbs()
        if self.dbh_demon.last_respond != 'Safetymode: NORMAL':
            self.dbh_demon.ur_unlock_protective_stop()
            self.dbh_demon.wait_dbs()
            self.dbh_demon.ur_close_safety_popup()
            self.dbh_demon.wait_dbs()
            self.dbh_demon.ur_brake_release()
            self.dbh_demon.wait_dbs()

        
