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
from threading import Thread
from common.logging.fpshelper import FPSHelper
from common.processing.imageanalysis import ImageAnalysis
from common.processing.imageconverter import ImageConverter
from common.processing.imagequeueing import ImageProcessing, ImageNumber
from common.processing.camerahandler import CameraHandler
from common.communication.communicationvalues import CommunicationValues
from letterdisplay.ledstriphandler import LEDStripHandler


class LetterDetectionHandler(object):
    class __LetterDetectionHandler:
        fileConfig(cfg.get_logging_config_fullpath())

        def __init__(self):
            self.__log = logging.getLogger()
            self.__log.setLevel(cfg.get_settings_loglevel())
            self.__log.info("Letterdetection started")
            #self.FPS = FPSHelper()
            self.frame = None
            self.stopped = True
            self.numbertodisplay = 0
            self.processingqueue = 0
            self.resultqueue = 0
            self.num_processing_units = 4
            self.font = cfg.get_opencv_font()
            self.min_amount_processed_letters = cfg.get_letter_min_amount_processed_letters()
            self.initqueues()

        def start(self):
            # start the thread to read frames from the video stream
            if self.stopped:
                #t = Thread(target=self.processing, args=())
                #t = Thread(target=self.rundetection, args=())
                t = Thread(target=self.processing_prod, args=())
                t.daemon = True
                self.stopped = False
                t.start()
                t.join()
            return self.numbertodisplay

        def starttest(self):
            # start the thread to read frames from the video stream
            if self.stopped:
                t = Thread(target=self.rundetection, args=())
                t.daemon = True
                self.stopped = False
                t.start()
                t.join()
            return self.numbertodisplay

        def stop(self):
            self.stopped = True  # indicate that the thread should be stopped

        def rundetection(self):
            self.__log.info("Start capturing")
            pistream = CameraHandler()

            while True:
                self.frame = pistream.read()
                #self.FPS.start()
                redmask = ImageConverter.mask_color_red_fullhsv(self.frame)
                imgmarked, edges = ImageAnalysis.get_ordered_corners_drawed(redmask, self.frame)
                if edges != 0:
                    correctedimg = ImageConverter.transform_perspectiveview2topdownview(self.frame, edges)
                    cropped = ImageConverter.minimize_roi_lettercontour(correctedimg)
                    try:
                        numberimg = ImageAnalysis.get_roman_letter_drawed(cropped)
                        cv2.imshow("Letter", numberimg)
                    except:
                        self.__log.error("hmmmm....")

                    # self.FPS.stop()
                    #self.__log.info("FPS: " + str(self.FPS.fps()) + " | ms: " + str(self.FPS.elapsedtime_ms()))
                    cv2.imshow("Transformed", correctedimg)
                    cv2.imshow("Cropped", cropped)

                    cv2.imshow("Video", imgmarked)
                    cv2.imshow("redmask", redmask)
                else:
                    #self.FPS.stop()
                    # self.__log.info("FPS: " + str(self.FPS.fps()) + " | ms: " + str(self.FPS.elapsedtime_ms()))
                    cv2.imshow("Video", self.frame)

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
            self.__log.info("Image-Processing-Units created, ready to process...")
            imgcount = 0
            LEDStripHandler.start_powerled()
            pistream = CameraHandler()

            self.__log.info("Ready! Start capturing")

            while True:
                self.frame = pistream.read()
                redmask = ImageConverter.mask_color_red_fullhsv(self.frame)
                imgmarked, edges = ImageAnalysis.get_ordered_corners_drawed(redmask, self.frame)
                if edges != 0:
                    processingqueue.put(ImageNumber(self.frame, edges))
                    imgcount += 1
                elif imgcount > self.min_amount_processed_letters:
                    # if more than specified images processed and no more edges found it's assumed that the number on the wall has passed
                    for i in range(num_units):
                        processingqueue.put(None)  # enforce ImageProcessing instances to terminate
                    processingqueue.join()  # waiting for alle processes to be terminated
                    break

                #cv2.imshow("mask", redmask)
                cv2.imshow("imagemarked", imgmarked)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    self.__log.info("Finished capturing")
                    break

            CameraHandler().stop()
            cv2.destroyAllWindows()
            self.__log.info("Processed " + str(imgcount) + " images")
            allnumbers = []
            print(resultqueue.qsize())
            while resultqueue.qsize() != 0:
                allnumbers.append(resultqueue.get())
            numbertodisplay = ImageAnalysis.most_voted_number(allnumbers)
            LEDStripHandler.display_letter_on_LEDs(numbertodisplay)
            time.sleep(5)
            LEDStripHandler.stop_powerled()
            LEDStripHandler.turn_off_all_letter_LEDS()
            # CommunicationValues().send_letter(numbertodisplay)

        def processing_prod(self):
            imgcount = 0
            pistream = CameraHandler()
            self.__log.info("Ready! Start capturing")

            while True:
                self.frame = pistream.read()
                redmask = ImageConverter.mask_color_red_fullhsv(self.frame)
                edges = ImageAnalysis.get_ordered_corners(redmask)
                if edges != 0:
                    self.processingqueue.put(ImageNumber(self.frame, edges))
                    imgcount += 1
                elif imgcount > self.min_amount_processed_letters:
                    # if more than specified images processed and no more edges found it's assumed that the number on the wall has passed
                    for i in range(self.num_processing_units):
                        self.processingqueue.put(None)  # enforce ImageProcessing instances to terminate
                    self.processingqueue.join()  # waiting for alle processes to be terminated
                    break

            CameraHandler().stop()
            self.__log.info("Processed " + str(imgcount) + " images")
            allnumbers = []

            while self.resultqueue.qsize() != 0:
                allnumbers.append(self.resultqueue.get())
            self.numbertodisplay = ImageAnalysis.most_voted_number(allnumbers)

        def initqueues(self):
            self.__log.info("Start processing, create Image-Processing-Units..")
            self.processingqueue = multiprocessing.JoinableQueue()
            self.resultqueue = multiprocessing.Queue()
            processingunits = [ImageProcessing(self.processingqueue, self.resultqueue) for i in range(self.num_processing_units)]
            for w in processingunits:
                w.start()
            self.__log.info("Image-Processing-Units created, ready to process...")

        def get_frame(self):
            return self.frame  # return the frame most recently read

    instance = None

    def __new__(cls, *args, **kwargs):
        if not LetterDetectionHandler.instance:
            LetterDetectionHandler.instance = LetterDetectionHandler.__LetterDetectionHandler()
        return LetterDetectionHandler.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

if __name__ == '__main__':
    """serialcomm = CommunicationValues()
    serialcomm.send_hello()
    hellostate = serialcomm.get_hello_blocking()  # await hello response or timeout...
    time.sleep(2)
    serialcomm.send_course(1)

    # Init camera
    print("Starting CameraHandling and start Trafficlight detection...")
    LetterDetectionHandler()
    time.sleep(5)
    serialcomm.send_start()"""
    ldh = LetterDetectionHandler()
    ldh.starttest()
    #numbertodisplay = ldh.start()
    #print("snömmerli esch: " + str(numbertodisplay))
