'''
Created on 26. aug. 2016

@author: MartinHuusBjerge
'''
import URBasic
import time

def ExampelDataLogging():
    logger = URBasic.dataLogging.DataLogging()
    logger.AddEventLogging('Demo')
    logger.DemoEvent.info('Test entry in the Demo Event log')
    logger.AddDataLogging('Demo')
    logger.DemoData.info('Test entry in the Demo Data log')


def ExampelRTDE(logger):
    ip = '192.168.56.101'
    #ip = '192.168.0.2'
    rtde = URBasic.rtde.RTDE(host=ip, conf_filename='rtde_configuration.xml',logger=logger)
    rtde.start()
    time.sleep(60)
    rtde.close()

if __name__ == '__main__':
    #ExampelDataLogging()
    logger = URBasic.dataLogging.DataLogging()
    ExampelRTDE(logger=logger)
    pass