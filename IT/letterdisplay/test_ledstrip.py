import time
from letterdisplay.ledstriphandler import LEDStripHandler

LEDStripHandler.display_letter_on_LEDs(1)
LEDStripHandler.display_letter_on_LEDs(2)
LEDStripHandler.display_letter_on_LEDs(3)
LEDStripHandler.display_letter_on_LEDs(4)
LEDStripHandler.display_letter_on_LEDs(5)
LEDStripHandler.start_powerled()
time.sleep(0.01)
LEDStripHandler.stop_powerled()
