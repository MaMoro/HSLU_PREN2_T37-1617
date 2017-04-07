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
from threading import Thread


class CameraHandler(object):
    class __CameraHandler:
        def __init__(self):
            fileConfig(cfg.get_logging_config_fullpath())
            self.__log = logging.getLogger()
            self.camera = PiCamera()
            self.rawcapture = None
            self.stream = None
            self.frame = None
            self.stopped = True
            self.brightness = 50
            self.awb = 'sunlight'

            self.__initpicamera()

        def __initpicamera(self):
            """
            This function will initialize the Raspbian Cam with the predefined settings in the configuration file
            """
            self.__log.info("PiCamera initialization started")
            self.camera.resolution = (cfg.get_camera_width(), cfg.get_camera_height())
            self.camera.framerate = cfg.get_camera_framerate()
            self.camera.iso = cfg.get_camera_iso()
            self.__log.debug("Initialize AWB, calculating...")
            time.sleep(2)
            # if cfg.get_camera_awb() == 'fixed':
            if self.awb == 'fixed':
                self.camera.shutter_speed = self.camera.exposure_speed
                self.camera.exposure_mode = 'off'
                gain = self.camera.awb_gains
                self.camera.awb_mode = 'off'
                self.camera.awb_gains = gain
            else:
                self.camera.brightness = 30
                self.camera.awb_mode = 'sunlight'
            self.rawcapture = PiRGBArray(self.camera, size=self.camera.resolution)
            self.stream = self.camera.capture_continuous(self.rawcapture, format="bgr", use_video_port=True)
            time.sleep(0.1)
            self.__log.info("PiCamera initialization finished")
            self.start()

        def calibratePiCamera(self):
            try:
                self.__log.info("Recalibrate PiCamera setting")
                self.stop()
                time.sleep(1)
                self.camera = PiCamera()
                self.__initpicamera()
                self.start()
            except:
                pass

        def get_pi_camerainstance(self):
            while self.stopped:
                time.sleep(1)
            return self.camera

        def get_pi_rgbarray(self):
            while self.stopped:
                time.sleep(1)
            return self.rawcapture

        def setbrightness(self, value):
            if 0 < value < 100:
                self.brightness = value
                self.camera.brightness = self.brightness

        def start(self):
            # start the thread to read frames from the video stream
            if self.stopped:
                t = Thread(target=self.update, args=())
                t.daemon = True
                self.stopped = False
                t.start()
                time.sleep(2)
            return self

        def update(self):
            # keep looping infinitely until the thread is stopped
            for f in self.stream:
                # grab the frame from the stream and clear the stream in preparation for the next frame
                self.frame = f.array
                self.rawcapture.truncate(0)

                # if the thread indicator variable is set, stop the thread and resource camera resources
                if self.stopped:
                    self.stream.close()
                    self.rawcapture.close()
                    self.camera.close()
                    return

        def read(self):
            if self.stopped:
                self.calibratePiCamera()
                time.sleep(2)
            return self.frame  # return the frame most recently read

        def stop(self):
            self.stopped = True  # indicate that the thread should be stopped

    instance = None

    def __new__(cls, *args, **kwargs):
        if not CameraHandler.instance:
            CameraHandler.instance = CameraHandler.__CameraHandler()
        return CameraHandler.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


