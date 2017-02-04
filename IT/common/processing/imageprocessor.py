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
import logging
import common.config.confighandler as cfg
import math
import logging.config
from common.logging.fpshelper import FPSHelper
from skimage.morphology import skeletonize
from collections import Counter


class ImageConverter(object):
    logging.config.fileConfig(cfg.get_logging_config_fullpath())
    __log = logging.getLogger()
    __log.setLevel(cfg.get_settings_loglevel())

    @staticmethod
    def convertbgr2gray(image):
        return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    @staticmethod
    def convertbgr2hsv(image):
        return cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    @staticmethod
    def convertbgr2hsvfull(image):
        return cv2.cvtColor(image,cv2.COLOR_BGR2HSV_FULL)

    @staticmethod
    def convertgray2bgr(image):
        return cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)

    @staticmethod
    def converthsv2bgr(image):
        return cv2.cvtColor(image,cv2.COLOR_HSV2BGR)

    @staticmethod
    def convert2blackwhite(image):
        lower_black = np.array(cfg.get_color_black_low_splited())
        upper_black = np.array(cfg.get_color_black_high_splited())

        mask = cv2.inRange(image, lower_black, upper_black)     # create overlay mask for all none matching bits to zero
        output_img = cv2.bitwise_and(image, image, mask=mask)    # apply mask on image
        img_gray = ImageConverter.convertbgr2gray(output_img)   # convert image to grayscale
        img_gray[img_gray > 0] = 1                              # set all non black pixels to white for BW-image

        return img_gray

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

        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(pts, dst)
        img2 = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
        return img2

    @staticmethod
    def thinningblackwhiteimage(image):
        edges = skeletonize(image)
        edges = edges * 1
        edges[edges == 1] = 255
        edges = np.uint8(edges)
        return edges

    @staticmethod
    def mask_color_red(img):
        fps = FPSHelper()
        """
        This function extracts only red color parts of the provided image with Hue-Range shifted
        :param img: image to extract red color parts
        :return: image (mask) with only red color parts, all other pixels are black (zero)
        """
        # convert image to HSV
        fps.start()
        img_hsv = ImageConverter.convertbgr2hsv(img)
        fps.stop()
        ImageConverter.__log.debug("processing time hsv: " + str(fps.elapsedtime_ms()) + " ms")

        # shift Hue Channel to remove issue on transition from value 180 to 0
        fps.start()
        img_hsv[..., 0] = (img_hsv[..., 0] + cfg.get_filter_hsv_shift()) % 180
        fps.stop()
        ImageConverter.__log.debug("processing time shift: " + str(fps.elapsedtime_ms()) + " ms")

        lower_red = np.array(cfg.get_maskletter_red_shift_l_splited())
        upper_red = np.array(cfg.get_maskletter_red_shift_h_splited())

        # create overlay mask for all none matching bits to zero (black)
        fps.start()
        mask = cv2.inRange(img_hsv, lower_red, upper_red)
        fps.stop()
        ImageConverter.__log.debug("processing time inRange: " + str(fps.elapsedtime_ms()) + " ms")

        # apply mask on image
        fps.start()
        output_img = cv2.bitwise_and(img, img, mask=mask)
        fps.stop()
        ImageConverter.__log.debug("processing time masking: " + str(fps.elapsedtime_ms()) + " ms")

        return output_img

    @staticmethod
    def mask_color_red_fullhsv(img):
        fps = FPSHelper()
        """
        This function extracts only red color parts of the provided image with Hue-Range shifted
        :param img: image to extract red color parts
        :return: image (mask) with only red color parts, all other pixels are black (zero)
        """
        # convert image to HSV
        fps.start()
        img_hsv = ImageConverter.convertbgr2hsvfull(img)
        fps.stop()
        ImageConverter.__log.info("processing time hsv: " + str(fps.elapsedtime_ms()) + " ms")

        lower_red = np.array(cfg.get_maskletter_red_low_full_splited())
        upper_red = np.array(cfg.get_maskletter_red_high_full_splited())

        # create overlay mask for all none matching bits to zero (black)
        fps.start()
        mask = cv2.inRange(img_hsv, lower_red, upper_red)
        fps.stop()
        ImageConverter.__log.info("processing time inRange: " + str(fps.elapsedtime_ms()) + " ms")

        # apply mask on image
        fps.start()
        output_img = cv2.bitwise_and(img, img, mask=mask)
        fps.stop()
        ImageConverter.__log.info("processing time masking: " + str(fps.elapsedtime_ms()) + " ms")

        return output_img

    @staticmethod
    def remove_erosions(img):
        kernel_size = cfg.get_filter_kernel_size()
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.dilate(img, kernel, iterations=1)


