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
import configparser
import os
import sys

from .trafficlightdetectionhandler import TrafficLightDetection
from common.logging.loghelper import LogHelper
from common.logging.fpshelper import FPSHelper


class TrafficLightDetectionVideo(object):
    # Function for converting string to boolean (for example if in Config.ini)
    def str2bool(v):
        return v.lower() in ("yes", "Yes", "YES", "true", "True", "TRUE", "1", "t")

    # Initialize Logger and FPS Helpers
    LOG = LogHelper()
    FPS = FPSHelper()

    # Set root dir for project (needed for example the Config.ini)
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Initialize ConfigParser and read Settings
    config = configparser.ConfigParser()
    config.read(ROOT_DIR + '/common/config/config.ini')

    # Load needed settings from Config.ini into variables (so you dont have to access the ini file each time)
    video = ROOT_DIR + '/medias/videos/' + config['files']['video']

    # Initialize the class
    def __init__(_self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        _self.video = cv2.VideoCapture(_self.video)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.

    # Destroy the class
    def __del__(_self):
        _self.video.release()

    # Get a frame
    def get_frame(_self):
        success, image = _self.video.read()
        if image is None:
            return
        tld = TrafficLightDetection()
        image = tld.detect_trafficlight(image)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
