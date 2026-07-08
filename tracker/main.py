import cv2

from camera.webcam import Webcam
from communication.serial_sender import SerialSender
from hand_tracking.mediapipe_tracker import HandTracker

from config import *
from utils.math_utils import clamp

cam = Webcam()
tracker = HandTracker()
sender = SerialSender(SERIAL_PORT, BAUDRATE)

prev = None

while True:
    frame = cam.read()
    if frame is None:
        break
    pos = tracker.get_index_finger(frame)
    if pos:
        cv2.circle(frame, pos, 8, (0,255,0), -1)
        if prev:
            dx = clamp((pos[0]-prev[0])*SENSITIVITY,-MAX_MOVE,MAX_MOVE)
            dy = clamp((pos[1]-prev[1])*SENSITIVITY,-MAX_MOVE,MAX_MOVE)
            if abs(dx) < DEADZONE:
                dx = 0
            if abs(dy) < DEADZONE:
                dy = 0
            sender.move(dx,dy)
        prev = pos
    else:
        prev = None
    cv2.imshow("Virtual Mouse",frame)
    if cv2.waitKey(1)==27:
        break

cam.release()
sender.close()

cv2.destroyAllWindows()