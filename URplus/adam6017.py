'''
Created on Dec 8, 2016

@author: MartinHuusBjerge
'''


from pymodbus.client.sync import ModbusTcpClient as ModbusClient
#from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.client.sync import ModbusUdpClient as ModbusClient
from bitstring import Bits

class InputRange:
    PlusMinus150mV = 259
    PlusMinus500mV = 260
    ZeroTo150mV = 261
    ZeroTo500mV = 262
    PlusMinus1V = 320
    PlusMinus5V = 322
    PlusMinus10V = 323
    ZeroTo1V = 325
    ZeroTo5V = 327
    ZeroTo10V = 328
    PlusMinus20mA = 385
    FourTo20mA = 4224
    ZeroTo20mA = 4226
    
    

class ADAM6017(object):
    '''
    Controlling the additional inputs and outputs on the robot
    This class is setup to use the ADAM-6017 model via Modbus over TCP
    '''
    def __init__(self, host):
        '''
        Constructor see class description for more info.
        '''
        self.__client = ModbusClient(host=host)
        connected = self.__client.connect()
        print(connected)
        
    def setDigitalOutput(self, outputNumber, state):
        result = self.__client.write_coil(outputNumber+16, state)
    
    def getDigitalOutputState(self, outputNumber):
        result = self.__client.read_coils(outputNumber+16,1)
        #result2 = self.__client.read_holding_registers(inputNumber, 2)
        return result.bits[0]
    
    def getAnalogInputs(self):
        result = self.__client.read_holding_registers(0, 8)
        bit = Bits(uint=result.registers[0], length=16)
        print(bit.int)
        return result.registers
    
    def getAnalogInput(self, inputNumber):
        result = self.__client.read_holding_registers(inputNumber, 1)
        return result
        
    def getInputRange(self, inputNumber):
        result = self.__client.read_holding_registers(200+inputNumber, 1)
        return result
    
    def setInputRange(self, inputNumber, inputRange):
        result = self.__client.write_register(200+inputNumber, inputRange)
    #skal der være en def updateRopeRoboticsRobotModel der kører fast?