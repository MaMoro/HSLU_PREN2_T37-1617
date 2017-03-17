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

def main():
    print("**************************************************")
    print("* Autonomes Geländefahrzeug: PREN Team 37, 2017  *")
    print("**************************************************")

#Import all needed classes

    from common.communication.communicationhandler import SerialCommunicationHandler
    from common.processing.camerahandler import CameraHandler
    from letterdetection.letterdetectionhandler import LetterDetectionHandler
    from trafficlight.trafficlightdetectionhandler import TrafficLightDetection
    from letterdisplay.ledstriphandler import LEDStripHandler

    #Load configuration / config handler
    #Init Webserver
    #Wait for parcour setting (left/right) - new site?

    #Init communication between raspi and freedom

    #Init camera
    #CameraHandler() ??

    #Traffic Light Detection
    #TrafficLightDetection.detect_trafficlight(self, frame) needs frame!
    #TODO: Define how frame is delivered to detect_trafficlight
    #mainTrafficLightDetection = TrafficLightDetection()
    #mainTrafficLightDetection.detect_trafficlight(self, frame)

    #Init PowerLED
    #LEDStripHandler.start_powerled()

    #Letter Detection
    #LetterDetectionHandler()
    #Somehow number = LetterDetectionHandler()

    #Stop PowerLED
    #LEDStripHandler.stop_powerled()

    #Display Letter on LEDStrip
    #LEDStripHandler.display_letter_on_LEDs(number)


# ================================================================================
# main routine
# ================================================================================
if __name__ == '__main__':
    main()
