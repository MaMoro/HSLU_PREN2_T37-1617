from logging.config import fileConfig

import cv2
from common.processing.camerahandler import CameraHandler
import common.config.confighandler as cfg

fileConfig(cfg.get_logging_config_fullpath())
pistream = CameraHandler().start()
while True:
    frame = pistream.read()
    pistream.setbrightness(cfg.get_camera_brightness())
    cv2.imshow("Video", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
CameraHandler().stop()
