# =======================================================================
# title           :trafficlightdetection_video.py
# description     :This program holds the function for TrafficLightDetection on a Video
# author          :Fabrizio Rohrbach
# date            :10.11.2016
# version         :0.1
# usage           :python trafficlightdetection_video.py
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


class TrafficLightDetectionVideo(object):
    __video = cfg.get_proj_rootdir() + '/medias/videos/' + cfg.get_files_video()

    # Initialize the class
    def __init__(self):
        self.video = cv2.VideoCapture(TrafficLightDetectionVideo.__video)
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()

    # Destroy the class
    def __del__(self):
        self.video.release()

    # Get a frame
    def get_frame(self):
        success, image = self.video.read()
        if image is None:
            return
        tld = TrafficLightDetection()
        image = tld.detect_trafficlight(image)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
