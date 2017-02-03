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
import time
import logging
import common.config.confighandler as cfg

from .trafficlightdetectionhandler import TrafficLightDetection
from logging.config import fileConfig


class TrafficLightDetectionImg(object):

    multiimg1 = cfg.get_proj_rootdir() + '/medias/images/' + cfg.get_files_multiimg1()
    multiimg2 = cfg.get_files_multiimg2()
    multiimgcount = cfg.get_files_multiimgcount()

    # Initialize the class
    def __init__(self):
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()
        self.frames = []
        for x in range(1, self.multiimgcount):
            self.frames.append(cv2.imread(self.multiimg1 + str(x) + self.multiimg2))

    # Get a frame
    def get_frame(self):
        image = self.frames[int(time.time()) % (self.multiimgcount - 1)]
        if image is None:
            return
        tld = TrafficLightDetection()
        image = tld.detect_trafficlight(image)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

        """image = Image.fromarray(image, 'RGB')   # Numpy array to image
        b, g, r = image.split() # RGB to BGR
        image = Image.merge("RGB", (r, g, b))   # Image to jpeg bytes
        output = io.BytesIO()
        image.save(output, format='JPEG')
        hex_data = output.getvalue()
        return hex_data """
