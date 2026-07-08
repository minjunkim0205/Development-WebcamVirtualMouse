import cv2
from config import CAMERA_INDEX

class Webcam:

    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)

    def read(self):
        ret, frame = self.cap.read()

        if not ret:
            return None

        frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        self.cap.release()