import cv2

from camera.webcam import Webcam

cam = Webcam()

while True:

    frame = cam.read()

    if frame is None:
        break

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == 27:
        break

cam.release()

cv2.destroyAllWindows()