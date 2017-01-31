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
        def __init__(_self):
            fileConfig(cfg.get_logging_config_fullpath())
            _self.__log = logging.getLogger()
            _self.camera = PiCamera()
            _self.rawcapture = _self.__initpicamera()

        def __initpicamera(_self):
            """
            This function will initialize the Raspbian Cam with the predefined settings in the configuration file
            :return: PIRGBArray for using as source for camera capturing
            """
            _self.__log.info("camera init started")
            _self.camera.resolution = (cfg.get_camera_width(), cfg.get_camera_height())
            _self.camera.framerate = cfg.get_camera_framerate()
            _self.camera.iso = cfg.get_camera_iso()
            _self.__log.debug("Initialize AWB, calculating...")
            time.sleep(2)
            if cfg.get_camera_awb() == 'fixed':
                _self.camera.shutter_speed = _self.camera.exposure_speed
                _self.camera.exposure_mode = 'off'
                gain = _self.camera.awb_gains
                _self.camera.awb_mode = 'off'
                _self.camera.awb_gains = gain
            rawcapture = PiRGBArray(_self.camera, size=_self.camera.resolution)
            time.sleep(0.1)
            _self.__log.debug("camera init finished")
            return rawcapture

        def updatePiCamera(_self):
            _self.__log.debug("Reconfigure PiCamera setting")
            _self.__initpicamera()

        def get_pi_camerainstance(_self):
            return _self.camera

        def get_pi_rgbarray(_self):
            return _self.rawcapture

    instance = None

    def __new__(cls, *args, **kwargs):
        if not CameraHandler.instance:
            CameraHandler.instance = CameraHandler.__CameraHandler()
        return CameraHandler.instance

    def __getattr__(_self, name):
        return getattr(_self.instance, name)

    def __setattr__(_self, name):
        return setattr(_self.instance, name)


