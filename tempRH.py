import serial
import subprocess as sp
import json
import numpy as np
import time

class tempRH(object):
# Module for communicating with the power meter
    '''
    Temperature and humidity reader
    http://qolah.org/Atmel_firmware/tempsense

    Usage: Send plaintext commands, separated by newline/cr or semicolon.
           An eventual reply comes terminated with cr+lf.

    Important commands:

    *RST     no specific function yet
    *IDN?    returns device identity
    ON       switches thermistor bias on
    OFF      switches thermistor bias off
    ITEMP?   returns instantaneous temperature in degree Celsius
    NTEMP?   returns last periodically (100ms) read temperature
    TEMP?    returns a low-pass filtered average temperature over 3.2sec
    RH?      returns relative humidity in percent from the SHT30 sensor
    CTEMP?   returns Sensirion chip temperature
    WEATHER? Reports both avg temperature and rel humidity
    HELP     prints a short help text
    DFU      initiates an identity change to prepare for a DFU loading sequence
    '''

    baudrate = 115200

    def __init__(self, port):
        self.serial = self._open_port(port)
        #self.serial.write(b'*IDN?;')# flush io buffer
        #print (self._serial_read()) #will read unknown command
        #self.set_range(4) #Sets bias resistor to 1k

    def _open_port(self, port):
        ser = serial.Serial(port, timeout=1)
        #ser.readline()
        #ser.timeout = 1 #causes problem with nexus 7
        return ser

    def close(self):
        self.serial.close()



    def _serial_write(self, string2):
        self.serial.write((string2+';').encode('UTF-8'))

    def _serial_read(self):
        msg_string = self.serial.readline().decode()
        # Remove any linefeeds etc
        msg_string = msg_string.rstrip()
        return msg_string

    def reset(self):
        self._serial_write('*RST')
        return self._serial_read()

    def get_intemp(self):
        #get instaneous temperature
        self._serial_write('ITEMP?')
        temp = self._serial_read()

        return temp

    def get_ntemp(self):
        self._serial_write('NTEMP?')
        temp = self._serial_read()

        return temp

    def get_temp(self):
        #get low pass filtered average temperature over 3.2 sec
        self._serial_write('TEMP?')
        temp = self._serial_read()
        return temp

    def on(self):
        #switch on thermistor
        self._serial_write('ON')

    def off(self):
        #switch on thermistor
        self._serial_write('OFF')
