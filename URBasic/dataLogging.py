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
import path
__author__ = "Martin Huus Bjerge"
__copyright__ = "Copyright 2017, Rope Robotics ApS, Denmark"
__license__ = "MIT License"

import logging
import time 
import os
import URBasic

class Singleton(type):
    _instances = {}
    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


class DataLogging(metaclass=Singleton):
    '''
    A module that add general logging functions to the UR Interface framework.
    '''
    
    def __init__(self,path=None):
        '''
        Constructor that setup a path where log files will be stored.
        '''
        self.directory = None
        self.logDir = None
        self.GetLogPath(path=path)
        self.fileLogHandler = logging.FileHandler(self.directory + '\\UrEvent.log', mode='w')
        self.fileLogHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.streamLogHandler = logging.StreamHandler()
        self.streamLogHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.fileDataLogHandler = logging.FileHandler(self.directory + '\\UrDataLog.csv', mode='w')
        self.writeDataLogHeadder = True

    def GetLogPath(self,path=None, developerTestingFlag=True):
        '''
        Setup a path where log files will be stored
        Path format .\[path]\YY-mm-dd\HH-MM-SS\
        '''
        if path is None:
            path = URBasic.__file__[0:URBasic.__file__.find('URBasic')] + 'log'
        if path[-1:]=='\\':
            path = path[0:-1]
        if self.directory is None:
            self.logDir = path
            if developerTestingFlag:
                self.directory = path
            else:
                self.directory =  time.strftime(path + "\\%Y-%m-%d\\%H-%M-%S", time.localtime())
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
                
        return self.directory, self.logDir        
    
    def AddEventLogging(self, name='root', log2file=True, log2Consol=True, level = logging.INFO):
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
            self.__dict__[name].addHandler(self.fileLogHandler)
        if log2Consol:
            self.__dict__[name].addHandler(self.streamLogHandler)
        self.__dict__[name].setLevel(level)
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
        self.__dict__[name].addHandler(self.fileDataLogHandler)
        self.__dict__[name].setLevel(logging.INFO)
        if self.writeDataLogHeadder:
            self.__dict__[name].info('Time;ModuleName;Level;Channel;UR_Time;Value1;Value2;Value3;Value4;Value5;Value6')
            self.fileDataLogHandler.setFormatter(logging.Formatter('%(asctime)s;%(name)s;%(levelname)s;%(message)s'))        
            self.__dict__[name].addHandler(self.fileDataLogHandler)
            self.writeDataLogHeadder = False
        return name
    