class ImageAnalysis(object):
    logging.config.fileConfig(cfg.get_logging_config_fullpath())
    __log = logging.getLogger()
    __log.setLevel(cfg.get_settings_loglevel())

    @staticmethod
    def reorder_edgepoints_clockwise(pts):
        """
        This function reorders the provided points in the following order:
        1. top-left     2. top-right    3. bottom-right     4. bottom-left
        :param pts: unordered list of four points / coordinates
        :return: ordered coordinates
        """

        # initialize a list of coordinates that will be ordered
        rect = np.zeros((4, 2), dtype="float32")

        # the top-left point will have the smallest sum, whereas the bottom-right point will have the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # compute the difference between the points, the top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    @staticmethod
    def get_ordered_corners(mask):
        """
        This function detects edges of the two biggest areas on a provided image (mask)
        :param mask: image / mask wo apply edge detection (e.g. only red colored parts)
        :return: reordered edges/corners (top left, top right, bottom right, bottom left)
        """

        img_gray = ImageConverter.convertbgr2gray(mask)         # set image to grayscale
        img_gray[img_gray > 0] = 255                            # set all non black pixels to white for BW-image
        img_dilated = ImageConverter.remove_erosions(img_gray)  # dilated image for remove of small erosions

        # find all contours and
        (_, cnts, _) = cv2.findContours(img_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # resort contours based on their area from highest to lowest and get only the two greatest
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:2]

        # all edges (top left, bottom left, top right, bottom right)
        edges = []
        i = False
        for c in cnts:

            # TODO: based on angle the solution can be made more robust as the angles need to be approx the same...
            # cv2.drawContours(img, [c], -1, (0, 255, 0), 1)
            # elipse = cv2.fitEllipse(c)
            # print("\nWinkel: " + str(elipse[2]))

            # TODO: risk of cut red line, need to guarantee that both red blocks are fully visible
            # e.g. ignore red color on image boarder

            rect = cv2.minAreaRect(c)       # get minimal area rectangle
            box = cv2.boxPoints(rect)       # represent area as points
            box = np.int0(np.around(box))   # round values and normalize array

            box = ImageAnalysis.reorder_edgepoints_clockwise(box)
            if not i:
                pt_top = tuple(np.int0(box[1]))         # top right position
                pt_bottom = tuple(np.int0(box[2]))      # bottom right position
            else:
                pt_top = tuple(np.int0(box[0]))         # top left position
                pt_bottom = tuple(np.int0(box[3]))      # bottom right position
            dist = math.sqrt((abs(pt_top[0] - pt_bottom[0])) ** 2 + (abs(pt_top[1] - pt_bottom[1])) ** 2)
            if(dist > 80):
                edges.append(pt_top)
                edges.append(pt_bottom)
            i = True

        if len(edges) == 4:
            # reorder edges to (top left, top right, bottom right, bottom left)
            edges = [edges[i] for i in [0, 2, 3, 1]]
            ImageAnalysis.__log.debug("edges: " + str(edges))
            return edges
        else:
            # not 4 edges found
            # TODO: Error handling, e.g. take next image or so
            return 0

    @staticmethod
    def get_ordered_corners_drawed(mask, img):
        """
        This function detects edges of the two biggest areas on a provided image (mask)
        :param mask: image / mask wo apply edge detection (e.g. only red colored parts)
        :param img: original image which will be used for drawing lines on it
        :return: reordered edges/corners (top left, top right, bottom right, bottom left)
        """

        img_gray = ImageConverter.convertbgr2gray(mask)         # set image to grayscale
        img_gray[img_gray > 0] = 255                            # set all non black pixels to white for BW-image
        img_dilated = ImageConverter.remove_erosions(img_gray)  # dilated image for remove of small erosions

        # find all contours and
        (_, cnts, _) = cv2.findContours(img_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # resort contours based on their area from highest to lowest and get only the two greatest
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:2]

        # all edges (top left, bottom left, top right, bottom right)
        edges = []
        i = False
        for c in cnts:

            # TODO: based on angle the solution can be made more robust as the angles need to be approx the same...
            # cv2.drawContours(img, [c], -1, (0, 255, 0), 1)
            # elipse = cv2.fitEllipse(c)
            # print("\nWinkel: " + str(elipse[2]))

            # TODO: risk of cut red line, need to guarantee that both red blocks are fully visible
            # e.g. ignore red color on image boarder

            rect = cv2.minAreaRect(c)       # get minimal area rectangle
            box = cv2.boxPoints(rect)       # represent area as points
            box = np.int0(np.around(box))  # round values and normalize array

            cv2.drawContours(img, [box], 0, (0, 255, 255), 1)
            box = ImageAnalysis.reorder_edgepoints_clockwise(box)
            if not i:
                pt_top = tuple(np.int0(box[1]))     # top right position
                pt_bottom = tuple(np.int0(box[2]))  # bottom right position
            else:
                pt_top = tuple(np.int0(box[0]))     # top left position
                pt_bottom = tuple(np.int0(box[3]))  # bottom right position

            dist = math.sqrt((abs(pt_top[0] - pt_bottom[0])) ** 2 + (abs(pt_top[1] - pt_bottom[1])) ** 2)
            if(dist > 80):
                edges.append(pt_top)
                edges.append(pt_bottom)
                cv2.line(img, pt_top, pt_bottom, (0, 0, 255), 1)
                cv2.circle(img, pt_top, 2, (0, 255, 0), -1)
                cv2.circle(img, pt_bottom, 2, (0, 255, 0), -1)
            i = True

        if len(edges) == 4:
            # reorder edges to (top left, top right, bottom right, bottom left)
            edges = [edges[i] for i in [0, 2, 3, 1]]
            ImageAnalysis.__log.debug("edges: " + str(edges))
            return img, edges
        else:
            # not 4 edges found
            # TODO: Error handling, e.g. take next image or so
            return img, 0

    @staticmethod
    def get_roman_letter_drawed(roi):
        """
        This function determines the number of a roman letter (only I, II, III, IV, V)
        :param roi: cropped image with only the letters on it
        :return: image with all detected lines for the number
        """
        FPS = FPSHelper()
        number = 0
        img_bw = ImageConverter.convert2blackwhite(roi)

        # edge detection
        FPS.start()
        edges = ImageConverter.thinningblackwhiteimage(img_bw)
        img_gray_mark = ImageConverter.convertgray2bgr(edges)

        lines = cv2.HoughLines(edges, 1, np.pi / 180, 15, np.array([]), 0, 0)
        FPS.stop()
        ImageAnalysis.__log.debug("processing time HoughLines: " + str(FPS.elapsedtime_ms()) + " ms")

        # if lines found, enumerate number based on its angle
        if lines is not None:
            line, _, _ = lines.shape
            v_left_found = False
            v_right_found = False
            all_i = []  # = [[] for i in range(3)]

            for i in range(line):

                rho = lines[i][0][0]  # vector distance to line
                theta = lines[i][0][1]  # angle of line in radian

                a, b = np.cos(theta), np.sin(theta)
                x0, y0 = a * rho, b * rho
                deg = theta * 180 / np.pi  # radian to degree

                line_pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
                line_pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))

                ImageAnalysis.__log.debug("-----\nlinept1: " + str(line_pt1)+ "\nlinept2: " + str(line_pt2) + "\ndeg:" + str(deg))

                # detect an I
                if (0.0 < deg < 1.0) or (178.0 < deg < 180.0):
                    ImageAnalysis.__log.debug("I - line found with deg: " + str(deg))

                    # get median x-value of both points
                    x = (int(x0 + 1000 * (-b)) + int(x0 - 1000 * (-b))) / 2
                    all_i.append([x, line_pt1, line_pt2])
                    cv2.line(img_gray_mark, line_pt1, line_pt2, (255, 255, 0), 1, cv2.LINE_AA)

                    ImageAnalysis.__log.debug("pos line_pt1: " + str(line_pt1) + " vertical line found with deg: " + str(deg) + ", theta: " + str(theta))
                    continue

                # right hand side of V
                elif 10.0 < deg < 20.0:
                    ImageAnalysis.__log.debug("V / - line found with deg: " + str(deg))
                    cv2.line(img_gray_mark, line_pt1, line_pt2, (0, 0, 255), 1, cv2.LINE_AA)
                    v_right_found = True
                    continue

                # left hand side of V
                elif 150.0 < deg < 170.0:
                    ImageAnalysis.__log.debug("V \ - line found with deg: " + str(deg))
                    cv2.line(img_gray_mark, line_pt1, line_pt2, (0, 255, 0), 1, cv2.LINE_AA)
                    v_left_found = True
                    continue
                else:
                    ImageAnalysis.__log.debug("line with deg: " + str(deg) + "out of allowed range")

            # eliminate redundant detected I
            i_count = ImageAnalysis.__eliminate_redundant_I(all_i)

            # enumerate the number based on detected lines
            number = ImageAnalysis.__enumerate_number_withlines(v_left_found, v_right_found, i_count)

        else:
            ImageAnalysis.__log.warning("no lines detected on image")
        ImageAnalysis.__log.debug("--")

        return img_gray_mark

    @staticmethod
    def get_roman_letter(roi):
        """
        This function determines the number of a roman letter (only I, II, III, IV, V)
        :param roi: cropped image with only the letters on it
        :return: detect number as integer
        """
        FPS = FPSHelper()
        number = 0
        img_bw = ImageConverter.convert2blackwhite(roi)

        # edge detection
        FPS.start()
        edges = ImageConverter.thinningblackwhiteimage(img_bw)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 15, np.array([]), 0, 0)
        FPS.stop()
        ImageAnalysis.__log.debug("processing time HoughLines: " + str(FPS.elapsedtime_ms()) + " ms")

        # if lines found, enumerate number based on its angle
        if lines is not None:
            line, _, _ = lines.shape
            v_left_found = False
            v_right_found = False
            all_i = []  # = [[] for i in range(3)]

            for i in range(line):

                rho = lines[i][0][0]  # vector distance to line
                theta = lines[i][0][1]  # angle of line in radian

                a, b = np.cos(theta), np.sin(theta)
                x0, y0 = a * rho, b * rho
                deg = theta * 180 / np.pi  # radian to degree

                line_pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
                line_pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))

                #ImageAnalysis.__log.debug("-----\tlinept1: " + str(line_pt1) + "\tlinept2: " + str(line_pt2) + "\tdeg:" + str(deg))

                # detect an I
                if (0.0 < deg < 1.0) or (178.0 < deg < 180.0):
                    ImageAnalysis.__log.debug("I - line found with deg: " + str(deg))

                    # get median x-value of both points
                    x = (int(x0 + 1000 * (-b)) + int(x0 - 1000 * (-b))) / 2
                    all_i.append([x, line_pt1, line_pt2])

                    #ImageAnalysis.__log.debug("pos line_pt1: " + str(line_pt1) + " vertical line found with deg: " + str(deg) + ", theta: " + str(theta))
                    continue

                # right hand side of V
                elif 10.0 < deg < 20.0:
                    ImageAnalysis.__log.debug("V / - line found with deg: " + str(deg))
                    v_right_found = True
                    continue

                # left hand side of V
                elif 150.0 < deg < 170.0:
                    ImageAnalysis.__log.debug("V \ - line found with deg: " + str(deg))
                    v_left_found = True
                    continue
                else:
                    ImageAnalysis.__log.debug("line with deg: " + str(deg) + "out of allowed range")

            # eliminate redundant detected I
            i_count = ImageAnalysis.__eliminate_redundant_I(all_i)

            # enumerate the number based on detected lines
            number = ImageAnalysis.__enumerate_number_withlines(v_left_found, v_right_found, i_count)

        else:
            ImageAnalysis.__log.warning("no lines detected on image")
        ImageAnalysis.__log.debug("--")

        return number

    @staticmethod
    def __enumerate_number_withlines(v_left, v_right, i):
        # enumerate the number based on detected lines
        if v_left and v_right:
            n = 5
            if i == 1:
                n = 4
            ImageAnalysis.__log.info("detected number: " + str(n))
            return n
        elif (i is not None) and (0 < i < 4):
            ImageAnalysis.__log.info("detected number: " + str(i))
            return i
        else:
            ImageAnalysis.__log.error("not able to enumerate number!!")
            # TODO: Error handling if number not detected e.g. other algorithm to detect number
            return 0

    @staticmethod
    def __eliminate_redundant_I(all_detected_I):
        # eliminate redundant detected I
        if len(all_detected_I) != 0:
            all_detected_I.sort()
            tolerance = cfg.get_letter_tolerance_i_gap()
            nondup_i = [all_detected_I.pop(0), ]
            all_i_count = 0

            for x in all_detected_I[1::1]:
                xcor = x[0]
                pt1 = x[1]
                pt2 = x[2]
                # Skip items within tolerance.
                if abs(nondup_i[all_i_count][0] - xcor) <= tolerance:
                    continue
                nondup_i.append([xcor, pt1, pt2])
                all_i_count += 1
            i_count = len(nondup_i)
            ImageAnalysis.__log.debug("all I: " + str(all_detected_I))
            ImageAnalysis.__log.debug("all nondup I: " + str(nondup_i) + "icount: " + str(i_count))
            return i_count

    @staticmethod
    def most_voted_number(allnumbers):
        count = Counter(allnumbers)
        mostvotednumber = count.most_common(1)[0][0]
        ImageAnalysis.__log.info("Most voted number is: " + str(mostvotednumber))
        return mostvotednumber

