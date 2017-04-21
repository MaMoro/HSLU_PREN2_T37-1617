import cv2
from common.processing.camerahandler import CameraHandler

from common.processing.imageconverter import ImageConverter

print("Start capturing")
pistream = CameraHandler().start()
while True:
    frame = pistream.read()
    redmask = ImageConverter.mask_color_red_fullhsv_traffic(frame)
    greenmask = ImageConverter.mask_color_green_traffic(frame)
    cv2.imshow("redmask", redmask)
    cv2.imshow("greenmask", greenmask)
    cv2.imshow("original", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        print("Finished capturing")
        break
CameraHandler().stop()
cv2.destroyAllWindows()
