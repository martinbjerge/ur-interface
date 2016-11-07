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
import URplus
import time
import clr  #remember to pip install pythonnet as administrator for clr access
sys.path.append(r"C:\SourceCode\ur-interface\URConnect\RobotServer\bin\Debug")
clr.AddReference("RobotServer")
from RobotServer import RobotController


#IP = '192.168.56.101'  #URSim - Running in Oracle VM VirtualBox  
#IP = '192.168.0.2'
IP = '192.168.25.128'   #URSim - Running in VMware player
acc = 0.9
vel = 0.9



def ExampleDataLogging():
    logger = URBasic.dataLogging.DataLogging()
    logger.AddEventLogging('Demo')
    logger.DemoEvent.info('Test entry in the Demo Event log')
    logger.AddDataLogging('Demo')
    logger.DemoData.info('Test entry in the Demo Data log')


def ExampleRTDE():
    rob = URBasic.rtde.RTDE(host=IP,conf_filename='rtde_configuration.xml')
    time.sleep(10)
    rob.close_rtde()

def ExampleRTC():
    rob = URBasic.realTimeClient.RT_CLient(IP, rtde_conf_filename='rtde_configuration.xml')
    print('RTC Connection status: ' + str(rob.is_rt_client_connected()))
    time.sleep(1)
    for a in range(2):
        t = time.time()
        rob.send_program('''def myprg():
        set_digital_out(0, True)
        set_digital_out(1, True)
end 
''')
        print(time.time()-t)
        time.sleep(1)
        t = time.time()
        print(rob.send_program('set_digital_out(0, False)', wait=False))
        print(time.time()-t)
        time.sleep(5)
    rob.close_rtc()

def ExampleDbs():
    dbs = URBasic.dashboard.DashBoard(IP)
    for a in range(1):
        dbs.ur_power_off()
        time.sleep(2)
        dbs.ur_robotmode()
        dbs.wait_dbs()
        if dbs.last_respond != 'Robotmode: RUNNING': #  'Robotmode: POWER_OFF': 
            dbs.ur_power_on()
            dbs.wait_dbs()
            dbs.ur_brake_release()
            dbs.wait_dbs()
        dbs.ur_safetymode()
        dbs.wait_dbs()
        if dbs.last_respond != 'Safetymode: NORMAL':
            dbs.ur_unlock_protective_stop()
            dbs.wait_dbs()
            dbs.ur_close_safety_popup()
            dbs.wait_dbs()
            dbs.ur_brake_release()
            dbs.wait_dbs()
    dbs.close_dbs()

def ExampleurScript():
    rob = URBasic.urScript.UrScript(IP, rtde_conf_filename='rtde_configuration.xml')
    print('movej with joint specification')
    if rob.movej(q=[0.,-1.5,0., -1.5,0,0], a=1.2, v=vel, t =0, r =0, wait=True):
        print('movej with pose specification')
        if rob.movej(pose=[0.5,0.4,0.4, 0,3.14,0], a=1.2, v=vel, t =0, r =0, wait=True):
            print('movel with pose specification')
            if rob.movel(pose=[0.5,-0.4,0.4, 0,3.14,0], a=1.2, v=vel, t =0, r =0, wait=True):
                print('forcs_mode')
                if rob.force_mode(task_frame=[0., 0., 0.,  0., 0., 0.], selection_vector=[0,0,1,0,0,0], wrench=[0., 0., -20.,  0., 0., 0.], f_type=2, limits=[2, 2, 1.5, 1, 1, 1]):
                    time.sleep(1)
                    rob.end_force_mode()
    rob.close_rtc()

def ExampleurScriptExt():
    rob = URBasic.urScriptExt.UrScriptExt(IP, rtde_conf_filename='rtde_configuration.xml')
    print('movej with joint specification')
    if not rob.movej(q=[0.,-1.5,-1.5, -1.5,1.5,0], a=1.2, v=vel, t =0, r =0, wait=True):
        rob.reset_error()
        
    print('movej with pose specification')
    if not rob.movej(pose=[0.3,0.3,0.6, 0,3.14,0], a=1.2, v=vel, t =0, r =0, wait=True):
        rob.reset_error()

    print('servoj with joint specification')
    if not rob.servoj(q=[0.,-1.5,-1.5, -1.5,1.5,0], t=3):
        print(rob.get_safety_status()['NormalMode'])
        rob.reset_error()

    print('movel with pose specification')
    if not rob.movel(pose=[0.5,0.4,0.4, 0,3.14,0], a=1.2, v=vel, t =0, r =0, wait=True):
        rob.reset_error()

    #print('forcs_mode')
    #if rob.force_mode(task_frame=[0., 0., 0.,  0., 0., 0.], selection_vector=[0,0,1,0,0,0], wrench=[0., 0., 20.,  0., 0., 0.], f_type=2, limits=[2, 2, 1.5, 1, 1, 1]):
    #    rob.end_force_mode()

    rob.close_urScriptExt()


def ExampleFT_sensor():
    rob = URBasic.urScriptExt.UrScriptExt(IP, rtde_conf_filename='rtde_configuration.xml')
    rob.ft_demon = URplus.forceTorqueSensor.ForceTorqueSensor(IP)
    time.sleep(4)
    rob.ft_demon.close_ft() 
    rob.close_urScriptExt()
    
def ExampleCSharpDll():
    print("Staring DLL")
    robot = RobotController()
    print("DLL is started")    
    output_bit0 = False
    while True:
        new_value = robot.RobotModel.DigitalOutputBit0
        if(new_value != output_bit0):
            output_bit0 = new_value
            print("Output Bit 0 from C#:  " + str(output_bit0))


if __name__ == '__main__':
    #ExampleDataLogging()   
    #ExampleRTDE()
    #ExampleRTC()
    #ExampleDbs()
    #ExampleurScript()
    #ExampleurScriptExt()
    #ExampleFT_sensor()
    ExampleCSharpDll()