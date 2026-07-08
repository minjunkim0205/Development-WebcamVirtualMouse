import cv2

class Webcam:

    def __init__(self):

        self.cap = cv2.VideoCapture(0)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 60)

        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)

        print(f"Resolution : {width} x {height}")
        print(f"FPS : {fps}")

    def read(self):

        ret, frame = self.cap.read()

        if not ret:
            return None

        frame = cv2.flip(frame, 1)

        return frame

    def release(self):

        self.cap.release()