# ================================================================================
# !/usr/bin/python
# TITLE           : imagequeueing.py
# DESCRIPTION     : Handler for Queue to analyze iamges
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 03.02.2017
# USAGE           :
# VERSION         : 0.1
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================
import multiprocessing
import logging
import common.config.confighandler as cfg

from logging.config import fileConfig
from common.processing.imageprocessor import ImageConverter, ImageAnalysis


class ImageProcessing(multiprocessing.Process):
    def __init__(self, processingqueue, resultqueue):
        multiprocessing.Process.__init__(self)
        self.processingqueue = processingqueue
        self.resultqueue = resultqueue
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()
        self.__log.setLevel(cfg.get_settings_loglevel())

    def run(self):
        proc_name = self.name
        firstrun = False
        self.__log.info('++process %s started' % proc_name)
        while True:
            queueitem = self.processingqueue.get()
            if queueitem is None and firstrun:
                self.processingqueue.task_done()
                break
            elif queueitem is None and firstrun is False:
                self.__log.warning("never processed any image...")
            else:
                self.__log.debug('calculating number with %s ...' % proc_name)
                firstrun = True
                number = queueitem()
                self.processingqueue.task_done()
                self.__log.debug('calculation done, got %s' % number)
                if number != 0:
                    self.resultqueue.put(number)
        self.__log.info('++process %s ended++' % proc_name)
        return


class ImageNumber(object):
    def __init__(self, image, edges):
        self.image = image
        self.edges = edges
        self.number = 0

    def __call__(self):
        correctedimg = ImageConverter.transform_perspectiveview2topdownview(self.image, self.edges)
        roi = ImageConverter.minimize_roi_lettercontour(correctedimg)
        self.number = ImageAnalysis.get_roman_letter(roi)
        return self.number

    def __str__(self):
        return 'Detected number: %s' % self.number
