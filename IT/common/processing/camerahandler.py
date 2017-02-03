# ================================================================================
# !/usr/bin/python
# TITLE           : camerahandler.py
# DESCRIPTION     : Handler for PiCamera
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 25.10.2016
# USAGE           :
# VERSION         : 0.8
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

# import the necessary packages
import logging
import time
import common.config.confighandler as cfg

from logging.config import fileConfig
from picamera.array import PiRGBArray
from picamera import PiCamera


class CameraHandler(object):
    class __CameraHandler:
        def __init__(self):
            fileConfig(cfg.get_logging_config_fullpath())
            self.__log = logging.getLogger()
            self.camera = PiCamera()
            self.rawcapture = self.__initpicamera()
            self.instanceclosed = False

        def __initpicamera(self):
            """
            This function will initialize the Raspbian Cam with the predefined settings in the configuration file
            :return: PIRGBArray for using as source for camera capturing
            """
            self.__log.info("camera init started")
            self.camera.resolution = (cfg.get_camera_width(), cfg.get_camera_height())
            self.camera.framerate = cfg.get_camera_framerate()
            self.camera.iso = cfg.get_camera_iso()
            self.__log.debug("Initialize AWB, calculating...")
            time.sleep(2)
            if cfg.get_camera_awb() == 'fixed':
                self.camera.shutter_speed = self.camera.exposure_speed
                self.camera.exposure_mode = 'off'
                gain = self.camera.awb_gains
                self.camera.awb_mode = 'off'
                self.camera.awb_gains = gain
            rawcapture = PiRGBArray(self.camera, size=self.camera.resolution)
            time.sleep(0.1)
            self.__log.debug("camera init finished")
            self.instanceclosed = False
            return rawcapture

        def reopenPiCamera(self):
            self.__log.info("Reconfigure PiCamera setting")
            self.camera = PiCamera()
            self.rawcapture = self.__initpicamera()

        def get_pi_camerainstance(self):
            if self.instanceclosed:
                self.reopenPiCamera()
            return self.camera

        def get_pi_rgbarray(self):
            if self.instanceclosed:
                self.reopenPiCamera()
            return self.rawcapture

        def close_pi_camerainstance(self):
            self.instanceclosed = True
            self.camera.close()

    instance = None

    def __new__(cls, *args, **kwargs):
        if not CameraHandler.instance:
            CameraHandler.instance = CameraHandler.__CameraHandler()
        return CameraHandler.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


