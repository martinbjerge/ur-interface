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

import URBasic
import numpy as np
import time

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


    def __init__(self, host, robotModel, hasForceTorque=False):
        super().__init__(host, robotModel, hasForceTorque)        
        logger = URBasic.dataLogging.DataLogging()
        name = logger.AddEventLogging(__name__)        
        self.__logger = logger.__dict__[name]
        self.__force_remote_set=False
        self.print_actual_tcp_pose()
        self.print_actual_joint_positions()
        self.__logger.info('Init done')
        
    def close(self):
        self.print_actual_tcp_pose()
        self.print_actual_joint_positions()
        self.robotConnector.close()
        
    def send_program(self, prg='', wait=True, timeout=300.):
        self.__force_remote_set=False
        #status =  URBasic.urScript.UrScript.send_program(self, prg=prg, wait=wait, timeout=timeout)
        self.robotConnector.RealTimeClient.SendProgram(prg)
        while(self.robotConnector.RobotModel.RuntimeState != 1):
            pass
        
        if self.robotConnector.RobotModel.SafetyStatus.StoppedDueToSafety:
            return False
        else:
            return True
                #return status
        
        
    
    def reset_error(self):
        '''
        Check if the UR controller is powered on and ready to run.
        If controller isn’t power on it will be power up. 
        If there is a safety error, it will be tried rest it once.

        Return Value:
        state (boolean): True of power is on and no safety errors active.
        
        '''
        
        if not self.robotConnector.RobotModel.RobotStatus().PowerOn:
            #self.robotConnector.DashboardClient.PowerOn()
            self.robotConnector.DashboardClient.ur_power_on()
            self.robotConnector.DashboardClient.wait_dbs()
            #self.robotConnector.DashboardClient.BrakeRelease()
            self.robotConnector.DashboardClient.ur_brake_release()
            self.robotConnector.DashboardClient.wait_dbs()
            time.sleep(2)
        if self.robotConnector.RobotModel.SafetyStatus().StoppedDueToSafety:         #self.get_safety_status()['StoppedDueToSafety']:
            #self.robotConnector.DashboardClient.UnlockProtectiveStop()
            self.robotConnector.DashboardClient.ur_unlock_protective_stop()
            self.robotConnector.DashboardClient.wait_dbs()
            #self.robotConnector.DashboardClient.CloseSafetyPopup()
            self.robotConnector.DashboardClient.ur_close_safety_popup()
            self.robotConnector.DashboardClient.wait_dbs()
            #self.robotConnector.DashboardClient.BrakeRelease()
            self.robotConnector.DashboardClient.ur_brake_release()
            self.robotConnector.DashboardClient.wait_dbs()
            time.sleep(2)
            
        #return self.get_robot_status()['PowerOn'] & (not self.get_safety_status()['StoppedDueToSafety'])
        return self.robotConnector.RobotModel.RobotStatus().PowerOn & (not self.robotConnector.RobotModel.SafetyStatus().StoppedDueToSafety)
            
    def get_in(self, port, wait=True):
        '''
        Get input signal level
        
        Parameters:
        port (HW profile str): Hardware profile tag
        wait (bool): True if wait for next RTDE sample, False, to get the latest sample
        
        Return Value:
        out (bool or float), The signal level.
        '''
        if 'BCI' == port[:3]:
            return self.get_conﬁgurable_digital_in(int(port[4:]), wait)
        elif 'BDI' == port[:3]:
            return self.get_standard_digital_in(int(port[4:]), wait)
        elif 'BAI' == port[:3]:
            return self.get_standard_analog_in(int(port[4:]), wait)

    def set_output(self, port, value):
        '''
        Get output signal level
        
        Parameters:
        port (HW profile str): Hardware profile tag
        value (bool or float): The output value to be set 
        
        Return Value:
        Status (bool): Status, True if signal set successfully.
        '''
        
        if 'BCO' == port[:3]:
            self.set_conﬁgurable_digital_out(int(port[4:]), value)
        elif 'BDO' == port[:3]:
            self.set_standard_digital_out(int(port[4:]), value)
        elif 'BAO' == port[:3]:
            pass
        elif 'TDO' == port[:3]:
            pass

            #if self.send_rtde_data():
            #    return True
            return True #Vi har sendt det .. vi checker ikke
        else:
            return False


    def init_force_remote(self, task_frame=[0.0, 0.0, 0.0,  0.0, 0.0, 0.0], f_type=2):
        '''
        The Force Remote function enables changing the force settings dynamically, 
        without sending new programs to the robot, and thereby exit and enter force mode again. 
        As the new settings are send via RTDE, the force can be updated every 8ms.
        This function initializes the remote force function, 
        by sending a program to the robot that can receive new force settings.  
        
        See "force_mode" for more details on force functions
        
        Parameters:
        task_frame (6D-vector): Initial task frame (can be changed via the update function)
        f_type (int): Initial force type (can be changed via the update function)
        
        Return Value:
        Status (bool): Status, True if successfully initialized.
        ''' 
        
        self.force_mode       
        if not self.rtde_is_running():
            self.__logger.error('RTDE need to be running to use force remote')
            return False
            
        rtde_input_check = True
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_int_register_0')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_int_register_1')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_int_register_2')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_int_register_3')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_int_register_4')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_int_register_5')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_int_register_6')
        
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_0')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_1')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_2')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_3')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_4')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_5')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_6')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_7')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_8')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_9')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_10')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_11')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_12')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_13')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_14')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_15')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_16')
        rtde_input_check = rtde_input_check and self.has_set_rtde_data_attr('input_double_register_17')
        
        if not rtde_input_check:
            self.__logger.error('RTDE is not configured to have all the needed input registeres needed')
            return False
        selection_vector=[0, 0, 0,  0, 0, 0]
        wrench=[0.0, 0.0, 0.0,  0.0, 0.0, 0.0]
        limits=[0.1, 0.1, 0.1,  0.1, 0.1, 0.1]

        self.set_rtde_data('input_int_register_0', selection_vector[0])
        self.set_rtde_data('input_int_register_1', selection_vector[1])
        self.set_rtde_data('input_int_register_2', selection_vector[2])
        self.set_rtde_data('input_int_register_3', selection_vector[3])
        self.set_rtde_data('input_int_register_4', selection_vector[4])
        self.set_rtde_data('input_int_register_5', selection_vector[5])
        
        self.set_rtde_data('input_double_register_0', wrench[0])
        self.set_rtde_data('input_double_register_1', wrench[1])
        self.set_rtde_data('input_double_register_2', wrench[2])
        self.set_rtde_data('input_double_register_3', wrench[3])
        self.set_rtde_data('input_double_register_4', wrench[4])
        self.set_rtde_data('input_double_register_5', wrench[5])

        self.set_rtde_data('input_double_register_6', limits[0])
        self.set_rtde_data('input_double_register_7', limits[1])
        self.set_rtde_data('input_double_register_8', limits[2])
        self.set_rtde_data('input_double_register_9', limits[3])
        self.set_rtde_data('input_double_register_10', limits[4])
        self.set_rtde_data('input_double_register_11', limits[5])

        self.set_rtde_data('input_double_register_12', task_frame[0])
        self.set_rtde_data('input_double_register_13', task_frame[1])
        self.set_rtde_data('input_double_register_14', task_frame[2])
        self.set_rtde_data('input_double_register_15', task_frame[3])
        self.set_rtde_data('input_double_register_16', task_frame[4])
        self.set_rtde_data('input_double_register_17', task_frame[5])
        
        self.set_rtde_data('input_int_register_6', f_type)
        self.send_rtde_data()
        
        prog='''def force_remote():
    while (True):

        global task_frame =  p[read_input_float_register(12), 
                              read_input_float_register(13),
                              read_input_float_register(14),
                              read_input_float_register(15),
                              read_input_float_register(16),
                              read_input_float_register(17)]


        global selection_vector = [ read_input_integer_register(0),
                                    read_input_integer_register(1),
                                    read_input_integer_register(2),
                                    read_input_integer_register(3),
                                    read_input_integer_register(4),
                                    read_input_integer_register(5)]
        
        global wrench = [ read_input_float_register(0), 
                          read_input_float_register(1),
                          read_input_float_register(2),
                          read_input_float_register(3),
                          read_input_float_register(4),
                          read_input_float_register(5)]
        
        global limits = [ read_input_float_register(6), 
                          read_input_float_register(7),
                          read_input_float_register(8),
                          read_input_float_register(9),
                          read_input_float_register(10),
                          read_input_float_register(11)]
                          
        global f_type = read_input_integer_register(6)

        force_mode(task_frame, selection_vector, wrench, f_type , limits)
        sync()
    end
end
'''
        prog = prog.format(**locals())  
        self.send_program(prog, wait=False)
        self.__force_remote_set=True
        return True
    
    def set_force_remote(self, task_frame=[0.0, 0.0, 0.0,  0.0, 0.0, 0.0], selection_vector=[0, 0, 0,  0, 0, 0], wrench=[0.0, 0.0, 0.0,  0.0, 0.0, 0.0], limits=[0.1, 0.1, 0.1,  0.1, 0.1, 0.1],f_type=2):
        '''
        Update/set remote force, see "init_force_remote" for more details.
                       
        Parameters:
        task frame: A pose vector that deﬁnes the force frame relative to the base frame.
        
        selection vector: A 6d vector that may only contain 0 or 1. 1 means that the robot will be
                          compliant in the corresponding axis of the task frame, 0 means the robot is
                          not compliant along/about that axis.

        wrench: The forces/torques the robot is to apply to its environment. These values
                have different meanings whether they correspond to a compliant axis or not.
                Compliant axis: The robot will adjust its position along/about the axis in order
                to achieve the speciﬁed force/torque. Non-compliant axis: The robot follows
                the trajectory of the program but will account for an external force/torque
                of the speciﬁed value.

        limits: A 6d vector with ﬂoat values that are interpreted differently for
                compliant/non-compliant axes: 
                Compliant axes: The limit values for compliant axes are the maximum
                                allowed tcp speed along/about the axis. 
                Non-compliant axes: The limit values for non-compliant axes are the
                                    maximum allowed deviation along/about an axis between the
                                    actual tcp position and the one set by the program.

        f_type: An integer specifying how the robot interprets the force frame. 
                1: The force frame is transformed in a way such that its y-axis is aligned with a vector
                   pointing from the robot tcp towards the origin of the force frame. 
                2: The force frame is not transformed. 
                3: The force frame is transformed in a way such that its x-axis is the projection of
                   the robot tcp velocity vector onto the x-y plane of the force frame. 
                All other values of f_type are invalid.

        Return Value:
        Status (bool): Status, True if parameters successfully updated.
        '''
        
        
        if self.rtde_is_running() and self.__force_remote_set:
            self.set_rtde_data('input_int_register_0', selection_vector[0])
            self.set_rtde_data('input_int_register_1', selection_vector[1])
            self.set_rtde_data('input_int_register_2', selection_vector[2])
            self.set_rtde_data('input_int_register_3', selection_vector[3])
            self.set_rtde_data('input_int_register_4', selection_vector[4])
            self.set_rtde_data('input_int_register_5', selection_vector[5])
            
            self.set_rtde_data('input_double_register_0', wrench[0])
            self.set_rtde_data('input_double_register_1', wrench[1])
            self.set_rtde_data('input_double_register_2', wrench[2])
            self.set_rtde_data('input_double_register_3', wrench[3])
            self.set_rtde_data('input_double_register_4', wrench[4])
            self.set_rtde_data('input_double_register_5', wrench[5])

            self.set_rtde_data('input_double_register_6', limits[0])
            self.set_rtde_data('input_double_register_7', limits[1])
            self.set_rtde_data('input_double_register_8', limits[2])
            self.set_rtde_data('input_double_register_9', limits[3])
            self.set_rtde_data('input_double_register_10', limits[4])
            self.set_rtde_data('input_double_register_11', limits[5])
            
            self.set_rtde_data('input_double_register_12', task_frame[0])
            self.set_rtde_data('input_double_register_13', task_frame[1])
            self.set_rtde_data('input_double_register_14', task_frame[2])
            self.set_rtde_data('input_double_register_15', task_frame[3])
            self.set_rtde_data('input_double_register_16', task_frame[4])
            self.set_rtde_data('input_double_register_17', task_frame[5])
            
            self.set_rtde_data('input_int_register_6', f_type)
            
            self.send_rtde_data()
            return True
            
        else:
            if self.__force_remote_set:
                self.__logger.warning('Force Remote not initialized')
            else:
                self.__logger.warning('RTDE is not running')
            
            return False


    def move_force_2stop(self,  start_tolerance=0.01, 
                                stop_tolerance=0.01, 
                                wrench_gain=[1.0, 1.0, 1.0,  1.0, 1.0, 1.0], 
                                timeout=10, 
                                task_frame=[0.0, 0.0, 0.0,  0.0, 0.0, 0.0], 
                                selection_vector=[0, 0, 0,  0, 0, 0], 
                                wrench=[0.0, 0.0, 0.0,  0.0, 0.0, 0.0], 
                                limits=[0.1, 0.1, 0.1,  0.1, 0.1, 0.1],
                                f_type=2):
        '''
        Move force will set the robot in force mode (see force_mode) and move the TCP until it meets an object making the TCP stand still.

        Parameters:
        start_tolerance (float): sum of all elements in a pose vector defining a robot has started moving (60 samples)

        stop_tolerance (float): sum of all elements in a pose vector defining a standing still robot (60 samples)

        wrench_gain (6D vector): Gain multiplied with wrench each 8ms sample  
        
        timeout (float): Seconds to timeout if tolerance not reached        
        
        task frame: A pose vector that defines the force frame relative to the base frame.
        
        selection vector: A 6d vector that may only contain 0 or 1. 1 means that the robot will be
                          compliant in the corresponding axis of the task frame, 0 means the robot is
                          not compliant along/about that axis.

        wrench: The forces/torques the robot is to apply to its environment. These values
                have different meanings whether they correspond to a compliant axis or not.
                Compliant axis: The robot will adjust its position along/about the axis in order
                to achieve the specified force/torque. Non-compliant axis: The robot follows
                the trajectory of the program but will account for an external force/torque
                of the specified value.

        limits: A 6d vector with float values that are interpreted differently for
                compliant/non-compliant axes: 
                Compliant axes: The limit values for compliant axes are the maximum
                                allowed tcp speed along/about the axis. 
                Non-compliant axes: The limit values for non-compliant axes are the
                                    maximum allowed deviation along/about an axis between the
                                    actual tcp position and the one set by the program.

        f_type: An integer specifying how the robot interprets the force frame. 
                1: The force frame is transformed in a way such that its y-axis is aligned with a vector
                   pointing from the robot tcp towards the origin of the force frame. 
                2: The force frame is not transformed. 
                3: The force frame is transformed in a way such that its x-axis is the projection of
                   the robot tcp velocity vector onto the x-y plane of the force frame. 
                All other values of f_type are invalid.

        Return Value:
        Status (bool): Status, True if signal set successfully.
        
        ''' 
        
        timeoutcnt = 125*timeout
        wrench = np.array(wrench)
        wrench_gain = np.array(wrench_gain)
        self.init_force_remote(task_frame, f_type)
        self.set_force_remote(task_frame, selection_vector, wrench, limits, f_type)
        
        dist = np.array(range(60),float)
        dist.fill(0.)
        cnt = 0        
        old_pose=self.get_actual_tcp_pose()*np.array(selection_vector)
        while np.sum(dist)<start_tolerance and cnt<timeoutcnt:  
            new_pose = self.get_actual_tcp_pose()*np.array(selection_vector)
            wrench = wrench*wrench_gain #Need a max wrencd check
            self.set_force_remote(task_frame, selection_vector, wrench, limits, f_type)
            dist[np.mod(cnt,60)] = np.abs(np.sum(new_pose-old_pose))
            old_pose=new_pose
            cnt +=1
        
        #Check if robot started to move
        if cnt<timeoutcnt:
            dist.fill(stop_tolerance)
            cnt = 0        
            while np.sum(dist)>stop_tolerance and cnt<timeoutcnt:  
                new_pose = self.get_actual_tcp_pose()*np.array(selection_vector)
                dist[np.mod(cnt,60)] = np.abs(np.sum(new_pose-old_pose))
                old_pose=new_pose
                cnt +=1
        
        self.set_force_remote(task_frame, selection_vector, [0,0,0, 0,0,0], limits, f_type)
        self.end_force_mode()
        if cnt>=timeoutcnt:
            return False
        else:
            return True


    def move_force(self, pose=None, 
                         a=1.2, 
                         v=0.25, 
                         t=0,
                         r=0.0, 
                         movetype='l',
                         task_frame=[0.0, 0.0, 0.0,  0.0, 0.0, 0.0], 
                         selection_vector=[0, 0, 0,  0, 0, 0], 
                         wrench=[0.0, 0.0, 0.0,  0.0, 0.0, 0.0], 
                         limits=[0.1, 0.1, 0.1,  0.1, 0.1, 0.1],
                         f_type=2,
                         wait=True,
                         q=None):   
                                     
        """
        Concatenate several move commands and applies a blending radius
        pose or q is a list of pose or joint-pose, and apply a force in a direction
        
        Parameters:
        pose: list of target pose (pose can also be speciﬁed as joint
              positions, then forward kinematics is used to calculate the corresponding pose see q)

        a:    tool acceleration [m/sˆ2]

        v:    tool speed [m/s]
        
        t:    time [S]

        r:    blend radius [m]

        movetype: (str): 'j', 'l', 'p', 'c'
                
        task frame: A pose vector that defines the force frame relative to the base frame.
        
        selection vector: A 6d vector that may only contain 0 or 1. 1 means that the robot will be
                          compliant in the corresponding axis of the task frame, 0 means the robot is
                          not compliant along/about that axis.

        wrench: The forces/torques the robot is to apply to its environment. These values
                have different meanings whether they correspond to a compliant axis or not.
                Compliant axis: The robot will adjust its position along/about the axis in order
                to achieve the specified force/torque. Non-compliant axis: The robot follows
                the trajectory of the program but will account for an external force/torque
                of the specified value.

        limits: A 6d vector with float values that are interpreted differently for
                compliant/non-compliant axes: 
                Compliant axes: The limit values for compliant axes are the maximum
                                allowed tcp speed along/about the axis. 
                Non-compliant axes: The limit values for non-compliant axes are the
                                    maximum allowed deviation along/about an axis between the
                                    actual tcp position and the one set by the program.

        f_type: An integer specifying how the robot interprets the force frame. 
                1: The force frame is transformed in a way such that its y-axis is aligned with a vector
                   pointing from the robot tcp towards the origin of the force frame. 
                2: The force frame is not transformed. 
                3: The force frame is transformed in a way such that its x-axis is the projection of
                   the robot tcp velocity vector onto the x-y plane of the force frame. 
                All other values of f_type are invalid.

        wait: function return when movement is finished

        q:    list of target joint positions  


        Return Value:
        Status (bool): Status, True if signal set successfully.
        
        """
        
        prg =  '''def move_force():
    force_mode(p{task_frame}, {selection_vector}, {wrench}, {f_type}, {limits})
{movestr}
    end_force_mode()
end
'''
        movestr = self._move(movetype, pose, a, v, t, r, wait, q)
        
        self.robotConnector.RealTimeClient.SendProgram(prg.format(**locals()))
        if(wait):
            self.waitRobotIdleOrStopFlag()

    def print_actual_tcp_pose(self):
        '''
        print the actual TCP pose 
        '''
        self.print_pose(self.get_actual_tcp_pose())

    def print_actual_joint_positions(self):
        '''
        print the actual TCP pose 
        '''
        self.print_pose(q=self.get_actual_joint_positions())

    def print_pose(self, pose=None, q=None):
        '''
        print a pose 
        '''        
        if q is None:
            print('Robot Pose: [{: 06.3f}, {: 06.3f}, {: 06.3f},   {: 06.3f}, {: 06.3f}, {: 06.3f}]'.format(*pose))
        else:
            print('Robot joint positions: [{: 06.3f}, {: 06.3f}, {: 06.3f},   {: 06.3f}, {: 06.3f}, {: 06.3f}]'.format(*q))
