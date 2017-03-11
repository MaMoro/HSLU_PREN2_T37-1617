# ================================================================================
# !/usr/bin/python
# TITLE           : ledstriphandler.py
# DESCRIPTION     : Handler for representing detected number on LEDs
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 03.02.2017
# USAGE           :
# VERSION         : 0.2
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
    __letterledpins = [11, 12, 13, 15, 16]
    __powerledpin = 14
    fileConfig(cfg.get_logging_config_fullpath())
    __log = logging.getLogger()
    __log.setLevel(cfg.get_settings_loglevel())

    @staticmethod
    def display_letter_on_LEDs(number):
        if not LEDStripHandler.__gpio_init:
            LEDStripHandler.__setupGPIOPins()
        GPIO.output(LEDStripHandler.__letterledpins[:number], GPIO.HIGH)  # LEDs einschalten
        time.sleep(0.1)  # Pin "setzen lassen"
        LEDStripHandler.__log.info("LEDs for number " + str(number) + " turned on!")

    @staticmethod
    def start_powerled():
        if not LEDStripHandler.__gpio_init:
            LEDStripHandler.__setupGPIOPins()
        GPIO.output(LEDStripHandler.__powerledpin, GPIO.HIGH)
        time.sleep(0.1)
        LEDStripHandler.__log.info("PowerLED turned on!")

    @staticmethod
    def stop_powerled():
        if not LEDStripHandler.__gpio_init:
            LEDStripHandler.__setupGPIOPins()
        GPIO.output(LEDStripHandler.__powerledpin, GPIO.LOW)
        time.sleep(0.1)
        LEDStripHandler.__log.info("PowerLED turned off!")

    @staticmethod
    def __setupGPIOPins():
        LEDStripHandler.__log.info("Initialize GPIO Pins...")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)    #GPIO Layout (Pin-Nummer verwenden)
        GPIO.setup(LEDStripHandler.__letterledpins, GPIO.OUT, initial=GPIO.LOW) #declare all LED Pins as output and turn LEDs off
        GPIO.setup(LEDStripHandler.__powerledpin, GPIO.OUT, initial=GPIO.LOW)   #declare PowerLED Pin as output and turn LED off
        time.sleep(0.1)             #Pins "setzen lassen"
        LEDStripHandler.__gpio_init = True
        LEDStripHandler.__log.info("Initialize GPIO Pins done!")
