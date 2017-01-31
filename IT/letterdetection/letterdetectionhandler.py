# ================================================================================
# !/usr/bin/python
# TITLE           : letterdetectionhandler.py
# DESCRIPTION     : Handler for letter detection
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 25.10.2016
# USAGE           : python3 letterdetectionhandler.py
# VERSION         : 0.8
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

# import the necessary packages

import cv2
import logging
import common.config.confighandler as cfg
import numpy as np

from logging.config import fileConfig
from common.logging.fpshelper import FPSHelper
from common.processing.imageprocessor import ImageConverter, ImageAnalysis
from common.processing.camerahandler import CameraHandler


class LetterDetectionHandler(object):

    def __init__(_self):
        fileConfig(cfg.get_logging_config_fullpath())
        _self.__log = logging.getLogger()

        _self.FPS = FPSHelper()

        _self.__log.info("Letterdetection started")
        _self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        _self.camera = CameraHandler().get_pi_camerainstance()
        _self.rawCapture = CameraHandler().get_pi_rgbarray()

        _self.rundetection()

    def rundetection(_self):
        _self.__log.info("Start capturing")
        for frame in _self.camera.capture_continuous(_self.rawCapture, format="bgr", use_video_port=True):
            img = frame.array
            numberplate = np.zeros((100, 100), np.uint8)
            _self.FPS.start()

            redmask = ImageConverter.mask_color_red(img)
            #cv2.imshow("redmask", redmask)
            _self.__log.debug("Frame: red mask done")
            imgmarked, edges = ImageAnalysis.get_ordered_corners_drawed(redmask, img)
            _self.__log.debug("Frame: edges for letter range detection done")
            if edges != 0:
                _self.__log.debug("Frame: correct perspective of letter range")
                correctedimg = ImageConverter.transform_perspectiveview2topdownview(img, edges)
                number = ImageAnalysis.get_roman_letter(correctedimg)
                _self.FPS.stop()
                _self.__log.debug("FPS: {0:.2f}".format(_self.FPS.fps()) + " ms: {0:.2f}\n".format(_self.FPS.elapsedtime_ms()))
                cv2.putText(img, "FPS: {0:.2f}".format(_self.FPS.fps()), (cfg.get_camera_width() - 90, cfg.get_camera_height() - 10), _self.font, 0.7, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.imshow("Perspective", correctedimg)
                number = str(number)
                cv2.putText(numberplate, number, (25, 80), 0, 1, (255, 255, 255))
                cv2.imshow("Letter", numberplate)
                cv2.imshow("Video", imgmarked)
            else:
                _self.__log.debug("Frame: no letter range detected")
                _self.FPS.stop()
                _self.__log.debug("FPS: {0:.2f}".format(_self.FPS.fps()) + " ms: {0:.2f}\n".format(_self.FPS.elapsedtime_ms()))
                cv2.putText(img, "FPS: {0:.2f}".format(_self.FPS.fps()), (550, 460), _self.font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.imshow("Video", img)
            _self.rawCapture.truncate(0)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                _self.__log.info("Finished capturing")
                break
        cv2.destroyAllWindows()

if __name__ == '__main__':
    LetterDetectionHandler()
