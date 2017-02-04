# ================================================================================
# !/usr/bin/python
# TITLE           : ledstriphandler.py
# DESCRIPTION     : Handler for representing detected number on LEDs
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 03.02.2017
# USAGE           :
# VERSION         : 0.1
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================
import RPi.GPIO as GPIO
import time
import logging
import common.config.confighandler as cfg
from logging.config import fileConfig


class LEDStripHandler:

    __gpio_init = False
    __ledpins = [11, 12, 13, 15, 16]
    fileConfig(cfg.get_logging_config_fullpath())
    __log = logging.getLogger()
    __log.setLevel(cfg.get_settings_loglevel())

    @staticmethod
    def display_letter_on_LEDs(number):
        if not LEDStripHandler.__gpio_init:
            LEDStripHandler.__setupGPIOPins()
        GPIO.output(LEDStripHandler.__ledpins[:number], GPIO.HIGH)  # LEDs einschalten
        time.sleep(0.1)  # Pin "setzen lassen"
        LEDStripHandler.__log.info("LEDs for number " + str(number) + " turned on!")

    @staticmethod
    def __setupGPIOPins():
        LEDStripHandler.__log.info("Initialize GPIO Pins...")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)    #GPIO Layout (Pin-Nummer verwenden)
        GPIO.setup(LEDStripHandler.__ledpins, GPIO.OUT, initial=GPIO.LOW) #declare all Pins as output and turn LEDs off
        time.sleep(0.1)             #Pin "setzen lassen"
        LEDStripHandler.__gpio_init = True
        LEDStripHandler.__log.info("Initialize GPIO Pins done!")
