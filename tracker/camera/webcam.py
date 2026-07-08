import cv2
import config


class Webcam:
    def __init__(self):
        backend = cv2.CAP_DSHOW if config.CAMERA_BACKEND == "DSHOW" else 0

        self.cap = cv2.VideoCapture(config.CAMERA_INDEX, backend)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, config.FPS)

        if not self.cap.isOpened():
            raise RuntimeError("Camera open failed")

    def read(self):
        ret, frame = self.cap.read()

        if not ret:
            return None

        if config.MIRROR_CAMERA:
            frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        self.cap.release()