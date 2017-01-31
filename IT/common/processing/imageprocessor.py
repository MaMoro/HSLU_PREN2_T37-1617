# ================================================================================
# !/usr/bin/python
# TITLE           : imageprocessor.py
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
import numpy as np

class ImageConverter(object):
    @staticmethod
    def convertbgr2gray(image):
        return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    @staticmethod
    def convertbgr2hsv(image):
        return cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
