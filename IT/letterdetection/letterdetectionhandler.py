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
import numpy as np
import time
import configparser
import os
import sys

from picamera.array import PiRGBArray
from picamera import PiCamera
from ..common.logging.fpshelper import FPSHelper
from ..common.logging.loghelper import LogHelper
from skimage.morphology import skeletonize


class LetterDetectionHandler(object):
    def str2bool(v):
        return v.lower() in ("yes", "Yes", "YES", "true", "True", "TRUE", "1", "t")

    LOG = LogHelper()
    FPS = FPSHelper()

    ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)

    config = configparser.ConfigParser()
    config.read('/home/pi/Desktop/PREN/common/config/config.ini')

    red_low_full = np.array([int(c) for c in config['mask_letter']['red_low_full'].split(',')])
    red_high_full = np.array([int(c) for c in config['mask_letter']['red_high_full'].split(',')])
    red_shift_l = np.array([int(c) for c in config['mask_letter']['red_shift_l'].split(',')])
    red_shift_h = np.array([int(c) for c in config['mask_letter']['red_shift_h'].split(',')])
    black_low = np.array([int(c) for c in config['color']['black_low'].split(',')])
    black_high = np.array([int(c) for c in config['color']['black_high'].split(',')])
    kernel_size = int(config['filter']['kernel_size'])
    hsv_shift = int(config['filter']['hsv_shift'])
    color_yellow = np.array([int(c) for c in config['color']['yellow'].split(',')])
    color_red = np.array([int(c) for c in config['color']['red'].split(',')])
    color_green = np.array([int(c) for c in config['color']['green'].split(',')])
    camera_width = int(config['camera']['width'])
    camera_height = int(config['camera']['height'])
    camera_framerate = int(config['camera']['framerate'])
    camera_iso = int(config['camera']['iso'])
    camera_awb = config['camera']['awb']
    tolerance_I_gap = int(config['letter']['tolerance_I_gap'])

    def imgcoloredmask_red_full(_self, img):
        """
        DEPRECATED: This function extracts only red color parts of the provided image with Full HSV-Range
        :param img: image to extract red color parts
        :return: image with only red color parts, all other pixels are black (zero)
        """
        img = cv2.GaussianBlur(img, (7, 7), 0)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)

        # lower mask (0-10)
        lower_red = np.array(_self.red_low_full)
        upper_red = np.array(_self.red_high_full)
        mask = cv2.inRange(img_hsv, lower_red, upper_red)

        # set output img to zero everywhere except my mask
        output_img = img.copy()
        output_img[np.where(mask == 0)] = 0
        return output_img

    def imgcoloredmask_red_shifted(_self, img):
        """
        This function extracts only red color parts of the provided image with Hue-Range shifted
        :param img: image to extract red color parts
        :return: image (mask) with only red color parts, all other pixels are black (zero)
        """
        # convert image to HSV
        _self.FPS.start()
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        _self.FPS.stop()
        _self.LOG.debug("processing time hsv: " + str(_self.FPS.elapsedtime_ms()) + " ms")

        # shift Hue Channel to remove issue on transition from value 180 to 0
        _self.FPS.start()
        shiftVal = _self.hsv_shift
        img_hsv[..., 0] = (img_hsv[..., 0] + shiftVal) % 180
        _self.FPS.stop()
        _self.LOG.debug("processing time shift: " + str(_self.FPS.elapsedtime_ms()) + " ms")

        lower_red = np.array(_self.red_shift_l)
        upper_red = np.array(_self.red_shift_h)

        # create overlay mask for all none matching bits to zero (black)
        _self.FPS.start()
        mask = cv2.inRange(img_hsv, lower_red, upper_red)
        _self.FPS.stop()
        _self.LOG.debug("processing time inRange: " + str(_self.FPS.elapsedtime_ms()) + " ms")

        # apply mask on image
        _self.FPS.start()
        output_img = cv2.bitwise_and(img, img, mask=mask)
        _self.FPS.stop()
        _self.LOG.debug("processing time masking: " + str(_self.FPS.elapsedtime_ms()) + " ms")

        return output_img

    def detectEdges(_self, mask, img_org):
        """
        This function detects edges of the two biggest areas on a provided image (mask)
        :param mask: image / mask wo apply edge detection (e.g. only red colored parts)
        :param img_org: original image which will be used for drawing lines on it
        :return: original image and reordered edges (top left, top right, bottom right, bottom left)
        """

        # convert image to grayscale
        img_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        # set all non black pixels to white for BW-image
        img_gray[img_gray > 0] = 255

        # dilated image for remove of small erosions
        kernel = np.ones((_self.kernel_size, _self.kernel_size), np.uint8)
        img_dilated = cv2.dilate(img_gray, kernel, iterations=1)

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

            # get minimal area rectangle
            rect = cv2.minAreaRect(c)
            # represent area as points
            box = cv2.boxPoints(rect)
            # normalize array
            box = np.int0(box)

            cv2.drawContours(img_org, [box], 0, (0, 255, 255), 1)
            box = _self.order_points(box)
            if not i:
                # top right position
                pt_top = tuple(np.int0(box[1]))
                # bottom right position
                pt_bottom = tuple(np.int0(box[2]))
            else:
                # top left position
                pt_top = tuple(np.int0(box[0]))
                # bottom right position
                pt_bottom = tuple(np.int0(box[3]))

            edges.append(pt_top)
            edges.append(pt_bottom)

            cv2.line(img_org, pt_top, pt_bottom, (0, 0, 255), 1)
            cv2.circle(img_org, pt_top, 2, (0, 255, 0), -1)
            cv2.circle(img_org, pt_bottom, 2, (0, 255, 0), -1)

            i = True

        if len(edges) == 4:
            # reorder edges to (top left, top right, bottom right, bottom left)
            edges = [edges[i] for i in [0, 2, 3, 1]]
            _self.LOG.debug("edges: " + str(edges))
            return img_org, edges
        else:
            # not 4 edges found
            # TODO: Error handling, e.g. take next image or so
            return img_org, 0

    def order_points(_self, pts):
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

    def correctPerspectiveView(_self, img, edges):
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

    def initCamera(_self):
        """
        This function will initialize the Raspbian Cam with the predefined settings in the configuration file
        :return: PIRGBArray for using as source for camera capturing
        """
        global camera
        _self.LOG.debug("Camera: Init started")
        camera = PiCamera()
        _self.LOG.debug(
            "Camera: Set resolution to " + str(_self.camera_width) + "x" + str(_self.camera_height))
        camera.resolution = (_self.camera_width, _self.camera_height)
        _self.LOG.debug("Camera: Set framerate to " + str(_self.camera_framerate))
        camera.framerate = _self.camera_framerate
        _self.LOG.debug("Camera: Set ISO to " + str(_self.camera_iso))
        camera.iso = _self.camera_iso
        _self.LOG.debug("Camera: Initialize AWB, calculating...")
        time.sleep(2)
        if _self.camera_awb == 'fixed':
            camera.shutter_speed = camera.exposure_speed
            camera.exposure_mode = 'off'
            gain = camera.awb_gains
            camera.awb_mode = 'off'
            camera.awb_gains = gain
        rawCapture = PiRGBArray(camera, size=(_self.camera_width, _self.camera_height))
        time.sleep(0.1)
        _self.LOG.debug("Camera: Init finished")
        return rawCapture

    def analyzeRomanLetter(_self, img, roi):
        """
        This function determines the number of a roman letter (only I, II, III, IV, V)
        :param img: original image which will be used for drawing lines on it
        :param roi: cropped image with only the letters on it
        :return: detect number as integer
        """
        FPS = FPSHelper()
        number = 0

        # black bit mask
        lower_black = np.array(_self.black_low)
        upper_black = np.array(_self.black_high)

        # create overlay mask for all none matching bits to zero (black)
        mask = cv2.inRange(roi, lower_black, upper_black)

        # apply mask on image
        output_img = cv2.bitwise_or(roi, roi, mask=mask)

        # convert image to grayscale
        img_gray = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)

        # set all non black pixels to white for BW-image
        img_gray[img_gray > 0] = 1

        # edge detection
        _self.FPS.start()
        edges = skeletonize(img_gray)
        edges = edges * 1
        edges[edges == 1] = 255
        edges = np.uint8(edges)
        img_gray_mark = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        lines = cv2.HoughLines(edges, 1, np.pi / 180, 15, np.array([]), 0, 0)
        _self.FPS.stop()
        _self.LOG.debug("processing time HoughLines: " + str(_self.FPS.elapsedtime_ms()) + " ms")

        # if lines found, enumerate number based on its angle
        if lines is not None:
            line, _, _ = lines.shape
            v_left_found = False
            v_right_found = False
            i_count = 0
            all_i = []  # = [[] for i in range(3)]

            for i in range(line):

                rho = lines[i][0][0]  # vector distance to line
                theta = lines[i][0][1]  # angle of line in radian

                a, b = np.cos(theta), np.sin(theta)
                x0, y0 = a * rho, b * rho
                deg = theta * 180 / np.pi  # radian to degree

                line_pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
                line_pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))

                _self.LOG.info("-----")
                _self.LOG.info("linept1: " + str(line_pt1))
                _self.LOG.info("linept2: " + str(line_pt2))
                _self.LOG.info("deg:" + str(deg))

                # detect an I
                if (0.0 < deg < 1.0) or (178.0 < deg < 180.0):
                    _self.LOG.info("I - line found with deg: " + str(deg))

                    # get median x-value of both points
                    x = (int(x0 + 1000 * (-b)) + int(x0 - 1000 * (-b))) / 2
                    all_i.append([x, line_pt1, line_pt2])
                    cv2.line(img_gray_mark, line_pt1, line_pt2, (255, 255, 0), 1, cv2.LINE_AA)

                    """
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * a)
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * a)
                    """
                    _self.LOG.info(
                        "pos line_pt1: " + str(line_pt1) + " vertical line found with deg: " + str(
                            deg) + ", theta: " + str(
                            theta))
                    continue

                # right hand side of V
                elif 10.0 < deg < 20.0:
                    _self.LOG.info("V / - line found with deg: " + str(deg))
                    cv2.line(img_gray_mark, line_pt1, line_pt2, (0, 0, 255), 1, cv2.LINE_AA)
                    v_right_found = True
                    continue

                # left hand side of V
                elif 150.0 < deg < 170.0:
                    _self.LOG.info("V \ - line found with deg: " + str(deg))
                    cv2.line(img_gray_mark, line_pt1, line_pt2, (0, 255, 0), 1, cv2.LINE_AA)
                    v_left_found = True
                    continue
                else:
                    _self.LOG.debug("line with deg: " + str(deg) + "out of allowed range")

            # eliminate redundant detected I
            if len(all_i) != 0:
                all_i.sort()
                tolerance = _self.tolerance_I_gap
                nondup_i = [all_i.pop(0), ]
                all_i_count = 0

                for x in all_i[1::1]:
                    xcor = x[0]
                    pt1 = x[1]
                    pt2 = x[2]
                    # Skip items within tolerance.
                    if abs(nondup_i[all_i_count][0] - xcor) <= tolerance:
                        continue
                    nondup_i.append([xcor, pt1, pt2])
                    cv2.line(img_gray_mark, pt1, pt2, (255, 255, 0), 1, cv2.LINE_AA)
                    all_i_count += 1
                    # i_count += 1
                i_count = len(nondup_i)
                _self.LOG.info("all I: " + str(all_i))
                _self.LOG.info("all nondup I: " + str(nondup_i) + "icount: " + str(i_count))

            # enumerate the number based on detected lines
            if v_left_found and v_right_found:
                number = 5
                if i_count == 1:
                    number = 4
                    _self.LOG.info("detected number: " + str(number))
            elif 0 < i_count < 4:
                number = i_count
                _self.LOG.info("detected number: " + str(number))
            else:
                _self.LOG.error("not able to enumerate number!!")
                # TODO: Error handling if number not detected e.g. other algorithm to detect number

        else:
            _self.LOG.warn("no lines detected on image")
            _self.LOG.info("--")

        return img_gray_mark
        # return number

    def __init__(_self):
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL

        _self.LOG.info("Main: Program started")
        _self.LOG.info("Main: Starting camera init")
        rawCapture = _self.initCamera()
        _self.LOG.info("Main: Start capturing")
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            img = frame.array
            _self.FPS.start()

            redmask = _self.imgcoloredmask_red_shifted(img)
            cv2.imshow("redmask", redmask)
            _self.LOG.debug("Frame: red mask done")
            imgmarked, edges = _self.detectEdges(redmask, img)
            _self.LOG.debug("Frame: edges for letter range detection done")
            if edges != 0:
                _self.LOG.debug("Frame: correct perspective of letter range")
                correctedimg = _self.correctPerspectiveView(img, edges)
                numberimg = _self.analyzeRomanLetter(img, correctedimg)
                _self.FPS.stop()
                _self.LOG.debug("FPS: {0:.2f}".format(_self.FPS.fps()) + " ms: {0:.2f}\n".format(
                    _self.FPS.elapsedtime_ms()))
                cv2.putText(correctedimg, "FPS: {0:.2f}".format(_self.FPS.fps()), (5, 10), font, 0.5,
                            (0, 255, 0),
                            1,
                            cv2.LINE_AA)
                cv2.putText(img, "FPS: {0:.2f}".format(_self.FPS.fps()),
                            (_self.camera_width - 90, _self.camera_height - 10), font, 0.7,
                            (0, 255, 0), 1,
                            cv2.LINE_AA)
                cv2.imshow("Perspective", correctedimg)
                cv2.imshow("Letter", numberimg)
                cv2.imshow("Video", imgmarked)
            else:
                _self.LOG.debug("Frame: no letter range detected")
                _self.FPS.stop()
                _self.LOG.debug("FPS: {0:.2f}".format(_self.FPS.fps()) + " ms: {0:.2f}\n".format(
                    _self.FPS.elapsedtime_ms()))
                cv2.putText(img, "FPS: {0:.2f}".format(_self.FPS.fps()), (550, 460), font, 0.7, (0, 255, 0),
                            1,
                            cv2.LINE_AA)
                cv2.imshow("Video", img)
            key = cv2.waitKey(1) & 0xFF
            rawCapture.truncate(0)
            if key == ord("q"):
                _self.LOG.info("Main: Finished capturing")
                break
        cv2.destroyAllWindows()


if __name__ == '__main__':
    LetterDetectionHandler()
