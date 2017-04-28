# ================================================================================
# !/usr/bin/python
# TITLE           : imageconverter.py
# DESCRIPTION     : supportive classes for image conversions
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 25.10.2016
# USAGE           : .
# VERSION         : 0.9
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

# import the necessary packages
import logging
from logging.config import fileConfig

import cv2
import numpy as np
from common.config import confighandler as cfg
from skimage.morphology import skeletonize


class ImageConverter(object):
    # Configure logging component
    fileConfig(cfg.get_logging_config_fullpath())
    __log = logging.getLogger()
    __log.setLevel(cfg.get_settings_loglevel())

    # Letter values
    lower_red_full = np.array(cfg.get_maskletter_red_low_full_splited())
    upper_red_full = np.array(cfg.get_maskletter_red_high_full_splited())

    # Trafficlight values
    lower_green_traffic = np.array(cfg.get_masktrafficlight_green_l_splited())
    upper_green_traffic = np.array(cfg.get_masktrafficlight_green_h_splited())
    lower_red_full_traffic = np.array(cfg.get_masktrafficlight_red_low_full_splited())
    upper_red_full_traffic = np.array(cfg.get_masktrafficlight_red_high_full_splited())

    color_black_low = np.array(cfg.get_color_black_low_splited())
    color_black_high = np.array(cfg.get_color_black_high_splited())

    kernel_size = cfg.get_filter_kernel_size()

    @staticmethod
    def convertbgr2gray(image):
        """
        Converts an BGR-Image to grayscale
        :param image: image with bgr color scheme
        :return: grayscaled image
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def convertbgr2hsv(image):
        """
        Converts an BGR-Image to HSV color space (standard)
        :param image: image with bgr color scheme
        :return: image in HSV color space
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    @staticmethod
    def convertbgr2hsvfull(image):
        """
        Converts an BGR-Image to HSV color space (Fullrange)
        :param image: image with bgr color scheme
        :return: image in HSV color space
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)

    @staticmethod
    def convertgray2bgr(image):
        """
        Converts a grayscaled image to BGR color scheme
        :param image: grayscaled image (1-channel)
        :return: image in BGR color scheme (3-channel)
        """
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def converthsv2bgr(image):
        """
        Converts a HSV-Image to BGR color space
        :param image: image in HSV color space
        :return: image in BGR color scheme
        """
        return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

    @staticmethod
    def converthsvfull2bgr(image):
        return cv2.cvtColor(image, cv2.COLOR_HSV2BGR_FULL)

    @staticmethod
    def convert2blackwhite(image):
        """
        Converts any image to black&white
        :param image: image to be converted to black&white
        :return: black&white image (pixelvalues: 0 = black, 1 = white)
        """
        mask = cv2.inRange(image, ImageConverter.color_black_low,
                           ImageConverter.color_black_high)  # create overlay mask for all none matching bits to zero
        output_img = cv2.bitwise_and(image, image, mask=mask)  # apply mask on image
        img_gray = ImageConverter.convertbgr2gray(output_img)  # convert image to grayscale
        img_gray[img_gray > 0] = 1  # set all non black pixels to white for BW-image
        return img_gray

    @staticmethod
    def mask_color_red_fullhsv(img):
        """
        This function extracts only red color parts of the provided image with Full-HSV color space
        :param img: image to extract red color parts
        :return: image (mask) with only red color parts, all other pixels are black (zero)
        """
        img_hsv = ImageConverter.convertbgr2hsvfull(img)  # convert image to HSV

        mask = cv2.inRange(img_hsv, ImageConverter.lower_red_full,
                           ImageConverter.upper_red_full)  # create overlay mask for all none matching bits to zero (black)
        output_img = cv2.bitwise_and(img, img, mask=mask)  # apply mask on image

        return output_img

    @staticmethod
    def mask_color_red_fullhsv_traffic(img):
        """
        This function extracts only red color parts of the provided image with Full-HSV color space
        :param img: image to extract red color parts
        :return: image (mask) with only red color parts, all other pixels are black (zero)
        """
        img_hsv = ImageConverter.convertbgr2hsvfull(img)  # convert image to HSV

        mask = cv2.inRange(img_hsv, ImageConverter.lower_red_full_traffic,
                           ImageConverter.upper_red_full_traffic)  # create overlay mask for all none matching bits to zero (black)
        output_img = cv2.bitwise_and(img, img, mask=mask)  # apply mask on image

        return output_img

    @staticmethod
    def mask_color_green_traffic(img):
        """
        This function extracts only green color parts of the provided image
        :param img: image to extract green color parts
        :return: image (mask) with only green color parts, all other pixels are black (zero)
        """
        img_hsv = ImageConverter.convertbgr2hsv(img)  # convert image to HSV

        mask = cv2.inRange(img_hsv, ImageConverter.lower_green_traffic,
                           ImageConverter.upper_green_traffic)  # create overlay mask for all none matching bits to zero (black)
        # mask = cv2.inRange(img_hsv, np.array(cfg.get_masktrafficlight_green_l_splited()), np.array(cfg.get_masktrafficlight_green_h_splited()))
        output_img = cv2.bitwise_and(img, img, mask=mask)  # apply mask on image

        return output_img

    @staticmethod
    def remove_erosions(img):
        """
        Removes erosions on an image with dilation method
        :param img: image to remove erosions
        :return: image with removed erosions
        """
        kernel = np.ones((ImageConverter.kernel_size, ImageConverter.kernel_size), np.uint8)
        return cv2.dilate(img, kernel, iterations=1)

    @staticmethod
    def transform_perspectiveview2topdownview(img, edges):
        """
        This function transforms a perspective image to a the "birds eye view"
        :param img: source image to transform
        :param edges: 4 points (edges) on the image to stretch the image
        :return: image in "birds eye view"
        """
        pts = np.array(edges, np.float32)
        (tl, tr, br, bl) = pts

        # compute the width of the new image, which will be the maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        max_width = max(int(width_a), int(width_b))

        # compute the height of the new image, which will be the maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_height = max(int(height_a), int(height_b))

        # now that we have the dimensions of the new image, construct the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points in the top-left, top-right, bottom-right, and bottom-left order
        dst = np.array([[0, 0], [max_width - 1, 0], [max_width - 1, max_height - 1], [0, max_height - 1]],
                       dtype="float32")

        # compute the perspective transform matrix and then apply it
        trans_matrix = cv2.getPerspectiveTransform(pts, dst)
        img_transformed = cv2.warpPerspective(img, trans_matrix, (max_width, max_height))
        return img_transformed

    @staticmethod
    def minimize_roi_lettercontour(roi):
        """
        Minimize image region by cropping image around black letters
        :param roi: original image to crop
        :return: cropped original image
        """
        img_bw = ImageConverter.convert2blackwhite(roi)
        img_bw[img_bw > 0] = 255

        # remove border erosion
        img_height, img_width = img_bw.shape
        img_bw_unbordered = img_bw[2:img_height - 4, 2:img_width - 4]

        # get rectangle around letter and crop original image
        pos_x, pos_y, width, height = cv2.boundingRect(img_bw_unbordered)
        img_cropped = roi[pos_y:pos_y + height, pos_x:pos_x + width]

        # resize to original size
        if 0 < img_cropped.shape[1] < 150:
            r = 150 / img_cropped.shape[1]
            dim = (150, int(img_cropped.shape[0] * r))
            img_cropped = cv2.resize(img_cropped, dim, interpolation=cv2.INTER_AREA)
        return img_cropped

    @staticmethod
    def thinningblackwhiteimage(image):
        """
        Applies thinning algorithm to an black&white image
        :param image: black&white image
        :return:
        """
        edges = skeletonize(image)
        edges = edges * 1  # convert float values to integer (do not optimize!)
        edges[edges == 1] = 255  # change white value from 1 to 255
        edges = np.uint8(edges)  # flatten values
        return edges
