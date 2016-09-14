'''
Created on 26. aug. 2016

@author: MartinHuusBjerge
'''
import URBasic
import time

def ExampleDataLogging():
    logger = URBasic.dataLogging.DataLogging()
    logger.AddEventLogging('Demo')
    logger.DemoEvent.info('Test entry in the Demo Event log')
    logger.AddDataLogging('Demo')
    logger.DemoData.info('Test entry in the Demo Data log')


def ExampleRTDE(logger):
    ip = '192.168.56.101'
    #ip = '192.168.0.2'
    rob = URBasic.rtde.RTDE(host=ip,conf_filename='rtde_configuration.xml', logger=logger)

    #rob.start()
    time.sleep(60)
    rob.close()

def ExampleRTC(logger):
    rob = URBasic.realTimeClient.RT_CLient('192.168.56.101', conf_filename='rtde_configuration.xml', logger=logger)
    print('RTC Connection status: ' + str(rob.is_connected()))
    time.sleep(1)
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
    rob.disconnect()

def ExampleurScript(logger):
    rob = URBasic.urScript.UrScript('192.168.56.101', rtde_conf_filename='rtde_configuration.xml', logger=logger)
    rob.movej(q=[0.,-1.5,0., -1.5,0,0], a=1.2, v =0.9, t =0, r =0, wait=True)
    rob.movej(pose=[0.5,0.4,0.4, 0,3.14,0], a=1.2, v =0.9, t =0, r =0, wait=True)
    rob.servoj(q=[0.,-1.5,0., -1.5,0,0], t=5)
    rob.movel(pose=[0.5,-0.4,0.4, 0,3.14,0], a=1.2, v =0.9, t =0, r =0, wait=True)
    rob.force_mode(task_frame=[0., 0., 0.,  0., 0., 0.], selection_vector=[0,0,1,0,0,0], wrench=[0., 0., -20.,  0., 0., 0.], f_type=2, limits=[2, 2, 1.5, 1, 1, 1])
    time.sleep(1)
    rob.end_force_mode()
    
    rob.disconnect()



if __name__ == '__main__':
    #ExampleDataLogging()
    logger = URBasic.dataLogging.DataLogging()
    #ExampleRTDE(logger=logger)
    #ExampleRTC(logger)
    ExampleurScript(logger)
    
    