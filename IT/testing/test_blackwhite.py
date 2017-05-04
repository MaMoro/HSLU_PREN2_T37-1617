import cv2
import time
from common.processing.imageconverter import ImageConverter
import common.config.confighandler as cfg
from logging.config import fileConfig

fileConfig(cfg.get_logging_config_fullpath())

while True:
    # image_org = cv2.imread(cfg.get_proj_rootdir() + '/testing/letter_brightness2.jpg')
    image_org = cv2.imread(cfg.get_proj_rootdir() + '/testing/letter_brightness.png')
    # image_org = cv2.imread(cfg.get_proj_rootdir() + '/testing/letter_brightness3.png')
    image_bw = ImageConverter.convert2blackwhite_full(image_org)
    # cv2.imshow("original", image_org)
    cv2.imshow("blackwhite", image_bw)
    time.sleep(0.5)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
