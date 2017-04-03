# =======================================================================
# title           :trafficlightdetectionhandler.py
# description     :This program holds the main logic for the TrafficLightDetection
# author          :Fabrizio Rohrbach, Marco Moro
# date            :03.02.2017
# version         :0.3
# usage           :python trafficlightdetectionhandler.py
# notes           :
# python_version  :3.5.2
# opencv_version  :3.1.0
# =======================================================================

# Import the modules needed to run the script.
import numpy as np
import cv2
import datetime
import logging
import common.config.confighandler as cfg

from logging.config import fileConfig
from common.logging.fpshelper import FPSHelper
from common.processing.imageconverter import ImageConverter


class TrafficLightDetection(object):

    # Load needed settings from Config.ini into variables (so you dont have to access the ini file each time)
    output_red = cfg.get_debug_output_red()  # write image with red pixels to disk after apply red color mask if True
    output_green = cfg.get_debug_output_green()  # write image with green pixels to disk after apply green color mask if True
    output_bgwhite = cfg.get_debug_output_bgwhite()  # set background color of output images to white instead of black if True
    debug = cfg.get_settings_debug()  # print debug informations if True
    cropheight = cfg.get_cropimage_height()  # height of the cropped image after first red pixel is found
    cropwidth = cfg.get_cropimage_width()  # width of the cropped image after first red pixel is found
    camera_width = cfg.get_camera_width()  # width of the captured image
    camera_height = cfg.get_camera_height()  # height of the captured image
    color_green = (0, 255, 0) # cfg.get_color_green()  # rgb values for green -> used for writing on image
    bordersize_left = cfg.get_imagetext_bordersize_left()  # position left of text on the image
    bordersize_top = cfg.get_imagetext_bordersize_top()  # position top of text on the image
    bordersize_bottom = cfg.get_imagetext_bordersize_bottom()  # position bottom of text on the image
    bordersize_right = cfg.get_imagetext_bordersize_right()  # position right of text on the image
    textspace = cfg.get_imagetext_textspace()  # space between text lines on image

    # Load Masks from Config.ini
    lower_red0 = cfg.get_masktrafficlight_red_low_l_splited()
    upper_red0 = cfg.get_masktrafficlight_red_low_h_splited()
    lower_red1 = cfg.get_masktrafficlight_red_high_l_splited()
    upper_red1 = cfg.get_masktrafficlight_red_high_h_splited()
    lower_green = cfg.get_masktrafficlight_green_l_splited()
    upper_green = cfg.get_masktrafficlight_green_h_splited()

    # Initialize the class
    def __init__(self):
        self.redpixelx = 0
        self.redpixely = 0
        self.redfound = False
        self.croppointx = 0
        self.croppointy = 0
        self.cropnewpointy = 0
        self.frame = 0
        self.image_original = 0
        self.green_image_bgr = 0
        self.red_image_bgr = 0
        self.maxLoc = 0
        self.green_color = 0
        self.red_color = 0
        self.greenpixel_count = 0
        self.redpixel_count = 0
        self.green_hit_counter = 0
        self.FPS = None
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()
        self.__log.setLevel(cfg.get_settings_loglevel())

    # Main logic for TrafficLightDetection
    def detect_trafficlight(self, frame):
        self.FPS = FPSHelper()
        self.frame = frame
        self.image_original = frame.copy()
        self.crop_image()
        self.get_brightest_redpixel()
        self.get_brightest_greenpixel()
        self.detect_brighter_color()

        return self.image_original

    # Crop the image
    def crop_image(self):
        # Crop the image after first red pixel in range found
        if self.redfound and self.redpixelx != 0 and self.redpixely != 0:
            self.croppointx = self.redpixelx - 25
            self.croppointy = self.redpixely - 25
            cropnewpointx = self.croppointx + self.cropwidth + 25
            cropnewpointy = self.croppointy + self.cropheight + 25
            self.__log.debug("Croppoint %d|%d Croppoint2 %d|%d" % (self.croppointx, self.croppointy, cropnewpointx, cropnewpointy))
            crop_img = self.frame[self.croppointy:cropnewpointy, self.croppointx:cropnewpointx]
            cv2.rectangle(self.image_original, (self.croppointx, self.croppointy), (cropnewpointx, cropnewpointy), (0, 0, 255), 2)
            self.frame = crop_img

    # Get the brightest red pixel on frame
    def get_brightest_redpixel(self):
        # --- Get red pixels ---
        red_image = self.frame
        red_image_output = ImageConverter.mask_color_red_traffic(red_image)
        self.red_image_bgr = ImageConverter.converthsv2bgr(red_image_output)

        # --- Count the red pixels ---
        red_image_gray = ImageConverter.convertbgr2gray(self.red_image_bgr)
        self.redpixel_count = cv2.countNonZero(red_image_gray)

        # Check if any red pixels are left after apply red color mask
        if self.redpixel_count > 0:
            # --- Find brightest spot ---
            # perform a naive attempt to find the (x, y) coordinates of the area of the image with the largest intensity value
            (minVal, maxVal, minLoc, self.maxLoc) = cv2.minMaxLoc(red_image_gray)  # get position of pixel with max grey value

            # Draw a circle around the detected red pixel
            if self.redfound and self.redpixelx != 0 and self.redpixely != 0:  # if first red pixel is found, draw on cropped image
                cv2.circle(self.image_original, (self.croppointx + self.maxLoc[0], self.croppointy + self.maxLoc[1]), 5, (0, 0, 255), 2)
            else:
                cv2.circle(self.image_original, self.maxLoc, 5, (0, 0, 255), 2)  # draw on original image
                self.red_color = np.uint8([[red_image_gray[self.maxLoc[1], self.maxLoc[0]]]])  # get value of brightest gray pixel
        else:  # if no red pixels are left after apply red color mask, set value to 0
            self.red_color = 0

    # Get the brightest green pixel on frame
    def get_brightest_greenpixel(self):
        # --- Get green pixels ---
        green_image = self.frame
        green_image_output = ImageConverter.mask_color_green(green_image)
        self.green_image_bgr = ImageConverter.converthsv2bgr(green_image_output)

        # --- Count the green pixels ---
        green_image_gray = ImageConverter.convertbgr2gray(self.green_image_bgr)
        self.greenpixel_count = cv2.countNonZero(green_image_gray)

        if self.greenpixel_count > 0:
            # --- Find brightest spot ---
            # perform a naive attempt to find the (x, y) coordinates of the area of the image with the largest intensity value
            (minVal, maxVal, minLoc, self.maxLoc) = cv2.minMaxLoc(green_image_gray)  # get position of pixel with max grey value

            # Draw a circle around the detected green pixel
            if self.redfound and self.redpixelx != 0 and self.redpixely != 0:  # if first red pixel is found, draw on cropped image
                cv2.circle(self.image_original, (self.croppointx + self.maxLoc[0], self.croppointy + self.maxLoc[1]), 5, (0, 255, 0), 2)
            else:
                cv2.circle(self.image_original, self.maxLoc, 5, (0, 255, 0), 2)  # draw on original image
                self.green_color = np.uint8([[green_image_gray[self.maxLoc[1], self.maxLoc[0]]]])  # get value of brightest gray pixel
        else:  # if no green pixels are left after apply green color mask, set value to 0
            self.green_color = 0

    # Find out which pixel is brighter (red or green)
    def detect_brighter_color(self):
        font = cfg.get_opencv_font()

        # Add border to frame
        self.image_original = cv2.copyMakeBorder(self.image_original, self.bordersize_top, self.bordersize_bottom, self.bordersize_left, self.bordersize_right, cv2.BORDER_CONSTANT, 0)

        # Debug
        if self.debug:
            # Debug green and red pixel count
            self.__log.debug("red count: " + str(self.redpixel_count) + " | green count: " + str(self.greenpixel_count))
            cv2.putText(self.image_original, "red count: " + str(self.redpixel_count) + " | green count: " + str(self.greenpixel_count), (self.textspace, (2 * self.textspace)), font, 0.7, self.color_green, 1, cv2.LINE_AA)
            # Debug grey pixel values (of original green and red pixel)
            self.__log.debug("red color: " + str(self.red_color) + " | green color: " + str(self.green_color))
            cv2.putText(self.image_original, "red color: " + str(self.red_color) + " | green color: " + str(self.green_color), (self.textspace, (3 * self.textspace)), font, 0.7, self.color_green, 1, cv2.LINE_AA)
        # Red detected
        if self.red_color > self.green_color:
            if not self.redfound:
                self.redfound = True
                self.redpixelx = self.maxLoc[0]
                self.redpixely = self.maxLoc[1]
                self.__log.info('Red detected!')
            cv2.putText(self.image_original, '{:%H:%M:%S.%f} - Red detected!'.format(datetime.datetime.now()), (self.textspace, self.textspace), font, 0.7, self.color_green, 1, cv2.LINE_AA)
            if self.output_red:
                if self.output_bgwhite:
                    self.red_image_bgr[np.where((self.red_image_bgr == [0, 0, 0]).all(axis=2))] = [255, 255, 255]
                cv2.imwrite("red.png", self.red_image_bgr)
        # Green detected
        elif self.red_color < self.green_color:
            self.__log.info('Green detected!')
            self.green_hit_counter += 1
            cv2.putText(self.image_original, '{:%H:%M:%S.%f} - Green detected!'.format(datetime.datetime.now()), (self.textspace, self.textspace), font, 0.7, self.color_green, 1, cv2.LINE_AA)
            if self.output_green:
                if self.output_bgwhite:
                    self.green_image_bgr[np.where((self.green_image_bgr == [0, 0, 0]).all(axis=2))] = [255, 255, 255]
                cv2.imwrite("green.png", self.green_image_bgr)
        # Default: Red detected
        else:
            self.__log.info('Red detected!')
            cv2.putText(self.image_original, '{:%H:%M:%S.%f} - Red detected!'.format(datetime.datetime.now()), (self.textspace, self.textspace), font, 0.7, self.color_green, 1, cv2.LINE_AA)

    def get_color_state(self):
        if self.green_hit_counter < 10:
            return "red"
        else:
            return "green"
