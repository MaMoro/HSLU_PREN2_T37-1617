# ================================================================================
# !/usr/bin/python
# TITLE           : imageanalysis.py
# DESCRIPTION     : supportive classes for image analysis
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
import cv2
import math
import common.config.confighandler as cfg
import numpy as np

from logging.config import fileConfig
from collections import Counter
from common.processing.imageconverter import ImageConverter


class ImageAnalysis(object):
    # Configure logging component
    fileConfig(cfg.get_logging_config_fullpath())
    __log = logging.getLogger()
    __log.setLevel(cfg.get_settings_loglevel())

    # Gather config settings
    letter_tolerance_i_gap = cfg.get_letter_tolerance_i_gap()
    letter_tolerance_v_gap = cfg.get_letter_tolerance_v_gap()
    min_maskarea_size = cfg.get_maskletter_min_maskarea_size()
    angle_tolerance_redblocks = 15

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

        img_gray = ImageConverter.convertbgr2gray(mask)  # set image to grayscale
        img_gray[img_gray > 0] = 255  # set all non black pixels to white for BW-image
        img_dilated = ImageConverter.remove_erosions(img_gray)  # dilated image for remove of small erosions

        # find all contours
        (_, cnts, _) = cv2.findContours(img_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # resort contours based on their area from highest to lowest and get only the two greatest
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:2]

        # all edges (top left, bottom left, top right, bottom right)
        edges = []
        left_mask_area_processed = False
        left_line_angle = None
        for c in cnts:
            # TODO: risk of cut red line, need to guarantee that both red blocks are fully visible
            # e.g. ignore red color on image boarder

            rect = cv2.minAreaRect(c)  # get minimal area rectangle
            box = cv2.boxPoints(rect)  # represent area as points
            box = np.int0(np.around(box))  # round values and normalize array

            # check aspect ratio
            box = ImageAnalysis.reorder_edgepoints_clockwise(box)
            vert_line_length = cv2.norm(np.int0(box[0]) - np.int0(box[3]))
            hori_line_length = cv2.norm(np.int0(box[0]) - np.int0(box[1]))
            try:
                if not(5 < (np.int0(vert_line_length) / np.int0(hori_line_length)) < 14):
                    break
            except ZeroDivisionError:
                break

            if not left_mask_area_processed:
                pt_top = tuple(np.int0(box[1]))  # top right position
                pt_bottom = tuple(np.int0(box[2]))  # bottom right position
                left_line_angle = ImageAnalysis.__anglewithtwopoints(pt_top, pt_bottom)

            else:
                pt_top = tuple(np.int0(box[0]))  # top left position
                pt_bottom = tuple(np.int0(box[3]))  # bottom right position
                right_line_angle = ImageAnalysis.__anglewithtwopoints(pt_top, pt_bottom)
                if not (math.fabs(right_line_angle - left_line_angle) < ImageAnalysis.angle_tolerance_redblocks):
                    break

            # only allow rectangles with minimal area size
            dist = math.sqrt((abs(pt_top[0] - pt_bottom[0])) ** 2 + (abs(pt_top[1] - pt_bottom[1])) ** 2)
            if dist > ImageAnalysis.min_maskarea_size:
                edges.append(pt_top)
                edges.append(pt_bottom)
            left_mask_area_processed = True

        if len(edges) == 4:
            # reorder edges to (top left, top right, bottom right, bottom left)
            edges = [edges[i] for i in [0, 2, 3, 1]]
            return edges
        else:
            return 0

    @staticmethod
    def get_ordered_corners_drawed(mask, img):
        """
        This function detects edges of the two biggest areas on a provided image (mask)
        :param mask: image / mask wo apply edge detection (e.g. only red colored parts)
        :param img: original image which will be used for drawing lines on it
        :return: reordered edges/corners (top left, top right, bottom right, bottom left)
        """

        img_gray = ImageConverter.convertbgr2gray(mask)  # set image to grayscale
        img_gray[img_gray > 0] = 255  # set all non black pixels to white for BW-image
        img_dilated = ImageConverter.remove_erosions(img_gray)  # dilated image for remove of small erosions

        # find all contours
        (_, cnts, _) = cv2.findContours(img_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # resort contours based on their area from highest to lowest and get only the two greatest
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:2]

        # all edges (top left, bottom left, top right, bottom right)
        edges = []
        left_mask_area_processed = False
        left_line_angle = None
        for c in cnts:
            # TODO: risk of cut red line, need to guarantee that both red blocks are fully visible
            # e.g. ignore red color on image boarder

            rect = cv2.minAreaRect(c)  # get minimal area rectangle
            box = cv2.boxPoints(rect)  # represent area as points
            box = np.int0(np.around(box))  # round values and normalize array
            cv2.drawContours(img, [box], 0, (0, 255, 255), 1)

            box = ImageAnalysis.reorder_edgepoints_clockwise(box)
            vert_line_length = cv2.norm(np.int0(box[0]) - np.int0(box[3]))
            hori_line_length = cv2.norm(np.int0(box[0]) - np.int0(box[1]))
            try:
                if not(5 < (vert_line_length / hori_line_length) < 14):
                    break
            except ZeroDivisionError:
                break

            if not left_mask_area_processed:
                pt_top = tuple(np.int0(box[1]))  # top right position
                pt_bottom = tuple(np.int0(box[2]))  # bottom right position
                left_line_angle = ImageAnalysis.__anglewithtwopoints(pt_top, pt_bottom)
                ImageAnalysis.__log.debug("Winkel left: " + str(left_line_angle))
            else:
                pt_top = tuple(np.int0(box[0]))  # top left position
                pt_bottom = tuple(np.int0(box[3]))  # bottom left position
                right_line_angle = ImageAnalysis.__anglewithtwopoints(pt_top, pt_bottom)
                ImageAnalysis.__log.debug("Winkel right: " + str(right_line_angle))
                if not (math.fabs(right_line_angle - left_line_angle) < ImageAnalysis.angle_tolerance_redblocks):
                    break

            # only allow rectangles with minimal area size
            dist = math.sqrt((abs(pt_top[0] - pt_bottom[0])) ** 2 + (abs(pt_top[1] - pt_bottom[1])) ** 2)
            if dist > ImageAnalysis.min_maskarea_size:
                edges.append(pt_top)
                edges.append(pt_bottom)
                cv2.line(img, pt_top, pt_bottom, (0, 0, 255), 1)
                cv2.circle(img, pt_top, 2, (0, 255, 0), -1)
                cv2.circle(img, pt_bottom, 2, (0, 255, 0), -1)
            left_mask_area_processed = True

        if len(edges) == 4:
            # reorder edges to (top left, top right, bottom right, bottom left)
            edges = [edges[i] for i in [0, 2, 3, 1]]
            ImageAnalysis.__log.debug("edges: " + str(edges))
            return img, edges
        else:
            return img, 0

    @staticmethod
    def get_roman_letter_drawed(roi):
        """
        Determines the number of an image with roman letter on it (only I, II, III, IV, V) and draws line on image
        :param roi: cropped image with only the letters on it
        :return: image with all detected lines for the number 
        """
        # FPS = FPSHelper()
        number = 0
        img_bw = ImageConverter.convert2blackwhite(roi)

        # edge detection
        #FPS.start()
        edges = ImageConverter.thinningblackwhiteimage(img_bw)
        img_gray_mark = ImageConverter.convertgray2bgr(edges)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 15, np.array([]), 0, 0)
        # FPS.stop()
        #ImageAnalysis.__log.info("processing time HoughLines & thinning: " + str(FPS.elapsedtime_ms()) + " ms")

        #FPS.start()
        # if lines found, enumerate number based on its angle
        if lines is not None:
            line, _, _ = lines.shape
            v_left_found = False
            v_right_found = False
            all_i = []
            all_v_left = []
            all_v_right = []

            for i in range(line):

                rho = lines[i][0][0]  # vector distance to line
                theta = lines[i][0][1]  # angle of line in radian

                a, b = np.cos(theta), np.sin(theta)
                x0, y0 = a * rho, b * rho
                deg = theta * 180 / np.pi  # radian to degree

                line_pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
                line_pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))

                ImageAnalysis.__log.debug(
                    "-----\nlinept1: " + str(line_pt1) + "\nlinept2: " + str(line_pt2) + "\ndeg:" + str(deg))

                # detect an I
                if (0.0 <= deg < 2.0) or (178.0 < deg <= 180.0):
                    ImageAnalysis.__log.debug("I - line found with deg: " + str(deg))

                    # get median x-value of both points
                    x = (int(x0 + 1000 * (-b)) + int(x0 - 1000 * (-b))) / 2
                    all_i.append([x, line_pt1, line_pt2])

                    ImageAnalysis.__log.debug(
                        "pos line_pt1: " + str(line_pt1) + " vertical line found with deg: " + str(
                            deg) + ", theta: " + str(theta))
                    continue

                # right hand side of V
                elif 10.0 < deg < 20.0:
                    ImageAnalysis.__log.debug("V / - line found with deg: " + str(deg))
                    x = (int(x0 + 1000 * (-b)) + int(x0 - 1000 * (-b))) / 2
                    all_v_right.append([x, line_pt1, line_pt2])
                    continue

                # left hand side of V
                elif 150.0 < deg < 170.0:
                    ImageAnalysis.__log.debug("V \ - line found with deg: " + str(deg))
                    x = (int(x0 + 1000 * (-b)) + int(x0 - 1000 * (-b))) / 2
                    all_v_left.append([x, line_pt1, line_pt2])
                    continue
                else:
                    ImageAnalysis.__log.debug("line with deg: " + str(deg) + "out of allowed range")
            # ImageAnalysis.__log.info("size of I: " + str(len(all_i)))
            # FPS.stop()
            #ImageAnalysis.__log.info("processing time evaluate all lines: " + str(FPS.elapsedtime_ms()) + " ms")

            # eliminate redundant detected I
            #FPS.start()
            nonredundant_i = ImageAnalysis.__eliminate_redundant_i(all_i)
            nonredundant_v_left = ImageAnalysis.__eliminate_redundant_v(all_v_left)
            nonredundant_v_right = ImageAnalysis.__eliminate_redundant_v(all_v_right)
            # FPS.stop()
            #ImageAnalysis.__log.info("processing time remove redundances: " + str(FPS.elapsedtime_ms()) + " ms")

            #FPS.start()
            roi_height = roi.shape[0]
            nonintersected_i = ImageAnalysis.__eliminate_intersectioned_i_with_v(nonredundant_v_left,
                                                                                 nonredundant_v_right,
                                                                                 nonredundant_i.copy(), roi_height)
            # FPS.stop()
            #ImageAnalysis.__log.info("processing time intersection: " + str(FPS.elapsedtime_ms()) + " ms")

            # enumerate the number based on detected lines
            ImageAnalysis.__log.debug("v_left: " + str(len(nonredundant_v_left)) + " | v_right: " + str(
                len(nonredundant_v_right)) + " | i: " + str(len(nonintersected_i)))

            #FPS.start()
            if len(nonredundant_v_left) > 0:
                img_gray_mark = ImageAnalysis.__printlines(img_gray_mark, nonredundant_v_left, "V-LEFT")
                v_left_found = True
            if len(nonredundant_v_right) > 0:
                img_gray_mark = ImageAnalysis.__printlines(img_gray_mark, nonredundant_v_right, "V-RIGHT")
                v_right_found = True
            i_count = len(nonintersected_i)
            if i_count > 0:
                img_gray_mark = ImageAnalysis.__printlines(img_gray_mark, nonintersected_i, "I")

            # FPS.stop()
            #ImageAnalysis.__log.info("processing time printlines: " + str(FPS.elapsedtime_ms()) + " ms")

            number = ImageAnalysis._enumerate_number_withlines(v_left_found, v_right_found, i_count)
        else:
            ImageAnalysis.__log.warning("no lines detected on image")
        ImageAnalysis.__log.debug("--")

        return img_gray_mark

    @staticmethod
    def get_roman_letter(roi):
        """
        Determines the number of an image with roman letter on it (only I, II, III, IV, V)
        :param roi: cropped image with only the letters on it
        :return: detected number  as integer, zero if not able to enumerate 
        """
        number = 0
        img_bw = ImageConverter.convert2blackwhite(roi)

        # edge detection
        edges = ImageConverter.thinningblackwhiteimage(img_bw)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 15, np.array([]), 0, 0)
        # if lines found, enumerate number based on its angle
        if lines is not None:
            line, _, _ = lines.shape
            v_left_found = False
            v_right_found = False
            all_i = []
            all_v_left = []
            all_v_right = []

            for i in range(line):

                rho = lines[i][0][0]  # vector distance to line
                theta = lines[i][0][1]  # angle of line in radian

                a, b = np.cos(theta), np.sin(theta)
                x0, y0 = a * rho, b * rho
                deg = theta * 180 / np.pi  # radian to degree

                line_pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
                line_pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))

                # detect an I
                if (0.0 <= deg < 2.0) or (178.0 < deg <= 180.0):
                    # get median x-value of both points
                    x = (int(x0 + 1000 * (-b)) + int(x0 - 1000 * (-b))) / 2
                    all_i.append([x, line_pt1, line_pt2])
                    continue

                # right hand side of V
                elif 10.0 < deg < 20.0:
                    x = (int(x0 + 1000 * (-b)) + int(x0 - 1000 * (-b))) / 2
                    all_v_right.append([x, line_pt1, line_pt2])
                    continue

                # left hand side of V
                elif 150.0 < deg < 170.0:
                    x = (int(x0 + 1000 * (-b)) + int(x0 - 1000 * (-b))) / 2
                    all_v_left.append([x, line_pt1, line_pt2])
                    continue

            # eliminate redundant detected I
            nonredundant_i = ImageAnalysis.__eliminate_redundant_i(all_i)
            nonredundant_v_left = ImageAnalysis.__eliminate_redundant_v(all_v_left)
            nonredundant_v_right = ImageAnalysis.__eliminate_redundant_v(all_v_right)
            roi_height = roi.shape[0]
            nonintersected_i = ImageAnalysis.__eliminate_intersectioned_i_with_v(nonredundant_v_left,
                                                                                 nonredundant_v_right,
                                                                                 nonredundant_i.copy(), roi_height)

            if len(nonredundant_v_left) > 0:
                v_left_found = True
            if len(nonredundant_v_right) > 0:
                v_right_found = True
            i_count = len(nonintersected_i)

            number = ImageAnalysis._enumerate_number_withlines(v_left_found, v_right_found, i_count)

        else:
            ImageAnalysis.__log.warning("no lines detected on image")
        return number

    @staticmethod
    def __anglewithtwopoints(top, bottom):
        # Compute x/y distance
        (dx, dy) = (bottom[0] - top[0], bottom[1] - top[1])
        try:
            # Compute the angle
            angle = math.atan(float(dx) / float(dy))
        except ZeroDivisionError:
            angle = 0.0
        angle *= 180 / math.pi
        # Now you have an angle from -90 to +90.
        if dy < 0:
            angle += 180
        return angle

    @staticmethod
    def _enumerate_number_withlines(v_left, v_right, i):
        """
        Gets number based on detected lines - protected not private for unittest
        :param v_left:  bool if left side of V detected
        :param v_right: bool if right side of V detected
        :param i: amount of detected I's
        :return: number 0-5, 0 if not able to enumerate
        """

        if v_left and v_right:
            number = 5
            if i != 0:
                number = 4
            ImageAnalysis.__log.info("detected number: " + str(number))
            return number
        elif (i is not None) and (0 < i < 4):
            ImageAnalysis.__log.info("detected number: " + str(i))
            return i
        else:
            ImageAnalysis.__log.warning("not able to enumerate number...")
            return 0

    @staticmethod
    def __eliminate_redundant_i(all_detected_i):
        """
        Eliminates all redundant detected of an I
        :param all_detected_i: all possible I lines in a list
        :return: list with all non-redundant I lines
        """
        if len(all_detected_i) != 0:
            all_detected_i.sort()
            nondup_i = [all_detected_i.pop(0), ]
            all_i_count = 0

            for x in all_detected_i[1::1]:
                xcor = x[0]
                pt1 = x[1]
                pt2 = x[2]
                # Skip items within tolerance.
                if abs(nondup_i[all_i_count][0] - xcor) <= ImageAnalysis.letter_tolerance_i_gap:
                    continue
                nondup_i.append([xcor, pt1, pt2])
                all_i_count += 1
            return nondup_i
        else:
            return []

    @staticmethod
    def __eliminate_redundant_v(all_detected_v):
        """
        Eliminates all redundant lines of a V (only one side of V)
        :param all_detected_v: all possible V lines in a list
        :return: list with all non-redundant V lines (only one side of V)
        """
        if len(all_detected_v) != 0:
            all_detected_v.sort()
            nondup_v = [all_detected_v.pop(0), ]
            all_v_count = 0

            for x in all_detected_v[1::1]:
                xcor = x[0]
                pt1 = x[1]
                pt2 = x[2]
                # Skip items within tolerance.
                if abs(nondup_v[all_v_count][0] - xcor) <= ImageAnalysis.letter_tolerance_v_gap:
                    continue
                nondup_v.append([xcor, pt1, pt2])
                all_v_count += 1
            return nondup_v
        else:
            return []

    @staticmethod
    def __eliminate_intersectioned_i_with_v(all_v_left, all_v_right, all_i, img_height):
        """
        Eliminate all intersecting I with any V line
        :param all_v_left: list with all non-redundant V left side lines
        :param all_v_right: list with all non-redundant V right side lines
        :param all_i: list with all non-redundanz I lines
        :param img_height: image height to allow correct calculations
        :return: list with all non-intersected I lines
        """
        for candidate in all_i:
            for v in all_v_left:
                intersectionfound = ImageAnalysis.__line_intersection(v, candidate)
                if intersectionfound:
                    # ignore intersection if line is intersectioned in the top 20% of the image as a V left line could possibly correctly intersect in this area
                    if intersectionfound[1] > img_height / 5:
                        all_i.remove(candidate)
                        break
            else:
                for v in all_v_right:
                    intersectionfound = ImageAnalysis.__line_intersection(v, candidate)
                    if intersectionfound:
                        # ignore intersection if it's outter image
                        if 0 < intersectionfound[1] < img_height:
                            all_i.remove(candidate)
                            break
        return all_i

    @staticmethod
    def __line_intersection(line1, line2):
        """
        Check if two lines intersect themself
        :param line1: first line (note: list e.g. (22.3, (x1,y1), (x2,y2))
        :param line2: second line (note: list e.g. (22.3, (x1,y1), (x2,y2))
        :return: x,y position of intersection or if no intersection => False
        """

        xdiff = (line1[1][0] - line1[2][0], line2[1][0] - line2[2][0])
        ydiff = (line1[1][1] - line1[2][1], line2[1][1] - line2[2][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return False

        d = (det(line1[1], line1[2]), det(line2[1], line2[2]))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

    @staticmethod
    def __printlines(img, lines, linetype):
        """
        Print lines on image
        :param img: Image to apply lines on
        :param lines: all lines to be printed
        :param linetype: line type to match coloring - VALUES: I, V-LEFT, V-RIGHT
        :return: image with colored lines
        """
        if len(lines) != 0:
            for line in lines:
                if linetype == "I":
                    cv2.line(img, line[1], line[2], (255, 255, 0), 1, cv2.LINE_AA)
                elif linetype == "V-LEFT":
                    cv2.line(img, line[1], line[2], (0, 255, 0), 1, cv2.LINE_AA)
                elif linetype == "V-RIGHT":
                    cv2.line(img, line[1], line[2], (0, 0, 255), 1, cv2.LINE_AA)
                else:
                    ImageAnalysis.__log.info("wrong line type provided, line will not be printed...")
        else:
            ImageAnalysis.__log.info("no lines provided to print...")
        return img

    @staticmethod
    def most_voted_number(allnumbers):
        """
        Enumerates most voted numbers of provided list
        :param allnumbers: list to enumerate most voted number
        :return: most voted number
        """
        count = Counter(allnumbers)
        mostvotednumber = count.most_common(1)[0][0]
        ImageAnalysis.__log.info("Most voted number is: " + str(mostvotednumber))
        return mostvotednumber
