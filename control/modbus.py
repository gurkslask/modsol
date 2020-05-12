#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymodbus3.client.sync import ModbusTcpClient
from pymodbus3.exceptions import ConnectionException
from ModbusDigitalInputIOCardClass import ModbusDigitalInputIOCard
from ModbusDigitalOutputIOCardClass import ModbusDigitalOutputIOCard
import datetime

IOVariables = {'b_VS1_CP1_DO': {'Value': 0, 'IOdevice': 2048, 'IOadress': 3, 'Comment': 'Radiator cirk pumpen'}}

def runModBus(IOVariables):
    client = ModbusTcpClient('192.168.1.9')
    Digital_Out_1 = ModbusDigitalOutputIOCard(2048, client, IOVariables)          
    try:
        Digital_Out_1.WriteStatus()
    except ConnectionException:
        print('A connection error to the modbus occured at {}'.format(
            datetime.datetime.now()
            )
        )
        pass
    client.close()      



class ModbusDigitalOutputIOCard():
    """docstring for ModbusDigitalOutput
    This is a class for CREVIS Digital Output card
    that communicates via Modbus.
    When assigning the class, the Modbus adress
    must be specified. The modbus client must be
    included as well, as this is where the connection
    will happen
    """
    def __init__(self, adress, client, IOdict):
        self.IOdict = IOdict
        self.IOcard = 0
        self.IOadress = adress
        self.IOValue = 0
        self.IOVariables = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        self.client = client
        #List all of the variables that are declared for this IOdevice
        self.IOlist = [
            i for i in self.IOdict
            if self.IOdict[i]['IOdevice'] == self.IOadress
            ]

    def BinToDec(self):
        '''
        This method will read the input values from the IO card
        and convert from decimal to bin
        Here you gotta do data assignments as follows:

        '''
        #Take all the variables for this device and check their values
        for i in self.IOlist:
            self.IOVariables[self.IOdict[i]['IOadress']] = strtobool(str(self.IOdict[i]['Value']))
        #Make the decimal numbers to a binary number, ie. 0110 = 6
        Bindata = ''
        for i in self.IOVariables:
            Bindata = str(self.IOVariables[i])+Bindata
        DecData = int(Bindata, 2)
        DecData = [DecData]
        #print(DecData)
        return DecData

    def WriteStatus(self):
        #Write it all down to the modbus device
        self.client.write_registers(self.IOadress, self.BinToDec())




