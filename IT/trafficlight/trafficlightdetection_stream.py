# =======================================================================
# title           :trafficlightdetection_stream.py
# description     :This program holds the function for TrafficLightDetection on a Stream
# author          :Fabrizio Rohrbach, Marco Moro
# date            :03.02.2017
# version         :0.2
# usage           :python trafficlightdetection_stream.py
# notes           :
# python_version  :3.5.2
# opencv_version  :3.1.0
# =======================================================================

# Import the modules needed to run the script.
import cv2
import logging
import common.config.confighandler as cfg

from .trafficlightdetectionhandler import TrafficLightDetection
from logging.config import fileConfig


class TrafficLightDetectionStream(object):
    # Initialize the class
    def __init__(self):
        self.video = cv2.VideoCapture(cfg.get_files_stream())
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()

    # Destroy the class
    def __del__(self):
        self.video.release()

    # Get a frame
    def get_frame(self):
        ret, frame = self.video.read()
        if frame is None:
            return
        tld = TrafficLightDetection()
        frame = tld.detect_trafficlight(frame)
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
