import time

from RPi import GPIO
from letterdisplay.ledstriphandler import LEDStripHandler

__letterledpins = [11, 12, 13, 15, 16]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # GPIO Layout (Pin-Nummer verwenden)
GPIO.setup(__letterledpins, GPIO.OUT,
           initial=GPIO.LOW)  # declare all LED Pins as output and turn LEDs off
# GPIO.output(16, GPIO.HIGH)


# LEDStripHandler.display_letter_on_LEDs(1)
# LEDStripHandler.display_letter_on_LEDs(2)
# LEDStripHandler.display_letter_on_LEDs(3)
# LEDStripHandler.display_letter_on_LEDs(4)
# LEDStripHandler.display_letter_on_LEDs(5)
# LEDStripHandler.start_powerled()
time.sleep(60)
# LEDStripHandler.stop_powerled()
