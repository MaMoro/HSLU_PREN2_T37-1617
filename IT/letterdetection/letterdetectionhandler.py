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
import multiprocessing

import cv2
import logging
import common.config.confighandler as cfg
import numpy as np

from logging.config import fileConfig
from common.logging.fpshelper import FPSHelper
from common.processing.imageprocessor import ImageConverter, ImageAnalysis
from common.processing.camerahandler import CameraHandler
from letterdetection.imagequeue.images2analyze import ImageProcessing, ImageNumber
from letterdisplay.ledstriphandler import LEDStripHandler


class LetterDetectionHandler(object):
    fileConfig(cfg.get_logging_config_fullpath())

    def __init__(self):

        self.__log = logging.getLogger()
        self.__log.setLevel(cfg.get_settings_loglevel())

        self.FPS = FPSHelper()

        self.__log.info("Letterdetection started")
        self.font = cfg.get_opencv_font()
        self.camera = CameraHandler().get_pi_camerainstance()
        self.rawCapture = CameraHandler().get_pi_rgbarray()

        self.processing()

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


    def analyzeimagewithmask(self, image, edges):
        correctedimg = ImageConverter.transform_perspectiveview2topdownview(image, edges)
        number = ImageAnalysis.get_roman_letter(correctedimg)
        return number

    def processing(self):
        self.__log.info("Start processing, create ")
        num_units = 4
        processingqueue = multiprocessing.JoinableQueue()
        resultqueue = multiprocessing.Queue()
        processingunits = [ImageProcessing(processingqueue, resultqueue) for i in range(num_units)]
        for w in processingunits:
            w.start()
        self.__log.info("Start capturing")
        imgcount = 0
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            img = frame.array
            self.FPS.start()
            redmask = ImageConverter.mask_color_red(img)
            imgmarked, edges = ImageAnalysis.get_ordered_corners_drawed(redmask, img)
            #cv2.imshow("imagemarked", imgmarked)
            if edges != 0:
                self.__log.info("got edgedimage")
                processingqueue.put(ImageNumber(img, edges))
                imgcount += 1
            elif imgcount > 50:
                # TODO: stop capturing
                for i in range(num_units):
                    processingqueue.put(None)
                processingqueue.join()
                self.camera.close()
                self.rawCapture.close()
                CameraHandler().close_pi_camerainstance()
                break
            self.rawCapture.truncate(0)
            self.FPS.stop()
            self.__log.warning("fps: " + str(self.FPS.fps()))
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                self.__log.info("Finished capturing")
                break

        cv2.destroyAllWindows()

        allnumbers = []
        while resultqueue.qsize() != 0:
            allnumbers.append(resultqueue.get())
        numbertodisplay = ImageAnalysis.most_voted_number(allnumbers)
        LEDStripHandler.display_letter_on_LEDs(numbertodisplay)

    def processing2(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            img = frame.array
            cv2.imshow("video", img)
            self.rawCapture.truncate(0)
if __name__ == '__main__':
    LetterDetectionHandler()
