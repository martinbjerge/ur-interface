'''
Python 3.x library to control an UR robot through its TCP/IP interfaces
Copyright (C) 2017  Martin Huus Bjerge, Rope Robotics ApS, Denmark

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
__copyright__ = "Copyright 2017, Rope Robotics ApS, Denmark"
__license__ = "MIT License"

import URBasic
import time


host = '192.168.0.113'   #E.g. a Universal Robot offline simulator, please adjust to match your IP
acc = 0.9
vel = 0.9


def ExampleurScript():
    '''
    This is a small example of how to connect to a Universal Robots robot and use a few simple script commands. 
    The scrips available is in general all the scrips from the universal robot script manual, 
    and the implementation is intended to follow the Universal Robots manual as much as possible.  
    
    This script can be run connected to a Universal Robot robot (tested at a UR5) or a Universal Robot offline simulator. 
    See this example in how to setup an offline simulator: 
    https://www.universal-robots.com/download/?option=26266#section16597
    '''
    robotModle = URBasic.robotModel.RobotModel()
    robot = URBasic.urScriptExt.UrScriptExt(host=host,robotModel=robotModle)
    robot.reset_error()
    print('movej with joint specification')
    robot.movej(q=[-3.14,-1.,0.5, -1.,-1.5,0], a=acc, v=vel)
    
    print('movej with pose specification')
    robot.movej(pose=[0.3,0.3,0.3, 0,3.14,0], a=1.2, v=vel)
    
    print('movel with pose specification')
    robot.movel(pose=[0.3,-0.3,0.3, 0,3.14,0], a=1.2, v=vel)
                
    print('forcs_mode')
    robot.force_mode(task_frame=[0., 0., 0.,  0., 0., 0.], selection_vector=[0,0,1,0,0,0], wrench=[0., 0., -20.,  0., 0., 0.], f_type=2, limits=[2, 2, 1.5, 1, 1, 1])
    time.sleep(1)
    robot.end_force_mode()
    robot.close()

def ExampleExtendedFunctions():
    '''
    This is an example of an extension to the Universal Robot script library. 
    How to update the force parameters remote via the RTDE interface, 
    hence without sending new programs to the controller.
    This enables to update force "realtime" (125Hz)  
    '''
    robotModle = URBasic.robotModel.RobotModel()
    robot = URBasic.urScriptExt.UrScriptExt(host=host,robotModel=robotModle)

    print('forcs_remote')
    robot.set_force_remote(task_frame=[0., 0., 0.,  0., 0., 0.], selection_vector=[0,0,1,0,0,0], wrench=[0., 0., 20.,  0., 0., 0.], f_type=2, limits=[2, 2, 1.5, 1, 1, 1])
    robot.reset_error()
    a = 0
    upFlag = True
    while a<3:
        pose = robot.get_actual_tcp_pose()
        if pose[2]>0.1 and upFlag:
            print('Move Down')
            robot.set_force_remote(task_frame=[0., 0., 0.,  0., 0., 0.], selection_vector=[0,0,1,0,0,0], wrench=[0., 0., -20.,  0., 0., 0.], f_type=2, limits=[2, 2, 1.5, 1, 1, 1])
            a +=1
            upFlag = False
        if pose[2]<0.0 and not upFlag:
            print('Move Up')
            robot.set_force_remote(task_frame=[0., 0., 0.,  0., 0., 0.], selection_vector=[0,0,1,0,0,0], wrench=[0., 0., 20.,  0., 0., 0.], f_type=2, limits=[2, 2, 1.5, 1, 1, 1])
            upFlag = True    
    robot.end_force_mode()
    robot.reset_error()
    robot.close()
    

def ExampleFT_sensor():
    '''
    This is a small example of how to connect to a Robotiq FORCE TORQUE SENSOR and read data from the sensor.
    To run this part comment in the function call in the main call below.

    '''
    robotModle = URBasic.robotModel.RobotModel()
    robot = URBasic.urScriptExt.UrScriptExt(host=host,robotModel=robotModle,hasForceTorque=True)

    print(robotModle.dataDir['urPlus_force_torque_sensor'])
    time.sleep(1)
    print(robotModle.dataDir['urPlus_force_torque_sensor'])
    robot.close()
        

if __name__ == '__main__':
    ExampleurScript()
    ExampleExtendedFunctions()
    #ExampleFT_sensor()
    