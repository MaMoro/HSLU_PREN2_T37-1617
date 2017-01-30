# =======================================================================
# title           :trafficlightdetectionhandler.py
# description     :This program holds the main logic for the TrafficLightDetection
# author          :Fabrizio Rohrbach
# date            :10.11.2016
# version         :0.1
# usage           :python trafficlightdetectionhandler.py
# notes           :
# python_version  :3.5.2
# opencv_version  :3.1.0
# =======================================================================

# Import the modules needed to run the script.
import numpy as np
import cv2
import datetime
import configparser
import os
import sys

from ..common.logging.fpshelper import FPSHelper
from ..common.logging.loghelper import LogHelper
from timeit import default_timer as timer


class TrafficLightDetection(object):
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
    config.read(ROOT_DIR + '/Core/Config.ini')

    # Load needed settings from Config.ini into variables (so you dont have to access the ini file each time)
    output_red = str2bool(
        config['debug']['output_red'])  # write image with red pixels to disk after apply red color mask if True
    output_green = str2bool(
        config['debug']['output_green'])  # write image with green pixels to disk after apply green color mask if True
    output_bgwhite = str2bool(
        config['debug']['output_bgwhite'])  # set background color of output images to white instead of black if True
    debug = str2bool(config['settings']['debug'])  # print debug informations if True
    cropheight = int(config['cropimage']['height'])  # height of the cropped image after first red pixel is found
    cropwidth = int(config['cropimage']['width'])  # width of the cropped image after first red pixel is found
    camera_width = int(config['camera']['width'])  # width of the captured image
    camera_height = int(config['camera']['height'])  # height of the captured image
    color_green = [int(c) for c in
                   config['color']['green'].split(',')]  # rgb values for green -> used for writing on image
    bordersize_left = int(config['imagetext']['bordersize_left'])  # position left of text on the image
    bordersize_top = int(config['imagetext']['bordersize_top'])  # position top of text on the image
    bordersize_bottom = int(config['imagetext']['bordersize_bottom'])  # position bottom of text on the image
    bordersize_right = int(config['imagetext']['bordersize_right'])  # position left of text on the image
    textspace = int(config['imagetext']['textspace'])  # space between text lines on image

    # Load Masks from Config.ini
    lower_red0 = np.array([int(c) for c in config['mask_trafficlight']['red_low_l'].split(',')])
    upper_red0 = np.array([int(c) for c in config['mask_trafficlight']['red_low_h'].split(',')])
    lower_red1 = np.array([int(c) for c in config['mask_trafficlight']['red_high_l'].split(',')])
    upper_red1 = np.array([int(c) for c in config['mask_trafficlight']['red_high_h'].split(',')])
    lower_green = np.array([int(c) for c in config['mask_trafficlight']['green_l'].split(',')])
    upper_green = np.array([int(c) for c in config['mask_trafficlight']['green_h'].split(',')])

    # Initialize the class
    def __init__(_self):
        _self.redpixelx = 0
        _self.redpixely = 0
        _self.redfound = False
        _self.croppointx = 0
        _self.croppointy = 0
        _self.cropnewpointx = 0
        _self.cropnewpointy = 0
        _self.frame = 0
        _self.image_original = 0
        _self.start_time = 0
        _self.end_time = 0
        _self.green_image_bgr = 0
        _self.red_image_bgr = 0
        _self.maxLoc = 0
        _self.green_color = 0
        _self.red_color = 0
        _self.green_count = 0
        _self.red_count = 0
        return

    # Main logic for TrafficLightDetection
    def detect_trafficlight(_self, frame):
        _self.start_time = timer()

        _self.frame = frame
        _self.image_original = frame.copy()

        _self.crop_image()
        _self.get_brightest_redpixel()
        _self.get_brightest_greenpixel()
        _self.detect_brighter_color()

        return _self.image_original

    # Crop the image
    def crop_image(_self):
        # Crop the image after first red pixel in range found
        if _self.redfound and _self.redpixelx != 0 and _self.redpixely != 0:
            _self.croppointx = _self.redpixelx - 25
            _self.croppointy = _self.redpixely - 25
            _self.cropnewpointx = _self.croppointx + _self.cropwidth + 25
            _self.cropnewpointy = _self.croppointy + _self.cropheight + 25
            _self.LOG.debug("Croppoint %d|%d Croppoint2 %d|%d" % (
            _self.croppointx, _self.croppointy, _self.cropnewpointx, _self.cropnewpointy))
            crop_img = _self.frame[_self.croppointy:_self.cropnewpointy, _self.croppointx:_self.cropnewpointx]
            cv2.rectangle(_self.image_original, (_self.croppointx, _self.croppointy),
                          (_self.cropnewpointx, _self.cropnewpointy), (0, 0, 255), 2)
            _self.frame = crop_img

    # Get the brightest red pixel on frame
    def get_brightest_redpixel(_self):
        # --- Get red pixels ---
        # copy image
        red_image = _self.frame.copy()
        # convert to HSV
        red_image_hsv = cv2.cvtColor(red_image, cv2.COLOR_BGR2HSV)

        red_image_mask0 = cv2.inRange(red_image_hsv, _self.lower_red0, _self.upper_red0)
        red_image_mask1 = cv2.inRange(red_image_hsv, _self.lower_red1, _self.upper_red1)

        # join my masks
        red_image_mask = red_image_mask0 + red_image_mask1

        # use mask
        red_image_output = cv2.bitwise_and(red_image_hsv, red_image_hsv, mask=red_image_mask)
        # to BGR
        _self.red_image_bgr = cv2.cvtColor(red_image_output, cv2.COLOR_HSV2BGR)

        # --- Count the red pixels ---
        # Convert HSV to GRAY
        red_count_image = cv2.cvtColor(_self.red_image_bgr, cv2.COLOR_HSV2BGR)
        red_count_image = cv2.cvtColor(red_count_image, cv2.COLOR_BGR2GRAY)
        # Count red
        _self.red_count = cv2.countNonZero(red_count_image)

        # Check if any red pixels are left after apply red color mask
        if _self.red_count > 0:
            # --- Find brightest spot ---
            # copy image
            red_rect_image = _self.red_image_bgr.copy()
            # convert to gray
            red_rect_image_gray = cv2.cvtColor(red_rect_image, cv2.COLOR_BGR2GRAY)
            # perform a naive attempt to find the (x, y) coordinates of the area of the image with the largest intensity value
            (minVal, maxVal, minLoc, _self.maxLoc) = cv2.minMaxLoc(
                red_rect_image_gray)  # get position of pixel with max grey value

            # Draw a circle around the detected red pixel
            if _self.redfound and _self.redpixelx != 0 and _self.redpixely != 0:  # if first red pixel is found, draw on cropped image
                cv2.circle(_self.image_original,
                           (_self.croppointx + _self.maxLoc[0], _self.croppointy + _self.maxLoc[1]), 5, (0, 0, 255), 2)
            else:
                cv2.circle(_self.image_original, _self.maxLoc, 5, (0, 0, 255), 2)  # draw on original image
                _self.red_color = np.uint8(
                    [[red_rect_image_gray[_self.maxLoc[1], _self.maxLoc[0]]]])  # get value of brightest gray pixel
        else:  # if no red pixels are left after apply red color mask, set value to 0
            _self.red_color = 0

    # Get the brightest green pixel on frame
    def get_brightest_greenpixel(_self):
        # --- Get green pixels ---
        # copy image
        green_image = _self.frame.copy()
        # convert to HSV
        green_image_hsv = cv2.cvtColor(green_image, cv2.COLOR_BGR2HSV)

        green_image_mask = cv2.inRange(green_image_hsv, _self.lower_green, _self.upper_green)
        # use mask
        green_image_output = cv2.bitwise_and(green_image_hsv, green_image_hsv, mask=green_image_mask)
        # to BGR
        _self.green_image_bgr = cv2.cvtColor(green_image_output, cv2.COLOR_HSV2BGR)

        # --- Count the green pixels ---
        # Convert HSV to GRAY
        green_count_image = cv2.cvtColor(_self.green_image_bgr, cv2.COLOR_HSV2BGR)
        green_count_image = cv2.cvtColor(green_count_image, cv2.COLOR_BGR2GRAY)
        # Count green
        _self.green_count = cv2.countNonZero(green_count_image)

        if _self.green_count > 0:
            # --- Find brightest spot ---
            # copy image
            green_rect_image = _self.green_image_bgr.copy()
            # convert to gray
            green_rect_image_gray = cv2.cvtColor(green_rect_image, cv2.COLOR_BGR2GRAY)
            # perform a naive attempt to find the (x, y) coordinates of the area of the image with the largest intensity value
            (minVal, maxVal, minLoc, _self.maxLoc) = cv2.minMaxLoc(
                green_rect_image_gray)  # get position of pixel with max grey value

            # Draw a circle around the detected green pixel
            if _self.redfound and _self.redpixelx != 0 and _self.redpixely != 0:  # if first red pixel is found, draw on cropped image
                cv2.circle(_self.image_original,
                           (_self.croppointx + _self.maxLoc[0], _self.croppointy + _self.maxLoc[1]), 5, (0, 255, 0), 2)
            else:
                cv2.circle(_self.image_original, _self.maxLoc, 5, (0, 255, 0), 2)  # draw on original image
                _self.green_color = np.uint8(
                    [[green_rect_image_gray[_self.maxLoc[1], _self.maxLoc[0]]]])  # get value of brightest gray pixel
        else:  # if no green pixels are left after apply green color mask, set value to 0
            _self.green_color = 0

    # Find out which pixel is brighter (red or green)
    def detect_brighter_color(_self):
        _self.end_time = timer()

        ms = (_self.end_time - _self.start_time) * 1000
        fps = 1 / (_self.end_time - _self.start_time)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL

        # Add border to frame
        _self.image_original = cv2.copyMakeBorder(_self.image_original, _self.bordersize_top, _self.bordersize_bottom,
                                                  _self.bordersize_left, _self.bordersize_right, cv2.BORDER_CONSTANT, 0)

        # Debug
        if _self.debug:
            # Debug green and red pixel count
            _self.LOG.debug("red count: " + str(_self.red_count) + " | green count: " + str(_self.green_count))
            cv2.putText(_self.image_original,
                        "red count: " + str(_self.red_count) + " | green count: " + str(_self.green_count),
                        (_self.textspace, (2 * _self.textspace)), font, 0.7,
                        _self.color_green, 1, cv2.LINE_AA)
            # Debug grey pixel values (of original green and red pixel)
            _self.LOG.debug("red color: " + str(_self.red_color) + " | green color: " + str(_self.green_color))
            cv2.putText(_self.image_original,
                        "red color: " + str(_self.red_color) + " | green color: " + str(_self.green_color),
                        (_self.textspace, (3 * _self.textspace)), font, 0.7,
                        _self.color_green, 1, cv2.LINE_AA)
            # Debug FPS
            _self.LOG.debug("FPS: {0:.2f}".format(fps) + " ms: {0:.2f}\n".format(ms))
            cv2.putText(_self.image_original, "FPS: {0:.2f}".format(fps),
                        ((_self.camera_width + _self.bordersize_right + _self.bordersize_left) - 100 - _self.textspace,
                         (_self.camera_height + _self.bordersize_top + _self.bordersize_bottom) - _self.textspace),
                        font, 0.7,
                        _self.color_green, 1, cv2.LINE_AA)
        # Red detected
        if _self.red_color > _self.green_color:
            if not _self.redfound:
                _self.redfound = True
                _self.redpixelx = _self.maxLoc[0]
                _self.redpixely = _self.maxLoc[1]
                _self.LOG.info('{:%H:%M:%S.%f} - Red detected!'.format(datetime.datetime.now()))
            cv2.putText(_self.image_original, '{:%H:%M:%S.%f} - Red detected!'.format(datetime.datetime.now()),
                        (_self.textspace, _self.textspace), font, 0.7,
                        _self.color_green, 1, cv2.LINE_AA)
            if _self.output_red:
                if _self.output_bgwhite:
                    _self.red_image_bgr[np.where((_self.red_image_bgr == [0, 0, 0]).all(axis=2))] = [255, 255, 255]
                cv2.imwrite("red.png", _self.red_image_bgr)
        # Green detected
        elif _self.red_color < _self.green_color:
            _self.LOG.info('{:%H:%M:%S.%f} - Green detected!'.format(datetime.datetime.now()))
            cv2.putText(_self.image_original, '{:%H:%M:%S.%f} - Green detected!'.format(datetime.datetime.now()),
                        (_self.textspace, _self.textspace), font, 0.7,
                        _self.color_green, 1, cv2.LINE_AA)
            if _self.output_green:
                if _self.output_bgwhite:
                    _self.green_image_bgr[np.where((_self.green_image_bgr == [0, 0, 0]).all(axis=2))] = [255, 255, 255]
                cv2.imwrite("green.png", _self.green_image_bgr)
        # Default: Red detected
        else:
            _self.LOG.info('{:%H:%M:%S.%f} - Red detected!'.format(datetime.datetime.now()))
            cv2.putText(_self.image_original, '{:%H:%M:%S.%f} - Red detected!'.format(datetime.datetime.now()),
                        (_self.textspace, _self.textspace), font, 0.7,
                        _self.color_green, 1, cv2.LINE_AA)
