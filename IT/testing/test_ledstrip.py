import time

from RPi import GPIO
from letterdisplay.ledstriphandler import LEDStripHandler

__letterledpins = [11, 12, 13, 15, 16]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # GPIO Layout (Pin-Nummer verwenden)
GPIO.setup(__letterledpins, GPIO.OUT, initial=GPIO.LOW)  # declare all LED Pins as output and turn LEDs off

LEDStripHandler.display_letter_on_LEDs(1)
time.sleep(2)
LEDStripHandler.turnoff_letter_on_LEDs(1)
LEDStripHandler.display_letter_on_LEDs(2)
time.sleep(2)
LEDStripHandler.turnoff_letter_on_LEDs(2)
LEDStripHandler.display_letter_on_LEDs(3)
time.sleep(2)
LEDStripHandler.turnoff_letter_on_LEDs(3)
LEDStripHandler.display_letter_on_LEDs(4)
time.sleep(2)
LEDStripHandler.turnoff_letter_on_LEDs(4)
LEDStripHandler.display_letter_on_LEDs(5)
time.sleep(2)
LEDStripHandler.turnoff_letter_on_LEDs(5)
LEDStripHandler.start_powerled()
time.sleep(2)
LEDStripHandler.stop_powerled()