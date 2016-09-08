'''
Created on 26. aug. 2016

@author: MartinHuusBjerge
'''

import logging
import time 
import os

class DataLogging():
    '''
    A module that add general logging functions to the UR Interface framework.
    '''
    
    def __init__(self,path='.\\log'):
        '''
        Constructor that setup a path where log files will be stored.
        '''
        self.GetLogPath(path=path)

    def GetLogPath(self,path):
        '''
        Setup a path where log files will be stored
        Path format .\[path]\YY-mm-dd\HH-MM-SS\
        '''
        #Log path C:\SourceCode\bladecrawler\bladecrawler\log
        self.directory =  time.strftime(path + "\\%Y-%m-%d\\%H-%M-%S", time.localtime())
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)        
    
    def AddEventLogging(self, name='root', log2file=True, log2Consol=True):
        '''
        Add a new event logger, the event logger can log data to a file and also output the log to the console.
        
        Input Parameters:
        Name (str): The name of the logger the logger name will get the extension event
        Log2file (bool): Set if the log should be stored in a log file
        Log2Consol (bool): Set if the log should be output to the console 
        
        Return parameter:
        Name (str): The logger name including the extension
        '''
        name = name.replace('__', '').replace('.', '_') + 'Event'
        self.__dict__[name] = logging.getLogger(name) 
        if log2file:
            logHandler = logging.FileHandler(self.directory + '\\' + name + '.log', mode='w')
            logHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.__dict__[name].addHandler(logHandler)
        if log2Consol:
            logHandler = logging.StreamHandler()
            logHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.__dict__[name].addHandler(logHandler)
        self.__dict__[name].setLevel(logging.INFO)
        self.__dict__[name].info("---- New run Event logging---- ")
        return name

    def AddDataLogging(self,name='root'):
        '''
        Add a new data logger, the data logger will log data to a csv-file.

        Input Parameters:
        Name (str): The name of the logger the logger name will get the extension Data
        
        Return parameter:
        Name (str): The logger name including the extension
        '''
        name = name+'Data'
        self.__dict__[name] = logging.getLogger(name)
        LogHandler = logging.FileHandler(self.directory + '\\'+ name.replace('__', '') + '.csv', mode='w')  
        self.__dict__[name].addHandler(LogHandler)
        self.__dict__[name].setLevel(logging.INFO)
        self.__dict__[name].info('Time;ModuleName;Level;Channel;UR_Time;Value1;Value2;Value3;Value4;Value5;Value6')

        LogHandler.setFormatter(logging.Formatter('%(asctime)s;%(name)s;%(levelname)s;%(message)s'))        
        self.__dict__[name].addHandler(LogHandler)
        return name