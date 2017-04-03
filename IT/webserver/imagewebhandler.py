# ================================================================================
# !/usr/bin/python
# TITLE           : imagewebhandler.py
# DESCRIPTION     : Handler for images for web interface from different sources
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 03.04.2017
# USAGE           :
# VERSION         : 0.1
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

# import the necessary packages
import logging
import cv2

import common.config.confighandler as cfg
from threading import Thread
from logging.config import fileConfig


class ImageWebHandler(object):
    class __ImageWebHandler:
        def __init__(self):
            fileConfig(cfg.get_logging_config_fullpath())
            self.__log = logging.getLogger()
            self.frame = None
            self.waitframe = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/keepcalm.png')
            self.start()

        def get_frame(self):
            if self.frame is None:
                currentframe = self.waitframe
            else:
                currentframe = self.frame
            _, imagepng = cv2.imencode('.png', currentframe)
            return imagepng.tobytes()

        def set_frame(self, frame):
            self.frame = frame

        def start(self):
            thread = Thread()
            thread.daemon = True
            thread.start()
            return self

    instance = None

    def __new__(cls, *args, **kwargs):
        if not ImageWebHandler.instance:
            ImageWebHandler.instance = ImageWebHandler.__ImageWebHandler()
        return ImageWebHandler.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
