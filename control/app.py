import time

from flask import Flask
from flask_restful import Resource, Api

from modbus import IOVariables, runModBus

while True:
    IOVariables['b_VS1_CP1_DO']['Value'] = not IOVariables['b_VS1_CP1_DO']['Value']
    runModBus(IOVariables)
    print(IOVariables['b_VS1_CP1_DO']['Value'] )

    time.sleep(5)
