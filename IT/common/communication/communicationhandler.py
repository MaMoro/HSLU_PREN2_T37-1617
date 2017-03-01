# ================================================================================
# !/usr/bin/python
# TITLE           : communicationhandler.py
# DESCRIPTION     : Handler for communication with FreedomBoard
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 30.01.2017
# USAGE           : comm = SerialCommunicationHandler().start()
# VERSION         : 0.1
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

# import the necessary packages
import logging
import time
import serial
import common.config.confighandler as cfg

from threading import Thread
from logging.config import fileConfig


# https://pyserial.readthedocs.io/en/latest/shortintro.html
# https://github.com/pyserial/pyserial/blob/master/serial/threaded/__init__.py
# http://stackoverflow.com/questions/17553543/pyserial-non-blocking-read-loop
# http://pyserial.readthedocs.io/en/latest/pyserial_api.html#module-serial.threaded


class SerialCommunicationHandler:
    class __SerialCommunicationHandler:
        def __init__(self):
            fileConfig(cfg.get_logging_config_fullpath())
            self.__log = logging.getLogger()
            self.serialcom = None
            self.__initCOMPort()

        def __initCOMPort(self):
            """
            This function will initialize the corresponding GPIO-Pins for serial
            """
            # Tx GPIO14 - BOARD-Layout: Pin8
            # Rx GPIO15 - BOARD-Layout: Pin10
            self.__log.info("Serial communication initialization started")
            self.serialcom = serial.Serial()
            self.serialcom.baudrate = 9600
            self.serialcom.port = '/dev/ttyAMA0'

        def send(self, value):
            self.__log.debug("sending value: " + str(value))
            self.data_str = value

        def receive(self):
            return self.data_str

        def _handle(self):
            try:
                while self.serialcom.is_open():
                    if self.serialcom.inWaiting() > 0:  # if incoming bytes are waiting to be read from the serial input buffer
                        self.data_str = self.serialcom.read(self.serialcom.inWaiting()).decode('ascii',
                                                                                               'ignore')  # read the bytes and convert from binary array to ASCII
                    elif self.data_str is not None:
                        self.serialcom.write(self.data_str.encode('ascii', 'ignore'))
                        self.__log.info("value: " + str(self.data_str) + " sent!")
                        self.data_str = None
            except serial.SerialException as e:
                self.__log.error("serial connection lost...")


        def start(self):
            # start the thread to read frames from the video stream
            t = Thread(target=self._handle())
            t.daemon = True
            t.start()
            time.sleep(1)
            return self

    instance = None

    def __new__(cls, *args, **kwargs):
        if not SerialCommunicationHandler.instance:
            SerialCommunicationHandler.instance = SerialCommunicationHandler.__SerialCommunicationHandler()
        return SerialCommunicationHandler.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
