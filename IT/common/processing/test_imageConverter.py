from unittest import TestCase
import common.config.confighandler as cfg
import cv2
import numpy as np
from common.processing.imageconverter import ImageConverter


class TestImageConverter(TestCase):

    #read original images from media
    img_letter_II_angle = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle.jpg')
    img_letter_II_normal = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal.jpg')
    img_letter_III_normal = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal.jpg')
    img_letter_IV_near = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near.jpg')
    img_letter_IV_top = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top.jpg')
    img_trafficlight_red = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_red.png')
    img_trafficlight_red_top = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_red_top.png')
    img_trafficlight_red_side = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_red_side.png')
    img_trafficlight_green = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_green.png')
    img_trafficlight_green_top = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_green_top.png')
    img_trafficlight_green_side = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_green_side.png')

    #read gray images from media
    img_letter_II_angle_bgr2gray = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_bgr2gray.png', 0)
    img_letter_II_normal_bgr2gray = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_bgr2gray.png', 0)
    img_letter_III_normal_bgr2gray = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_bgr2gray.png', 0)
    img_letter_IV_near_bgr2gray = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_bgr2gray.png', 0)
    img_letter_IV_top_bgr2gray = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_bgr2gray.png', 0)

    # read minimize roi lettercontour images from media
    img_letter_II_angle_min = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_min.png')
    img_letter_II_normal_min = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_min.png')
    img_letter_III_normal_min = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_min.png')
    img_letter_IV_near_min = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_min.png')
    img_letter_IV_top_min = cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_min.png')

    def createnewreferenceimages(self):
        print('')

        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_angle_bgr2gray.png", ImageConverter.convertbgr2gray(self.img_letter_II_angle))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_normal_bgr2gray.png", ImageConverter.convertbgr2gray(self.img_letter_II_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_III_normal_bgr2gray.png", ImageConverter.convertbgr2gray(self.img_letter_III_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_near_bgr2gray.png", ImageConverter.convertbgr2gray(self.img_letter_IV_near))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_top_bgr2gray.png", ImageConverter.convertbgr2gray(self.img_letter_IV_top))

        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_angle_bgr2hsv.png", ImageConverter.convertbgr2hsv(self.img_letter_II_angle))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_normal_bgr2hsv.png", ImageConverter.convertbgr2hsv(self.img_letter_II_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_III_normal_bgr2hsv.png", ImageConverter.convertbgr2hsv(self.img_letter_III_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_near_bgr2hsv.png", ImageConverter.convertbgr2hsv(self.img_letter_IV_near))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_top_bgr2hsv.png", ImageConverter.convertbgr2hsv(self.img_letter_IV_top))

        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_angle_bgr2hsvfull.png", ImageConverter.convertbgr2hsvfull(self.img_letter_II_angle))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_normal_bgr2hsvfull.png", ImageConverter.convertbgr2hsvfull(self.img_letter_II_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_III_normal_bgr2hsvfull.png", ImageConverter.convertbgr2hsvfull(self.img_letter_III_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_near_bgr2hsvfull.png", ImageConverter.convertbgr2hsvfull(self.img_letter_IV_near))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_top_bgr2hsvfull.png", ImageConverter.convertbgr2hsvfull(self.img_letter_IV_top))

        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_angle_gray2bgr.png", ImageConverter.convertgray2bgr(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_bgr2gray.png', 0)))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_normal_gray2bgr.png", ImageConverter.convertgray2bgr(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_bgr2gray.png', 0)))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_III_normal_gray2bgr.png", ImageConverter.convertgray2bgr(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_bgr2gray.png', 0)))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_near_gray2bgr.png", ImageConverter.convertgray2bgr(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_bgr2gray.png', 0)))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_top_gray2bgr.png", ImageConverter.convertgray2bgr(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_bgr2gray.png', 0)))

        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_angle_hsv2bgr.png", ImageConverter.converthsv2bgr(self.img_letter_II_angle))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_normal_hsv2bgr.png", ImageConverter.converthsv2bgr(self.img_letter_II_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_III_normal_hsv2bgr.png", ImageConverter.converthsv2bgr(self.img_letter_III_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_near_hsv2bgr.png", ImageConverter.converthsv2bgr(self.img_letter_IV_near))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_top_hsv2bgr.png", ImageConverter.converthsv2bgr(self.img_letter_IV_top))

        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_angle_bw.png", ImageConverter.convert2blackwhite(self.img_letter_II_angle))

        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_angle_red.png", ImageConverter.mask_color_red(self.img_letter_II_angle))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_normal_red.png", ImageConverter.mask_color_red(self.img_letter_II_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_III_normal_red.png", ImageConverter.mask_color_red(self.img_letter_III_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_near_red.png", ImageConverter.mask_color_red(self.img_letter_IV_near))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_top_red.png", ImageConverter.mask_color_red(self.img_letter_IV_top))

        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_angle_redfull.png", ImageConverter.mask_color_red_fullhsv(self.img_letter_II_angle))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_II_normal_redfull.png", ImageConverter.mask_color_red_fullhsv(self.img_letter_II_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_III_normal_redfull.png", ImageConverter.mask_color_red_fullhsv(self.img_letter_III_normal))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_near_redfull.png", ImageConverter.mask_color_red_fullhsv(self.img_letter_IV_near))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/letter_IV_top_redfull.png", ImageConverter.mask_color_red_fullhsv(self.img_letter_IV_top))

        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/trafficlight_red_redtraffic.png", ImageConverter.mask_color_red_traffic(self.img_trafficlight_red))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/trafficlight_red_top_redtraffic.png", ImageConverter.mask_color_red_traffic(self.img_trafficlight_red_top))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/trafficlight_red_side_redtraffic.png", ImageConverter.mask_color_red_traffic(self.img_trafficlight_red_side))

        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/trafficlight_green_greentraffic.png", ImageConverter.mask_color_green(self.img_trafficlight_green))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/trafficlight_green_top_greentraffic.png", ImageConverter.mask_color_green(self.img_trafficlight_green_top))
        #cv2.imwrite(cfg.get_proj_rootdir() + "/medias/images/Unittest/trafficlight_green_side_greentraffic.png", ImageConverter.mask_color_green(self.img_trafficlight_green_side))

    def test_convertbgr2gray(self):
        self.assertEqual(np.array_equal(self.img_letter_II_angle_bgr2gray, ImageConverter.convertbgr2gray(self.img_letter_II_angle)), True)
        self.assertEqual(np.array_equal(self.img_letter_II_normal_bgr2gray, ImageConverter.convertbgr2gray(self.img_letter_II_normal)), True)
        self.assertEqual(np.array_equal(self.img_letter_III_normal_bgr2gray, ImageConverter.convertbgr2gray(self.img_letter_III_normal)), True)
        self.assertEqual(np.array_equal(self.img_letter_IV_near_bgr2gray, ImageConverter.convertbgr2gray(self.img_letter_IV_near)), True)
        self.assertEqual(np.array_equal(self.img_letter_IV_top_bgr2gray, ImageConverter.convertbgr2gray(self.img_letter_IV_top)), True)

    def test_convertbgr2hsv(self):
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_bgr2hsv.png'), ImageConverter.convertbgr2hsv(self.img_letter_II_angle)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_bgr2hsv.png'), ImageConverter.convertbgr2hsv(self.img_letter_II_normal)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_bgr2hsv.png'), ImageConverter.convertbgr2hsv(self.img_letter_III_normal)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_bgr2hsv.png'), ImageConverter.convertbgr2hsv(self.img_letter_IV_near)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_bgr2hsv.png'), ImageConverter.convertbgr2hsv(self.img_letter_IV_top)), True)

    def test_convertbgr2hsvfull(self):
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_bgr2hsvfull.png'), ImageConverter.convertbgr2hsvfull(self.img_letter_II_angle)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_bgr2hsvfull.png'), ImageConverter.convertbgr2hsvfull(self.img_letter_II_normal)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_bgr2hsvfull.png'), ImageConverter.convertbgr2hsvfull(self.img_letter_III_normal)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_bgr2hsvfull.png'), ImageConverter.convertbgr2hsvfull(self.img_letter_IV_near)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_bgr2hsvfull.png'), ImageConverter.convertbgr2hsvfull(self.img_letter_IV_top)), True)

    def test_convertgray2bgr(self):
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_gray2bgr.png'), ImageConverter.convertgray2bgr(self.img_letter_II_angle_bgr2gray)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_gray2bgr.png'), ImageConverter.convertgray2bgr(self.img_letter_II_normal_bgr2gray)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_gray2bgr.png'), ImageConverter.convertgray2bgr(self.img_letter_III_normal_bgr2gray)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_gray2bgr.png'), ImageConverter.convertgray2bgr(self.img_letter_IV_near_bgr2gray)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_gray2bgr.png'), ImageConverter.convertgray2bgr(self.img_letter_IV_top_bgr2gray)), True)

    def test_converthsv2bgr(self):
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_hsv2bgr.png'), ImageConverter.converthsv2bgr(self.img_letter_II_angle)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_hsv2bgr.png'), ImageConverter.converthsv2bgr(self.img_letter_II_normal)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_hsv2bgr.png'), ImageConverter.converthsv2bgr(self.img_letter_III_normal)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_hsv2bgr.png'), ImageConverter.converthsv2bgr(self.img_letter_IV_near)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_hsv2bgr.png'), ImageConverter.converthsv2bgr(self.img_letter_IV_top)), True)

    def test_convert2blackwhite(self):
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_bw.png', 0), ImageConverter.convert2blackwhite(self.img_letter_II_angle)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_bw.png', 0), ImageConverter.convert2blackwhite(self.img_letter_II_normal)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_bw.png', 0), ImageConverter.convert2blackwhite(self.img_letter_III_normal)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_bw.png', 0), ImageConverter.convert2blackwhite(self.img_letter_IV_near)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_bw.png', 0), ImageConverter.convert2blackwhite(self.img_letter_IV_top)), True)

    def test_mask_color_red_fullhsv(self):
        #Bar detection
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_angle_redfull.png'), ImageConverter.mask_color_red_fullhsv(self.img_letter_II_angle)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_II_normal_redfull.png'), ImageConverter.mask_color_red_fullhsv(self.img_letter_II_normal)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_III_normal_redfull.png'), ImageConverter.mask_color_red_fullhsv(self.img_letter_III_normal)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_near_redfull.png'), ImageConverter.mask_color_red_fullhsv(self.img_letter_IV_near)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/letter_IV_top_redfull.png'), ImageConverter.mask_color_red_fullhsv(self.img_letter_IV_top)), True)

    def test_mask_color_red_fullhsv_traffic(self):
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_red_redtraffic.png'), ImageConverter.mask_color_red_fullhsv_traffic(self.img_trafficlight_red)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_red_top_redtraffic.png'), ImageConverter.mask_color_red_fullhsv_traffic(self.img_trafficlight_red_top)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_red_side_redtraffic.png'), ImageConverter.mask_color_red_fullhsv_traffic(self.img_trafficlight_red_side)), True)


    def test_mask_color_green_traffic(self):
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_green_greentraffic.png'), ImageConverter.mask_color_green_traffic(self.img_trafficlight_green)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_green_top_greentraffic.png'), ImageConverter.mask_color_green_traffic(self.img_trafficlight_green_top)), True)
        self.assertEqual(np.array_equal(cv2.imread(cfg.get_proj_rootdir() + '/medias/images/Unittest/trafficlight_green_side_greentraffic.png'), ImageConverter.mask_color_green_traffic(self.img_trafficlight_green_side)), True)


    def test_transform_perspectiveview2topdownview(self):
        #TODO Prio B
        self.fail()

    def test_minimize_roi_lettercontour(self):
        # TODO Prio B
        self.fail()

    def test_thinningblackwhiteimage(self):
        #TODO Not tested due to the fact that it is not visible
        self.assertEqual(True, True)
