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

    def __init__(self):
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()

        self.FPS = FPSHelper()

        self.__log.info("Letterdetection started")
        self.font = cfg.get_opencv_font()
        self.camera = CameraHandler().get_pi_camerainstance()
        self.rawCapture = CameraHandler().get_pi_rgbarray()

        self.rundetection()

    def rundetection(self):
        self.__log.info("Start capturing")
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            img = frame.array
            numberplate = np.zeros((100, 100), np.uint8)
            self.FPS.start()

            redmask = ImageConverter.mask_color_red(img)
            #cv2.imshow("redmask", redmask)
            self.__log.debug("Frame: red mask done")
            imgmarked, edges = ImageAnalysis.get_ordered_corners_drawed(redmask, img)
            self.__log.debug("Frame: edges for letter range detection done")
            if edges != 0:
                self.__log.debug("Frame: correct perspective of letter range")
                correctedimg = ImageConverter.transform_perspectiveview2topdownview(img, edges)
                number = ImageAnalysis.get_roman_letter(correctedimg)
                self.FPS.stop()
                self.__log.debug("FPS: {0:.2f}".format(self.FPS.fps()) + " ms: {0:.2f}\n".format(self.FPS.elapsedtime_ms()))
                cv2.putText(img, "FPS: {0:.2f}".format(self.FPS.fps()), (cfg.get_camera_width() - 90, cfg.get_camera_height() - 10), self.font, 0.7, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.imshow("Perspective", correctedimg)
                number = str(number)
                cv2.putText(numberplate, number, (25, 80), 0, 1, (255, 255, 255))
                cv2.imshow("Letter", numberplate)
                cv2.imshow("Video", imgmarked)
            else:
                self.__log.debug("Frame: no letter range detected")
                self.FPS.stop()
                self.__log.debug("FPS: {0:.2f}".format(self.FPS.fps()) + " ms: {0:.2f}\n".format(self.FPS.elapsedtime_ms()))
                cv2.putText(img, "FPS: {0:.2f}".format(self.FPS.fps()), (550, 460), self.font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.imshow("Video", img)
            self.rawCapture.truncate(0)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                self.__log.info("Finished capturing")
                break
        cv2.destroyAllWindows()

if __name__ == '__main__':
    LetterDetectionHandler()
