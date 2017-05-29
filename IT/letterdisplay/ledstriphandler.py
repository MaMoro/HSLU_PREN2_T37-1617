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
    __powerledpwm = None
    __letterledpins = [11, 12, 13, 15, 16]
    __powerledpin = 18
    fileConfig(cfg.get_logging_config_fullpath())
    __log = logging.getLogger()
    __log.setLevel(cfg.get_settings_loglevel())

    @staticmethod
    def display_letter_on_LEDs(number):
        if not LEDStripHandler.__gpio_init:
            LEDStripHandler.__setupGPIOPins()
        if number == 1:
            GPIO.output(16, GPIO.HIGH)  # LED 1 einschalten
        elif number == 2:
            GPIO.output(15, GPIO.HIGH)  # LED 2 einschalten
        elif number == 3:
            GPIO.output(13, GPIO.HIGH)  # LED 3 einschalten
        elif number == 4:
            GPIO.output(11, GPIO.HIGH)  # LED 4 einschalten
        elif number == 5:
            GPIO.output(12, GPIO.HIGH)  # LED 5 einschalten
        #LEDStripHandler.__log.info("LEDs for number " + str(number) + " turned on!")

    @staticmethod
    def turnoff_letter_on_LEDs(number):
        if not LEDStripHandler.__gpio_init:
            LEDStripHandler.__setupGPIOPins()
        if number == 1:
            GPIO.output(16, GPIO.LOW)  # LED 1 einschalten
        elif number == 2:
            GPIO.output(15, GPIO.LOW)  # LED 2 einschalten
        elif number == 3:
            GPIO.output(13, GPIO.LOW)  # LED 3 einschalten
        elif number == 4:
            GPIO.output(11, GPIO.LOW)  # LED 4 einschalten
        elif number == 5:
            GPIO.output(12, GPIO.LOW)  # LED 5 einschalten

    @staticmethod
    def turn_off_all_letter_LEDS():
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)

    @staticmethod
    def blinkled(number):
        i = 0
        while i < 4:
            LEDStripHandler.display_letter_on_LEDs(number)
            time.sleep(0.5)
            LEDStripHandler.turnoff_letter_on_LEDs(number)
            i += 1

    @staticmethod
    def start_powerled():
        if not LEDStripHandler.__gpio_init:
            LEDStripHandler.__setupGPIOPins()
        GPIO.output(LEDStripHandler.__powerledpin, GPIO.HIGH)
        #LEDStripHandler.__powerledpwm = GPIO.PWM(LEDStripHandler.__powerledpin, 200)
        #LEDStripHandler.__powerledpwm.start(80)  # only x% power
        LEDStripHandler.__log.info("PowerLED turned on!")

    @staticmethod
    def stop_powerled():
        if not LEDStripHandler.__gpio_init:
            LEDStripHandler.__setupGPIOPins()
        GPIO.output(LEDStripHandler.__powerledpin, GPIO.LOW)
        #LEDStripHandler.__powerledpwm.stop()
        LEDStripHandler.__log.info("PowerLED turned off!")

    @staticmethod
    def __setupGPIOPins():
        LEDStripHandler.__log.info("Initialize GPIO Pins...")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)    #GPIO Layout (Pin-Nummer verwenden)
        GPIO.setup(LEDStripHandler.__letterledpins, GPIO.OUT, initial=GPIO.LOW) #declare all LED Pins as output and turn LEDs off
        GPIO.setup(LEDStripHandler.__powerledpin, GPIO.OUT, initial=GPIO.LOW)   #declare PowerLED Pin as output and turn LED off
        LEDStripHandler.__gpio_init = True
        LEDStripHandler.__log.info("Initialize GPIO Pins done!")
