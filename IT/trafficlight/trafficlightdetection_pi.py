# =======================================================================
# title           :trafficlightdetection_pi.py
# description     :This program holds the function for TrafficLightDetection on Raspberry Pi
# author          :Fabrizio Rohrbach
# date            :10.11.2016
# version         :0.1
# usage           :python trafficlightdetection_pi.py
# notes           :
# python_version  :3.5.2
# opencv_version  :3.1.0
# =======================================================================

# Import the modules needed to run the script.
import cv2
import threading
import configparser
import time
import os
import sys
import picamera

from ..trafficlight.trafficlightdetectionhandler import TrafficLightDetection
from ..common.logging.fpshelper import FPSHelper
from ..common.logging.loghelper import LogHelper
from picamera.array import PiRGBArray


class TrafficLightDetectionPi(object):
    # Function for converting string to boolean (for example if in Config.ini)
    def str2bool(v):
        return v.lower() in ("yes", "Yes", "YES", "true", "True", "TRUE", "1", "t")

    # Initialize Logger and FPS Helpers
    LOG = LogHelper()
    FPS = FPSHelper()

    # Set root dir for project (needed for example the Config.ini)
    ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)

    # Initialize ConfigParser and read Settings
    config = configparser.ConfigParser()
    config.read(ROOT_DIR + '/common/config/config.ini')

    # Load needed settings from Config.ini into variables (so you dont have to access the ini file each time)
    camera_width = int(config['camera']['width'])
    camera_height = int(config['camera']['height'])
    camera_framerate = int(config['camera']['framerate'])
    camera_iso = int(config['camera']['iso'])
    camera_awb = config['camera']['awb']

    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    # Initialize the class
    def __init__(_self):
        _self.initialize()

    def initialize(_self):
        if _self.thread is None:
            # start background frame thread
            _self.thread = threading.Thread(target=_self._thread)
            _self.last_access = time.time()
            _self.thread.start()

            # wait until frames start to be available
            while _self.frame is None:
                time.sleep(0)

    # Get a frame
    def get_frame(_self):
        _self.last_access = time.time()
        _self.initialize()
        return _self.frame

    @classmethod
    def _thread(cls):

        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (TrafficLightDetectionPi.camera_width, TrafficLightDetectionPi.camera_height)
            camera.framerate = TrafficLightDetectionPi.camera_framerate
            camera.iso = TrafficLightDetectionPi.camera_iso
            time.sleep(2)
            if TrafficLightDetectionPi.camera_awb == 'fixed':
                camera.shutter_speed = camera.exposure_speed
                camera.exposure_mode = 'off'
                gain = camera.awb_gains
                camera.awb_mode = 'off'
                camera.awb_gains = gain
            rawCapture = PiRGBArray(camera,
                                    size=(TrafficLightDetectionPi.camera_width, TrafficLightDetectionPi.camera_height))
            # let camera warm up
            time.sleep(0.1)
            TrafficLightDetectionPi.last_access = time.time()

            for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
                image = frame.array
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                tld = TrafficLightDetection()
                data = tld.detect_trafficlight(image_rgb)
                _, jpeg = cv2.imencode('.jpg', data)
                cls.frame = jpeg.tobytes()
                rawCapture.truncate(0)

                t = time.time()
                if t - TrafficLightDetectionPi.last_access > 20:
                    break
        cls.thread = None
