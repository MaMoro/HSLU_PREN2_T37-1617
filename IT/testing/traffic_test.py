import cv2
from common.processing.camerahandler import CameraHandler

from common.processing.imageconverter import ImageConverter

print("Start capturing")
pistream = CameraHandler().start()
while True:
    frame = pistream.read()
    # redmask = ImageConverter.mask_color_red_fullhsv(frame)
    redmask = ImageConverter.mask_color_red_traffic(frame)
    cv2.imshow("redmask", redmask)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        print("Finished capturing")
        break
CameraHandler().stop()
cv2.destroyAllWindows()
