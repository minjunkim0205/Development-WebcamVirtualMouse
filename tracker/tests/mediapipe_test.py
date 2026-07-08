import cv2

from camera.webcam import Webcam
from hand_tracking.mediapipe_tracker import HandTracker

cam = Webcam()

tracker = HandTracker()

while True:

    frame = cam.read()

    if frame is None:
        break

    pos = tracker.get_index_finger(frame)

    if pos:

        cv2.circle(frame, pos, 8, (0,255,0), -1)

        print(pos)

    cv2.imshow("Hand", frame)

    if cv2.waitKey(1) == 27:
        break

cam.release()

cv2.destroyAllWindows()