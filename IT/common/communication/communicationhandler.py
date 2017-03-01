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


class SerialCommunicationHandler:
    class __SerialCommunicationHandler:
        def __init__(self):
            fileConfig(cfg.get_logging_config_fullpath())
            self.__log = logging.getLogger()
            self.gpiopinsconfigured = False
            # https://pyserial.readthedocs.io/en/latest/shortintro.html
            self.serialcom = None
            self.__initCOMPort()
            self.__initGPIOPins()

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

        def __initCommunicationToFreedomBoard(self):
            """
            This function will initialize the corresponding GPIO-Pins for serial
            """
            self.__log.info("Setup communication with FreedomBoard started")
            # TODO: Setup communication with FreedomBoard over seriaö

        def transmit(self, value):
            self.__log.debug("sending value: " + str(value))
            self.serialcom.write(value)
            self.serialcom.close()
            # TODO: transmit value over serial
            self.__log.info("value: " + str(value) + " sent!")

        def receive(self):
            val = self.serialcom.read(8)
            self.serialcom.close()
            self.__log.debug("got value: XXX")
            # TODO: receive value
            return val

        def start(self):
            # start the thread to read frames from the video stream
            t = Thread()
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
