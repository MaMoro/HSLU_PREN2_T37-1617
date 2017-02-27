# ================================================================================
# !/usr/bin/python
# TITLE           : parcoursstatehandler.py
# DESCRIPTION     : Handler for parcours and its state
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 30.01.2017
# USAGE           :
# VERSION         : 0.1
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

# import the necessary packages
import logging
import time
import common.config.confighandler as cfg
from threading import Thread

from logging.config import fileConfig
from parcours.parcourstate import ParcoursState


class ParcoursStateHandler:
    class __ParcoursStateHandler:
        def __init__(self):
            fileConfig(cfg.get_logging_config_fullpath())
            self.__log = logging.getLogger()
            self.stopped = False
            self.currentParcoursState = ParcoursState.NotInitalized
            self.__initparcours()

        def __initparcours(self):
            """
            This function will initialize the ParcoursStateHandler with the predefined settings in the configuration file
            """
            self.__log.info("Parcours initialization started")

        def start(self):
            # start the thread to read frames from the video stream
            t = Thread(target=self.update, args=())
            t.daemon = True
            self.stopped = False
            t.start()
            time.sleep(1)
            return self

        def setcurrentstate(self, state):
            if isinstance(state, ParcoursState):
                self.currentParcoursState = state
            elif (state).is_integer():
                self.currentParcoursState = ParcoursState(state)
            else:
                self.__log.warning("State unknown, tried to set " + str(state))
                self.currentParcoursState = ParcoursState.Error

        def getcurrentstate(self):
            if self.stopped:
                self.calibratePiCamera()
            return self.frame  # return the frame most recently read

        def stop(self):
            self.stopped = True  # indicate that the thread should be stopped

    instance = None

    def __new__(cls, *args, **kwargs):
        if not ParcoursStateHandler.instance:
            ParcoursStateHandler.instance = ParcoursStateHandler.__ParcoursStateHandler()
        return ParcoursStateHandler.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
