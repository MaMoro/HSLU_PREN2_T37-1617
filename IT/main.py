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

# Import all needed classes
import logging
import time
import common.config.confighandler as cfg

from logging.config import fileConfig
from common.communication.communicationvalues import CommunicationValues
from letterdisplay.ledstriphandler import LEDStripHandler
from trafficlight.trafficlightdetection_pi import TrafficLightDetectionPi
from letterdetection.letterdetectionhandler import LetterDetectionHandler


class RunPiHandler(object):
    def __init__(self):
        # Load configuration / config handler
        LEDStripHandler.blinkled(1)
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()
        self.__log.setLevel(cfg.get_settings_loglevel())
        self.__log.info(" ")
        self.__log.info("**************************************************")
        self.__log.info("* Autonomes Geländefahrzeug: PREN Team 37, 2017  *")
        self.__log.info("**************************************************")
        self.__log.info(" ")
        self.__log.info("Pi ready! :)")
        LEDStripHandler.display_letter_on_LEDs(1)
        self.serialcomm = None
        self.currentcourse = 2
        self.runparcours()

    def runparcours(self):
        # Wait for parcour setting (left/right)
        self.__log.info("Await course selection...")
        while self.currentcourse == 2:
            self.currentcourse = cfg.get_settings_course()
            time.sleep(0.5)
            LEDStripHandler.singleblinkled(2)
        self.__log.info("Course selected!")
        LEDStripHandler.display_letter_on_LEDs(2)

        # Init communication between raspi and freedom
        self.__log.info("Setup serial communication with FreedomBoard...")
        self.serialcomm = CommunicationValues()
        self.serialcomm.send_hello()
        hellostate = self.serialcomm.get_hello_blocking()  # await hello response or timeout...
        if hellostate == '1' or hellostate == 1:
            self.__log.info("serial communication established!")
            LEDStripHandler.display_letter_on_LEDs(3)
            self.serialcomm.send_course(self.currentcourse)
        else:
            self.__log.error("not able to setup communication with Freedom-Board!!")
            LEDStripHandler.blinkled(3)

        coursestate = self.serialcomm.get_course_blocking()  # await course response or timeout...
        if coursestate == '1' or coursestate == 1:
            self.__log.info("course left turn!")
            LEDStripHandler.display_letter_on_LEDs(4)
        elif coursestate == '0' or coursestate == 0:
            self.__log.info("course right turn!")
            LEDStripHandler.display_letter_on_LEDs(4)
        else:
            self.__log.error("course not acknowledged :(")
            LEDStripHandler.blinkled(4)

        LEDStripHandler.display_letter_on_LEDs(5)

        # Start letterdetection to init queues
        self.__log.info("Init Letter Queues")
        ldh = LetterDetectionHandler()
        ldh.initqueues()

        # Traffic Light Detection
        self.__log.info("Detecting trafficlight change to green...")
        t = TrafficLightDetectionPi()
        LEDStripHandler.turn_off_all_letter_LEDS()
        while t.getstatus() == "red":
            time.sleep(0.3)
        self.__log.info("Green signal detected...")
        t.stop()

        # Init Camera & PowerLED
        LEDStripHandler.start_powerled()
        ldh.initcamera()
        self.__log.info("Let's go!")

        # Letter Detection
        self.__log.info("Run, chügeliwägeli, run!")
        self.serialcomm.send_start()

        numbertodisplay = ldh.start()
        LEDStripHandler.stop_powerled()
        self.__log.info("Letter found: " + str(numbertodisplay))

        self.serialcomm.send_letter(numbertodisplay)

        # blink detected letter till number  acknowledged
        sendednumber = self.serialcomm.get_letter()
        while int(sendednumber) != numbertodisplay:
            sendednumber = self.serialcomm.get_letter()
            time.sleep(0.2)
            LEDStripHandler.singleblinkled(numbertodisplay)
        self.__log.info("Letter acknowledged")
        LEDStripHandler.display_letter_on_LEDs(numbertodisplay)

        self.__log.info(" ")
        self.__log.info("**************************************************")
        self.__log.info("*                Jobs done on RPi                *")
        self.__log.info("**************************************************")

if __name__ == '__main__':
    RunPiHandler()
    # keep alive till poweroff
    while True:
        pass
