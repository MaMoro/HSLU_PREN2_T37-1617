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

        # Init Webserver
        subprocess.Popen([sys.executable, '/home/pi/Desktop/PREN/webserver/app.py'], env=os.environ.copy())
        time.sleep(15)

        # Wait for parcour setting (left/right)
        while self.currentcourse == 0:
            self.currentcourse = cfg.get_settings_course()
            time.sleep(0.5)

        # Init communication between raspi and freedom
        self.serialcomm = CommunicationValues()
        self.serialcomm.send_hello()
        hellostate = self.serialcomm.get_hello_blocking()  # await hello response or timeout...
        if hellostate == '1':
            self.serialcomm.send_course(self.currentcourse)
        else:
            self.__log.error("not able to setup communication with Freedom-Board!!")

        # Init camera
        CameraHandler().start()

        # Traffic Light Detection
        t = TrafficLightDetectionPi()
        #while t.getstatus() == "red":
        #    time.sleep(0.3)
        self.__log.info("Green signal detected...")
        time.sleep(5)

        # Init PowerLED
        LEDStripHandler.start_powerled()
        CameraHandler().calibratePiCamera()

        # Letter Detection
        LetterDetectionHandler().start()

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