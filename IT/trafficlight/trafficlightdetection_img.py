# =======================================================================
# title           :trafficlightdetection_img.py
# description     :This program holds the function for TrafficLightDetection on Images
# author          :Fabrizio Rohrbach
# date            :10.11.2016
# version         :0.1
# usage           :python trafficlightdetection_img.py
# notes           :
# python_version  :3.5.2
# opencv_version  :3.1.0
# =======================================================================

# Import the modules needed to run the script.
import cv2
import io
import configparser
import os

from time import time
from PIL import Image
from .trafficlightdetectionhandler import TrafficLightDetection
from common.logging.loghelper import LogHelper
from common.logging.fpshelper import FPSHelper


class TrafficLightDetectionImg(object):
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
    multiimg1 = ROOT_DIR + '/medias/images/' + config['files']['multiimg1']
    multiimg2 = config['files']['multiimg2']
    multiimgcount = int(config['files']['multiimgcount'])

    # Initialize the class
    def __init__(_self):
        _self.frames = []
        for x in range(1, _self.multiimgcount):
            _self.frames.append(cv2.imread(_self.multiimg1 + str(x) + _self.multiimg2))

    # Get a frame
    def get_frame(_self):
        image = _self.frames[int(time()) % (_self.multiimgcount - 1)]
        if image is None:
            return
        tld = TrafficLightDetection()
        image = tld.detect_trafficlight(image)
        # Numpy array to image
        image = Image.fromarray(image, 'RGB')
        # RGB to BGR
        b, g, r = image.split()
        image = Image.merge("RGB", (r, g, b))
        # Image to jpeg bytes
        output = io.BytesIO()
        image.save(output, format='JPEG')
        hex_data = output.getvalue()

        return hex_data
