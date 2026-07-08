import cv2
import math

from camera.webcam import Webcam
from hand_tracking.mediapipe_tracker import HandTracker


def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


cam = Webcam()
tracker = HandTracker()

left_pressed = False

while True:
    frame = cam.read()

    if frame is None:
        break

    fingers = tracker.get_fingers(frame)

    if fingers:
        thumb = fingers["thumb"]
        index = fingers["index"]
        middle = fingers["middle"]

        cv2.circle(frame, thumb, 8, (255, 0, 0), -1)
        cv2.circle(frame, index, 8, (0, 255, 0), -1)
        cv2.circle(frame, middle, 8, (0, 0, 255), -1)

        thumb_index_dist = distance(thumb, index)

        if thumb_index_dist < 40 and not left_pressed:
            print("LEFT_DOWN")
            left_pressed = True

        elif thumb_index_dist > 60 and left_pressed:
            print("LEFT_UP")
            left_pressed = False

        cv2.putText(frame, f"thumb-index: {int(thumb_index_dist)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("MediaPipe Test", frame)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()