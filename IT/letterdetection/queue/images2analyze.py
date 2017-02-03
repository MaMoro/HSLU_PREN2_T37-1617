# ================================================================================
# !/usr/bin/python
# TITLE           : ledstriphandler.py
# DESCRIPTION     : Handler for Queue to analyze iamges
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 03.02.2017
# USAGE           :
# VERSION         : 0.1
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

import queue
import logging
from threading import Thread

import common.config.confighandler as cfg
from logging.config import fileConfig


class ImageQueue:
    class __ImageQueue:

        def __init__(self):
            self.queue = queue.Queue(maxsize=100)

        def get_queue(self):
            return self.queue

    instance = None

    def __new__(cls, *args, **kwargs):
        if not ImageQueue.instance:
            ImageQueue.instance = ImageQueue.__ImageQueue()
        return ImageQueue.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class ImageEnqueuer(Thread):

    def __init__(self):
        Thread.__init__(self)
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()

    def run(self):
        first = False
        while True:
            img = None  # TODO: call image detection with image as return
            if img is not None:
                if not ImageQueue.get_queue().full():
                    ImageQueue.get_queue().put(img)
                    first = True
                    self.__log.info("Image inserted in AnalyzeQueue")
            elif first:
                self.__log.info("no more images")
                break
        return
