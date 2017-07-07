# coding: latin-1
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
from URplus.bk9050 import BK9050

__author__ = "Steffen Østergaard Jacobsen"
__copyright__ = "Copyright 2017, Rope Robotics ApS, Denmark"
__license__ = "MIT License"

import threading
import URBasic

class BK9050Reader(threading.Thread):

    def __init__(self, host, robotModel=None):
        threading.Thread.__init__(self)
        self.__beckhoff = None
        if host is None:
            return
        if robotModel is None:
            self.__robotModel = URBasic.robotModel.RobotModel()
        else:
            self.__robotModel = robotModel

        self.__initDataModel()
        self.__counter = 0
        self.__stop_flag = False
        self.__bk9050 = BK9050(host=host)
        self.start()

    def __readSample(self):
        values = self.__bk9050.getAnalogInputs()
        self.__updateDataModel(values)

    def close(self):
        self.__stop_flag = True
        if self.isAlive():
            self.join()

    def connected(self):
        if(self.__beckhoff is not None):
            return self.__bk9050.connected
        else:
            return False

    def run(self):
        self.__stop_flag = False
        while not self.__stop_flag:
            self.__readSample()

    def __updateDataModel(self, values):
            self.__robotModel.dataDir['analogInput0'] = values[0]
            self.__robotModel.dataDir['analogInput1'] = values[1]
            self.__robotModel.dataDir['analogInput2'] = values[2]
            self.__robotModel.dataDir['analogInput3'] = values[3]
            self.__robotModel.dataDir['analogInput4'] = values[4]
            self.__robotModel.dataDir['analogInput5'] = values[5]
            self.__robotModel.dataDir['analogInput6'] = values[6]
            self.__robotModel.dataDir['analogInput7'] = values[7]

    def __initDataModel(self):
            self.__robotModel.dataDir['analogInput0'] = None
            self.__robotModel.dataDir['analogInput1'] = None
            self.__robotModel.dataDir['analogInput2'] = None
            self.__robotModel.dataDir['analogInput3'] = None
            self.__robotModel.dataDir['analogInput4'] = None
            self.__robotModel.dataDir['analogInput5'] = None
            self.__robotModel.dataDir['analogInput6'] = None
            self.__robotModel.dataDir['analogInput7'] = None
