'''
Created on 26. aug. 2016

@author: MartinHuusBjerge
'''

import URBasic
from URBasic.realTimeClient import RT_CLient

if __name__ == '__main__':
    rob = RT_CLient('192.168.56.101')
    rob.connect()
    print(rob.is_connected())
    rob.disconnect()
