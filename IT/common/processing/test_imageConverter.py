from unittest import TestCase
import common.config.confighandler as cfg
import cv2
import numpy as np
from common.processing.imageprocessor import ImageConverter

class TestImageConverter(TestCase):
    def test_convertbgr2gray(self):
        #read before and after image from media

        img_letter_II_angle = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle.jpg')
        img_letter_II_angle_bgr2gray  = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_bgr2gray.jpg')

        img_letter_II_normal = cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal.jpg'
        img_letter_III_normal = cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal.jpg'
        img_letter_IV_near = cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near.jpg'
        img_letter_IV_top = cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top.jpg'

        #array = ImageConverter.convertbgr2gray(img_letter_II_angle)
        #cv2.imwrite("bgr2gray_img_letter_II_angle.jpg", array)
        #result = ImageConverter.convertbgr2gray(img_letter_II_angle)
        #cv2.imwrite("result.jpg", result)

        print(ImageConverter.convertbgr2gray(img_letter_II_angle))
        print(img_letter_II_angle_bgr2gray)
        letter_II_angle = np.array_equal(ImageConverter.convertbgr2gray(img_letter_II_angle), img_letter_II_angle_bgr2gray)
        self.assertEqual(letter_II_angle, True)

    def test_convertbgr2hsv(self):
        self.fail()

    def test_convertbgr2hsvfull(self):
        self.fail()

    def test_convertgray2bgr(self):
        self.fail()

    def test_converthsv2bgr(self):
        self.fail()

    def test_convert2blackwhite(self):
        self.fail()

    def test_mask_color_red(self):
        self.fail()

    def test_mask_color_red_fullhsv(self):
        self.fail()

    def test_mask_color_red_traffic(self):
        self.fail()

    def test_mask_color_green(self):
        self.fail()

    def test_remove_erosions(self):
        self.fail()

    def test_transform_perspectiveview2topdownview(self):
        self.fail()

    def test_minimize_roi_lettercontour(self):
        self.fail()

    def test_thinningblackwhiteimage(self):
        self.fail()
