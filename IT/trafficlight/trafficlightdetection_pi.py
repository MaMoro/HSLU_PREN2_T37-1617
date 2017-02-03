# =======================================================================
# title           :trafficlightdetection_pi.py
# description     :This program holds the function for TrafficLightDetection on Raspberry Pi
# author          :Marco Moro
# date            :03.02.2017
# version         :0.2
# usage           :python trafficlightdetection_pi.py
# notes           :
# python_version  :3.5.2
# opencv_version  :3.1.0
# =======================================================================

# Import the modules needed to run the script.
import cv2
import time
import logging
import threading
import common.config.confighandler as cfg

from .trafficlightdetectionhandler import TrafficLightDetection
from logging.config import fileConfig
from common.processing.camerahandler import CameraHandler


class TrafficLightDetectionPi(object):

    camera = None
    rawCapture = None
    stream = None
    frame = None
    thread = None
    last_access = 0
    stopped = False

    # Initialize the class
    def __init__(self):
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()
        self.start()

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self._thread)
            self.last_access = time.time()
            self.thread.start()

            while self.frame is None:
                time.sleep(0)

    # Get a frame
    def get_frame(self):
        self.last_access = time.time()
        self.start()
        return self.frame

    @classmethod
    def _thread(cls):
        cls.last_access = time.time()
        if cls.camera is None or cls.rawCapture is None or cls.stream is None:
            cls.camera = CameraHandler().get_pi_camerainstance()
            cls.rawCapture = CameraHandler().get_pi_rgbarray()
            cls.stream = cls.camera.capture_continuous(cls.rawCapture, format="bgr", use_video_port=True)
        for f in cls.stream:
            image = f.array
            tld = TrafficLightDetection()
            data = tld.detect_trafficlight(image)
            _, jpeg = cv2.imencode('.jpg', data)
            cls.frame = jpeg.tobytes()
            cls.rawCapture.truncate(0)

            t = time.time()
            if cls.stopped or t - cls.last_access > 20:
                cls.stream.close()
                cls.rawCapture.close()
                CameraHandler().close_pi_camerainstance()
                break
        cls.thread = None

    def stop(self):
        self.stopped = True
