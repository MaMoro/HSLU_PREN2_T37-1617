from unittest import TestCase
import common.config.confighandler as cfg
import cv2
import numpy as np
from common.processing.imageprocessor import ImageConverter

class TestImageConverter(TestCase):
    #read original images from media
    img_letter_II_angle = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle.jpg')
    img_letter_II_normal = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal.jpg')
    img_letter_III_normal = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal.jpg')
    img_letter_IV_near = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near.jpg')
    img_letter_IV_top = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top.jpg')

    #read gray images from media
    img_letter_II_angle_bgr2gray = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_bgr2gray.jpg')
    img_letter_II_normal_bgr2gray = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_bgr2gray.jpg')
    img_letter_III_normal_bgr2gray = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_bgr2gray.jpg')
    img_letter_IV_near_bgr2gray = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_bgr2gray.jpg')
    img_letter_IV_top_bgr2gray = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_bgr2gray.jpg')

    #read hsv images from media
    img_letter_II_angle_bgr2hsv = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_bgr2hsv.jpg')
    img_letter_II_normal_bgr2hsv = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_bgr2hsv.jpg')
    img_letter_III_normal_bgr2hsv = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_bgr2hsv.jpg')
    img_letter_IV_near_bgr2hsv = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_bgr2hsv.jpg')
    img_letter_IV_top_bgr2hsv = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_bgr2hsv.jpg')

    # read hsvfull images from media
    img_letter_II_angle_bgr2hsvfull = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_bgr2hsvfull.jpg')
    img_letter_II_normal_bgr2hsvfull = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_bgr2hsvfull.jpg')
    img_letter_III_normal_bgr2hsvfull = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_bgr2hsvfull.jpg')
    img_letter_IV_near_bgr2hsvfull = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_bgr2hsvfull.jpg')
    img_letter_IV_top_bgr2hsvfull = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_bgr2hsvfull.jpg')

    # read mask color red images from media
    img_letter_II_angle_red = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_red.jpg')
    img_letter_II_normal_red = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_red.jpg')
    img_letter_III_normal_red = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_red.jpg')
    img_letter_IV_near_red = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_red.jpg')
    img_letter_IV_top_red = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_red.jpg')


    # read mask color red fullhsv images from media
    img_letter_II_angle_redfull = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_redfull.jpg')
    img_letter_II_normal_redfull = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_redfull.jpg')
    img_letter_III_normal_redfull = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_redfull.jpg')
    img_letter_IV_near_redfull = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_redfull.jpg')
    img_letter_IV_top_redfull = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_redfull.jpg')

    # read minimize roi lettercontour images from media
    img_letter_II_angle_min = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_min.jpg')
    img_letter_II_normal_min = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_min.jpg')
    img_letter_III_normal_min = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_min.jpg')
    img_letter_IV_near_min = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_min.jpg')
    img_letter_IV_top_min = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_min.jpg')

    def test_convertbgr2gray(self):

        print(ImageConverter.convertbgr2gray(self.img_letter_II_angle))
        print(self.img_letter_II_angle_bgr2gray)
        self.assertEqual(np.array_equal(ImageConverter.convertbgr2gray(self.img_letter_II_angle), self.img_letter_II_angle_bgr2gray))

    def test_convertbgr2hsv(self):
        self.fail()

    def test_convertbgr2hsvfull(self):
        self.fail()

    def test_convertgray2bgr(self):
        self.fail()

    def test_converthsv2bgr(self):
        self.fail()

    def test_convert2blackwhite(self):
        #TODO doesnt seem to work as expected ?
        cv2.imwrite("letter_II_angle_bw.jpg", ImageConverter.convert2blackwhite(self.img_letter_II_angle))
        cv2.imwrite("letter_II_normal_bw.jpg", ImageConverter.convert2blackwhite(self.img_letter_II_normal))
        cv2.imwrite("letter_III_normal_bw.jpg", ImageConverter.convert2blackwhite(self.img_letter_III_normal))
        cv2.imwrite("letter_IV_near_bw.jpg", ImageConverter.convert2blackwhite(self.img_letter_IV_near))
        cv2.imwrite("letter_IV_top_bw.jpg", ImageConverter.convert2blackwhite(self.img_letter_IV_top))
        self.fail()

    def test_mask_color_red(self):
        self.fail()

    def test_mask_color_red_fullhsv(self):
        self.fail()

    def test_mask_color_red_traffic(self):
        #TODO
        self.fail()

    def test_mask_color_green(self):
        #TODO
        self.fail()

    def test_remove_erosions(self):
        #TODO
        self.fail()

    def test_transform_perspectiveview2topdownview(self):
        #TODO
        self.fail()

    def test_minimize_roi_lettercontour(self):
        self.fail()

    def test_thinningblackwhiteimage(self):
        #TODO as soon as BW image works...
        self.fail()
