# =======================================================================
# title           :trafficlightdetection_pi.py
# description     :This program holds the function for TrafficLightDetection on Raspberry Pi
# author          :Marco Moro
# date            :03.02.2017
# version         :0.2
# usage           :python trafficlightdetection_pi.py
# notes           :
# python_version  :3.5.2
# opencv_version  :3.1.0
# =======================================================================

# Import the modules needed to run the script.
import time
import logging
import cv2

import common.config.confighandler as cfg

from trafficlight.trafficlightdetectionhandler import TrafficLightDetection
from logging.config import fileConfig
from common.processing.camerahandler import CameraHandler
from threading import Thread


class TrafficLightDetectionPi(object):
    # Initialize the class
    def __init__(self):
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()
        self.__log.setLevel(cfg.get_settings_loglevel())
        self.stopped = True
        self.frame = None
        self.greencount = 0
        self.pistream = CameraHandler().start()
        self.start()

    def start(self):
        if self.stopped:
            t = Thread(target=self.update, args=())
            t.daemon = True
            self.stopped = False
            t.start()
            time.sleep(0.5)
            return self

    def getstatus(self):
        if self.greencount < 10:
            return "red"
        else:
            return "green"

    def updatestatus(self, status):
        if status:
            self.greencount += 1
        else:
            self.greencount = 0

    def update(self):
        while not self.stopped:
            img = self.pistream.read()
            tld = TrafficLightDetection()
            self.frame = tld.detect_trafficlight(img)
            self.updatestatus(tld.get_color_state())
            #cv2.imshow("trafficlight", self.frame)
            #cv2.imshow("red", redimg)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                self.__log.info("Finished capturing")
                break

    def stop(self):
        self.stopped = True
        CameraHandler().stop()

if __name__ == '__main__':
    t = TrafficLightDetectionPi()
    while t.getstatus() == "red":
        time.sleep(0.3)
    print("yeey greeen")
    t.stop()
    time.sleep(999)
