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
import time

from logging.config import fileConfig
from common.logging.fpshelper import FPSHelper
from common.processing.imageprocessor import ImageConverter, ImageAnalysis
from common.processing.camerahandler import CameraHandler
from common.processing.imagequeueing import ImageProcessing, ImageNumber
from letterdisplay.ledstriphandler import LEDStripHandler


class LetterDetectionHandler(object):
    fileConfig(cfg.get_logging_config_fullpath())

    def __init__(self):
        self.__log = logging.getLogger()
        self.__log.setLevel(cfg.get_settings_loglevel())
        self.FPS = FPSHelper()
        self.__log.info("Letterdetection started")
        self.font = cfg.get_opencv_font()
        self.min_amount_processed_letters = cfg.get_letter_min_amount_processed_letters()
        self.processing()
        #self.rundetection()

    def rundetection(self):
        self.__log.info("Start capturing")
        pistream = CameraHandler().start()
        while True:
            img = pistream.read()
            self.FPS.start()
            redmask = ImageConverter.mask_color_red_fullhsv(img)
            imgmarked, edges = ImageAnalysis.get_ordered_corners_drawed(redmask, img)
            if edges != 0:
                correctedimg = ImageConverter.transform_perspectiveview2topdownview(img, edges)
                cropped = ImageConverter.minimize_roi_lettercontour(correctedimg)
                numberimg = ImageAnalysis.get_roman_letter(cropped)
                self.FPS.stop()
                self.__log.info("FPS: " + str(self.FPS.fps()) + " | ms: " + str(self.FPS.elapsedtime_ms()))
                #cv2.imshow("Cropped", cropped)
                #cv2.imshow("Letter", numberimg)
                cv2.imshow("Video", imgmarked)
            else:
                self.FPS.stop()
                #self.__log.info("FPS: " + str(self.FPS.fps()) + " | ms: " + str(self.FPS.elapsedtime_ms()))
                cv2.imshow("Video", img)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                self.__log.info("Finished capturing")
                break
        CameraHandler().stop()
        cv2.destroyAllWindows()

    def processing(self):
        self.__log.info("Start processing, create Image-Processing-Units..")
        num_units = 4
        processingqueue = multiprocessing.JoinableQueue()
        resultqueue = multiprocessing.Queue()
        processingunits = [ImageProcessing(processingqueue, resultqueue) for i in range(num_units)]
        for w in processingunits:
            w.start()
        time.sleep(1)
        self.__log.info("Image-Processing-Units created, ready to process...")
        imgcount = 0
        pistream = CameraHandler().start()
        self.__log.info("Ready! Start capturing")
        while True:
            img = pistream.read()
            redmask = ImageConverter.mask_color_red_fullhsv(img)
            imgmarked, edges = ImageAnalysis.get_ordered_corners_drawed(redmask, img)
            if edges != 0:
                processingqueue.put(ImageNumber(img, edges))
                imgcount += 1
            elif imgcount > self.min_amount_processed_letters:
                # if more than specified images processed and no more edges found it's assumed that the number on the wall has passed
                for i in range(num_units):
                    processingqueue.put(None)   # enforce ImageProcessing instances to terminate
                processingqueue.join()          # waiting for alle processes to be terminated
                break

            cv2.imshow("mask", redmask)
            cv2.imshow("imagemarked", imgmarked)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                self.__log.info("Finished capturing")
                break

        CameraHandler().stop()
        cv2.destroyAllWindows()
        self.__log.info("Processed " + str(imgcount) + " images")
        allnumbers = []
        while resultqueue.qsize() != 0:
            allnumbers.append(resultqueue.get())
        numbertodisplay = ImageAnalysis.most_voted_number(allnumbers)
        LEDStripHandler.display_letter_on_LEDs(numbertodisplay)

if __name__ == '__main__':
    LetterDetectionHandler()
