# ================================================================================
# !/usr/bin/python
# TITLE           : main.py
# DESCRIPTION     : Main routine to start raspberry for project
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 30.01.2017
# USAGE           :
# VERSION         : 0.1
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

#Import all needed classes
import logging
import os
import subprocess
import sys
import time
import common.config.confighandler as cfg

from logging.config import fileConfig
from common.communication.communicationvalues import CommunicationValues
from common.processing.camerahandler import CameraHandler
from letterdisplay.ledstriphandler import LEDStripHandler
from trafficlight.trafficlightdetection_pi import TrafficLightDetectionPi
from letterdetection.letterdetectionhandler import LetterDetectionHandler


class RunPiHandler(object):
    def __init__(self):
        print("**************************************************")
        print("* Autonomes Geländefahrzeug: PREN Team 37, 2017  *")
        print("**************************************************")

        # Load configuration / config handler
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()
        self.__log.setLevel(cfg.get_settings_loglevel())
        self.__log.info("Pi ready! :)")
        self.serialcomm = None
        self.currentcourse = 0
        self.runparcours()

    def runparcours(self):
        # Wait for parcour setting (left/right)
        self.__log.info("Await course selection...")
        while self.currentcourse == 0:
            self.currentcourse = cfg.get_settings_course()
            time.sleep(0.5)
        self.__log.info("Course selected!")

        # Init communication between raspi and freedom
        self.__log.info("Setup serial communication with FreedomBoard...")
        self.serialcomm = CommunicationValues()
        self.serialcomm.send_hello()
        hellostate = self.serialcomm.get_hello_blocking()  # await hello response or timeout...
        if hellostate == '1':
            self.__log.info("serial communication established!")
            self.serialcomm.send_course(self.currentcourse)
        else:
            self.__log.error("not able to setup communication with Freedom-Board!!")

        # Init camera
        self.__log.info("Starting CameraHandling and start Trafficlight detection...")
        CameraHandler()

        # Traffic Light Detection
        t = TrafficLightDetectionPi()
        while t.getstatus() == "red":
            time.sleep(0.3)
        self.__log.info("Green signal detected...")

        # Init PowerLED
        self.__log.info("Recalibrate camera before starting")
        LEDStripHandler.start_powerled()
        CameraHandler().calibratePiCamera4Letter()
        self.__log.info("Recalibration done.")
        self.__log.info("Let's go!")

        # Letter Detection
        LetterDetectionHandler()
        self.serialcomm.send_start()
        self.__log.info("Run, chügeliwägeli, run!")

        # Stop PowerLED
        LEDStripHandler.stop_powerled()

        print("**************************************************")
        print("*                Jobs done on RPi                *")
        print("**************************************************")

if __name__ == '__main__':
    RunPiHandler()
    # keep alive till poweroff
    while True:
        pass
