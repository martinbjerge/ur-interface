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
import URBasic.realTimeClient

class UrScript(URBasic.realTimeClient.RT_CLient):
    '''
    Interface to remote access UR script commands.
    For more details see the script manual at this site:
    http://www.universal-robots.com/download/
    
    Beside the implementation of the script interface, this class also inherits from the 
    Real Time Client and RTDE interface and thereby also open a connection to these data interfaces.
    The Real Time Client in this version is only used to send program and script commands 
    to the robot, not to read data from the robot, all data reading is done via the RTDE interface.
    
    The constructor takes a UR robot hostname as input, and a RTDE configuration file, and optional a logger object.

    Input parameters:
    host (string):  hostname or IP of UR Robot (RT CLient server)
    rtde_conf_filename (string):  Path to xml file describing what channels to activate
    logger (URBasis_DataLogging obj): A instance if a logger object if common logging is needed.

    
    Example:
    rob = URBasic.urScript.UrScript('192.168.56.101', rtde_conf_filename='rtde_configuration.xml')
    self.close_rtc()
    '''


    def __init__(self, host='localhost', rtde_conf_filename='rtde_configuration.xml', logger = URBasic.dataLogging.DataLogging()):
        '''
        Constructor see class description for more info.
        '''
        super().__init__(host, rtde_conf_filename, logger)        
        name = logger.AddEventLogging(__name__)        
        self.__logger = logger.__dict__[name]
        self.__logger.info('Init done')
        
    def movej(self, q=None, a=1.4, v =1.05, t =0, r =0, wait=True, pose=None):
        '''
        Move to position (linear in joint-space) When using this command, the
        robot must be at standstill or come from a movej og movel with a
        blend. The speed and acceleration parameters controls the trapezoid
        speed proﬁle of the move. The $t$ parameters can be used in stead to
        set the time for this move. Time setting has priority over speed and
        acceleration settings. The blend radius can be set with the $r$
        parameters, to avoid the robot stopping at the point. However, if he
        blend region of this mover overlaps with previous or following regions,
        this move will be skipped, and an ’Overlapping Blends’ warning
        message will be generated.
        Parameters:
        q:    joint positions (Can also be a pose)
        a:    joint acceleration of leading axis [rad/sˆ2]
        v:    joint speed of leading axis [rad/s]
        t:    time [S]
        r:    blend radius [m]
        pose: target pose
        '''
        if q is None:
            prg = 'movej(p{pose}, {a}, {v}, {t}, {r})'
        else:
            prg = 'movej({q}, {a}, {v}, {t}, {r})'
        return self.send_program(prg.format(**locals()), wait)
        
    def movel(self, pose, a=1.2, v =0.25, t =0, r =0, wait=True):
        '''
        Move to position (linear in tool-space)
        See movej.
        Parameters:
        pose: target pose
        a:    tool acceleration [m/sˆ2]
        v:    tool speed [m/s]
        t:    time [S]
        r:    blend radius [m]
        '''
        prg = 'movel(p{pose}, {a}, {v}, {t}, {r})'
        return self.send_program(prg.format(**locals()), wait)

    def movep(self, pose, a=1.2, v =0.25, r =0, wait=True):
        '''
        Move Process
        
        Blend circular (in tool-space) and move linear (in tool-space) to
        position. Accelerates to and moves with constant tool speed v.
        Parameters:
        pose: target pose (pose can also be speciﬁed as joint
              positions, then forward kinematics is used to calculate the corresponding pose)
        a:    tool acceleration [m/sˆ2]
        v:    tool speed [m/s]
        r:    blend radius [m]
        '''
        prg = 'movep({pose}, {a}, {v}, {r})'
        return self.send_program(prg.format(**locals()), wait)
        
    def movec(self, pose_via, pose_to, a=1.2, v =0.25, r =0, wait=True):
        '''
        Move Circular: Move to position (circular in tool-space)

        TCP moves on the circular arc segment from current pose, through pose via to pose to. 
        Accelerates to and moves with constant tool speed v.

        Parameters:
        pose_via: path point (note: only position is used). (pose via can also be speciﬁed as joint positions,
                  then forward kinematics is used to calculate the corresponding pose)
        pose to:  target pose (pose to can also be speciﬁed as joint positions, then forward kinematics 
                  is used to calculate the corresponding pose)
        a:        tool acceleration [m/sˆ2]
        v:        tool speed [m/s]
        r:        blend radius (of target pose) [m]
        '''
        prg = 'movec({pose_via}, {pose_to}, {a}, {v}, {r})'
        return self.send_program(prg.format(**locals()), wait)
 
    def force_mode(self, task_frame=[0.,0.,0., 0.,0.,0.], selection_vector=[0,0,1,0,0,0], wrench=[0.,0.,0., 0.,0.,0.], f_type=2, limits=[2, 2, 1.5, 1, 1, 1], wait=False, timeout=60):
        '''
        Set robot to be controlled in force mode
        
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

        f_type: An integer specifying how the robot interprets the force frame. 
                1: The force frame is transformed in a way such that its y-axis is aligned with a vector
                   pointing from the robot tcp towards the origin of the force frame. 
                2: The force frame is not transformed. 
                3: The force frame is transformed in a way such that its x-axis is the projection of
                   the robot tcp velocity vector onto the x-y plane of the force frame. 
                All other values of f_type are invalid.

        limits: A 6d vector with ﬂoat values that are interpreted differently for
                compliant/non-compliant axes: 
                Compliant axes: The limit values for compliant axes are the maximum
                                allowed tcp speed along/about the axis. 
                Non-compliant axes: The limit values for non-compliant axes are the
                                    maximum allowed deviation along/about an axis between the
                                    actual tcp position and the one set by the program.
                                    
        '''
        prg = '''def ur_force_mode():
        while True:
            force_mode(p{task_frame}, {selection_vector}, {wrench}, {f_type}, {limits})
            sync()
        end
end'''
        return self.send_program(prg.format(**locals()), wait, timeout)
 
    def end_force_mode(self, wait=True):
        '''
        Resets the robot mode from force mode to normal operation.
        This is also done when a program stops.
        '''
        prg = 'end_force_mode()'        
        return self.send_program(prg.format(**locals()), wait)
        
    def servoc(self, pose, a=1.2, v =0.25, r =0, wait=True):
        '''
        Servo Circular
        Servo to position (circular in tool-space). Accelerates to and moves with constant tool speed v.
        
        Parameters:
        pose: target pose
        a:    tool acceleration [m/sˆ2]
        v:    tool speed [m/s]
        r:    blend radius (of target pose) [m]
        '''
        prg = 'servoc(p{pose}, {a}, {v}, {r})'
        return self.send_program(prg.format(**locals()), wait)

    def servoj(self, q, t =0.008, lookahead_time=0.1, gain=300, wait=True):
        '''
        Servo to position (linear in joint-space)
        Servo function used for online control of the robot. The lookahead time
        and the gain can be used to smoothen or sharpen the trajectory.
        Note: A high gain or a short lookahead time may cause instability.
        Prefered use is to call this function with a new setpoint (q) in each time
        step (thus the default t=0.008)
        Parameters:
        q:              joint positions [rad]
        t:              time where the command is controlling
                        the robot. The function is blocking for time t [S]
        lookahead_time: time [S], range [0.03,0.2] smoothens the trajectory with this lookahead time
        gain:           proportional gain for following target position, range [100,2000]
        '''
        prg = 'servoj({q}, 0, 0, {t}, {lookahead_time}, {gain})'
        return self.send_program(prg.format(**locals()), wait)
        
    def speedj(self, qd, a, t , wait=True):
        '''
        Joint speed
        Accelerate linearly in joint space and continue with constant joint
        speed. The time t is optional; if provided the function will return after
        time t, regardless of the target speed has been reached. If the time t is
        not provided, the function will return when the target speed is reached.
        Parameters:
        qd: joint speeds [rad/s]
        a:  joint acceleration [rad/sˆ2] (of leading axis)
        t:  time [s] before the function returns (optional)
        '''
        prg = 'speedj({qd}, {a}, {t})'
        return self.send_program(prg.format(**locals()), wait)

    def stopj(self, a, wait=True):
        '''
        Stop (linear in joint space)
        Decellerate joint speeds to zero
        Parameters
        a: joint acceleration [rad/sˆ2] (of leading axis)
        '''
        prg = 'stopj({a})'
        return self.send_program(prg.format(**locals()), wait)        
        
    def speedl(self, xd, a, t, aRot='a', wait=True):
        '''
        Tool speed
        Accelerate linearly in Cartesian space and continue with constant tool
        speed. The time t is optional; if provided the function will return after
        time t, regardless of the target speed has been reached. If the time t is
        not provided, the function will return when the target speed is reached.
        Parameters:
        xd:   tool speed [m/s] (spatial vector)
        a:    tool position acceleration [m/sˆ2]
        t:    time [s] before function returns (optional)
        aRot: tool acceleration [rad/sˆ2] (optional), if not deﬁned a, position acceleration, is used
        '''
        prg = 'speedl({xd}, {a}, {t}, {aRot})'
        return self.send_program(prg.format(**locals()), wait)

    def stopl(self, a, aRot ='a', wait=True):
        '''
        Stop (linear in tool space)
        Decellerate tool speed to zero
        Parameters:
        a:    tool accleration [m/sˆ2]
        aRot: tool acceleration [rad/sˆ2] (optional), if not deﬁned a, position acceleration, is used
        '''
        prg = 'stopl({a}, {arot})'
        return self.send_program(prg.format(**locals()), wait)

    def freedrive_mode(self, wait=True):
        '''
        Set robot in freedrive mode. In this mode the robot can be moved around by hand in the 
        same way as by pressing the ”freedrive” button.
        The robot will not be able to follow a trajectory (eg. a movej) in this mode.
        '''
        prg = '''def ur_freedrive_mode():
        while True:
            freedrive_mode()
        end
        end'''
        self.send_program(prg.format(**locals()), wait)

    def end_freedrive_mode(self, wait=True):
        '''
        Set robot back in normal position control mode after freedrive mode.
        '''
        prg = 'end_freedrive_mode()'        
        return self.send_program(prg.format(**locals()), wait)
        
    def teach_mode(self, wait=True):
        '''
        Set robot in freedrive mode. In this mode the robot can be moved
        around by hand in the same way as by pressing the ”freedrive” button.
        The robot will not be able to follow a trajectory (eg. a movej) in this mode.
        '''
        prg = '''def ur_teach_mode():
        while True:
            teach_mode()
        end
        end'''
        self.send_program(prg.format(**locals()), wait)

    def end_teach_mode(self, wait=True):
        '''
        Set robot back in normal position control mode after freedrive mode.
        '''
        prg = 'end_teach_mode()'        
        return self.send_program(prg.format(**locals()), wait)
    
        
    def conveyor_pulse_decode(self, in_type, A, B, wait=True):
        '''
        Tells the robot controller to treat digital inputs number A and B as pulses 
        for a conveyor encoder. Only digital input 0, 1, 2 or 3 can be used.

        >>> conveyor pulse decode(1,0,1)

        This example shows how to set up quadrature pulse decoding with
        input A = digital in[0] and input B = digital in[1]

        >>> conveyor pulse decode(2,3)
        
        This example shows how to set up rising and falling edge pulse
        decoding with input A = digital in[3]. Note that you do not have to set
        parameter B (as it is not used anyway).
        Parameters:
            in_type: An integer determining how to treat the inputs on A
                  and B
                  0 is no encoder, pulse decoding is disabled.
                  1 is quadrature encoder, input A and B must be
                    square waves with 90 degree offset. Direction of the
                    conveyor can be determined.
                  2 is rising and falling edge on single input (A).
                  3 is rising edge on single input (A).
                  4 is falling edge on single input (A).

            The controller can decode inputs at up to 40kHz
            A: Encoder input A, values of 0-3 are the digital inputs 0-3.
            B: Encoder input B, values of 0-3 are the digital inputs 0-3.
        '''
        
        prg = 'conveyor_pulse_decode({in_type}, {A}, {B})'        
        return self.send_program(prg.format(**locals()), wait)
        
    def set_conveyor_tick_count(self, tick_count, absolute_encoder_resolution=0, wait=True):
        '''
        Tells the robot controller the tick count of the encoder. This function is
        useful for absolute encoders, use conveyor pulse decode() for setting
        up an incremental encoder. For circular conveyors, the value must be
        between 0 and the number of ticks per revolution.
        Parameters:
        tick_count: Tick count of the conveyor (Integer)
        absolute_encoder_resolution: Resolution of the encoder, needed to
                                     handle wrapping nicely.
                                     (Integer)
                                    0 is a 32 bit signed encoder, range [-2147483648 ;2147483647] (default)
                                    1 is a 8 bit unsigned encoder, range [0 ; 255]
                                    2 is a 16 bit unsigned encoder, range [0 ; 65535]
                                    3 is a 24 bit unsigned encoder, range [0 ; 16777215]
                                    4 is a 32 bit unsigned encoder, range [0 ; 4294967295]
        '''
        prg = 'set_conveyor_tick_count({tick_count}, {absolute_encoder_resolution})'
        self.send_program(prg.format(**locals()), wait)
                
    def get_conveyor_tick_count(self, wait=True, rtde_reg='output_double_register_0'):
        '''
        Tells the tick count of the encoder, note that the controller interpolates tick counts to get 
        more accurate movements with low resolution encoders

        Return Value:
            The conveyor encoder tick count
        '''
        
        if self.has_get_data_attr(rtde_reg):
            prg = '''def ur_get_conveyor_tick_count():
            write_output_float_register(0, get_conveyor_tick_count())
            end'''
            if self.send_program(prg.format(**locals()), wait):
                return self.get_data(rtde_reg, wait=True)
            else:
                return False
        else:
            self.__logger.warning('RTDE register not configured, expecting: ' + rtde_reg)
            return False
        
    def stop_conveyor_tracking(self, a=15, aRot ='a', wait=True):
        '''
        Stop tracking the conveyor, started by track conveyor linear() or
        track conveyor circular(), and decellerate tool speed to zero.
        Parameters:
        a:    tool accleration [m/sˆ2] (optional)
        aRot: tool acceleration [rad/sˆ2] (optional), if not deﬁned a, position acceleration, is used
        '''
        prg = 'stop_conveyor_tracking({a}, {aRot})'
        return self.send_program(prg.format(**locals()), wait)
        
    def track_conveyor_circular(self, center, ticks_per_revolution, rotate_tool, wait=True):
        '''
        Makes robot movement (movej() etc.) track a circular conveyor.
        
        >>> track conveyor circular(p[0.5,0.5,0,0,0,0],500.0, false)
        
        The example code makes the robot track a circular conveyor with
        center in p[0.5,0.5,0,0,0,0] of the robot base coordinate system, where
        500 ticks on the encoder corresponds to one revolution of the circular
        conveyor around the center.
        Parameters:
        center:               Pose vector that determines the center the conveyor in the base
                              coordinate system of the robot.
        ticks_per_revolution: How many tichs the encoder sees when the conveyor moves one revolution.
        rotate tool:          Should the tool rotate with the coneyor or stay in the orientation 
                              speciﬁed by the trajectory (movel() etc.).
        '''
        prg = 'track_conveyor_circular({center}, {ticks_per_revolution}, {rotate_tool})'
        return self.send_program(prg.format(**locals()), wait)


    def track_conveyor_linear(self, direction, ticks_per_meter, wait=True):
        '''
        Makes robot movement (movej() etc.) track a linear conveyor.
        
        >>> track conveyor linear(p[1,0,0,0,0,0],1000.0)
        
        The example code makes the robot track a conveyor in the x-axis of
        the robot base coordinate system, where 1000 ticks on the encoder
        corresponds to 1m along the x-axis.
        Parameters:
        direction:       Pose vector that determines the direction of the conveyor in the base
                         coordinate system of the robot
        ticks per meter: How many tichs the encoder sees when the conveyor moves one meter
        '''
        prg = 'track_conveyor_linear({direction}, {ticks_per_meter})'
        return self.send_program(prg.format(**locals()), wait)

    def position_deviation_warning(self, enabled, threshold =0.8, wait=True):
        '''
        Write a message to the log when the robot position deviates from the target position.
        Parameters:
        enabled:   enable or disable position deviation log messages (Boolean)
        threshold: (optional) should be a ratio in the range ]0;1], where 0 is no position deviation and 1 is the
                   position deviation that causes a protective stop (Float).
        '''
        prg = 'position_deviation_warning({enabled}, {threshold})'
        return self.send_program(prg.format(**locals()), wait)
        
    def reset_revolution_counter(self, qNear=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], wait=True):
        '''
        Reset the revolution counter, if no offset is speciﬁed. This is applied on
        joints which safety limits are set to ”Unlimited” and are only applied
        when new safety settings are applied with limitted joint angles.

        >>> reset revolution counter()

        Parameters:
        qNear: Optional parameter, reset the revolution counter to one close to the given qNear joint vector. 
               If not deﬁned, the joint’s actual number of revolutions are used.
        ''' 
        prg = 'reset_revolution_counter(qNear)'
        return self.send_program(prg.format(**locals()), wait)
        
    def set_pos(self, q, wait=True):
        '''
        Set joint positions of simulated robot
        Parameters
        q: joint positions
        '''
        prg = 'set_pos({q})'
        return self.send_program(prg.format(**locals()), wait)

    
    def force(self):
        '''
        Returns the force exerted at the TCP
        
        Return the current externally exerted force at the TCP. The force is the
        norm of Fx, Fy, and Fz calculated using get tcp force().
        Return Value
        The force in Newtons (ﬂoat)
        '''


        
    def get_actual_joint_positions(self):
        '''
        Returns the actual angular positions of all joints
        
        The angular actual positions are expressed in radians and returned as a
        vector of length 6. Note that the output might differ from the output of
        get target joint positions(), especially durring acceleration and heavy
        loads.
        
        Return Value:
        The current actual joint angular position vector in rad : [Base,
        Shoulder, Elbow, Wrist1, Wrist2, Wrist3]
        '''
        
    def get_actual_joint_speeds(self):
        '''
        Returns the actual angular velocities of all joints
        
        The angular actual velocities are expressed in radians pr. second and
        returned as a vector of length 6. Note that the output might differ from
        the output of get target joint speeds(), especially durring acceleration
        and heavy loads.
        
        Return Value
        The current actual joint angular velocity vector in rad/s:
        [Base, Shoulder, Elbow, Wrist1, Wrist2, Wrist3]
        '''
        
    def get_actual_tcp_pose(self):
        '''
        Returns the current measured tool pose
        
        Returns the 6d pose representing the tool position and orientation
        speciﬁed in the base frame. The calculation of this pose is based on
        the actual robot encoder readings.
        
        Return Value
        The current actual TCP vector : ([X, Y, Z, Rx, Ry, Rz])
        '''
        
    def get_actual_tcp_speed(self):
        '''
        Returns the current measured TCP speed
        
        The speed of the TCP retuned in a pose structure. The ﬁrst three values
        are the cartesian speeds along x,y,z, and the last three deﬁne the
        current rotation axis, rx,ry,rz, and the length |rz,ry,rz| deﬁnes the angular
        velocity in radians/s.
        Return Value
        The current actual TCP velocity vector; ([X, Y, Z, Rx, Ry, Rz])
        '''
        
    def get_actual_tool_ﬂange_pose(self):
        '''
        Returns the current measured tool ﬂange pose
        
        Returns the 6d pose representing the tool ﬂange position and
        orientation speciﬁed in the base frame, without the Tool Center Point
        offset. The calculation of this pose is based on the actual robot
        encoder readings.
        
        Return Value:
        The current actual tool ﬂange vector : ([X, Y, Z, Rx, Ry, Rz])
        
        Note: See get actual tcp pose for the actual 6d pose including TCP offset.
        '''
        
    def get_controller_temp(self):
        '''
        Returns the temperature of the control box
        
        The temperature of the robot control box in degrees Celcius.
        
        Return Value:
        A temperature in degrees Celcius (ﬂoat)
        '''