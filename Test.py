# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 12:21:09 2023

@author: MartinHuusBjerge
"""

import URBasic
import time
RobotModel = URBasic.robotModel.RobotModel()
RobotModel.ipAddress = '192.168.56.101'
rob = URBasic.rtde.RTDE(RobotModel, 'rtdeConfigurationTest.xml')
time.sleep(10)
rob.close()
