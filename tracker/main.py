import cv2
import time
import numpy as np

import config
from camera.webcam import Webcam
from communication.serial_sender import SerialSender
from hand_tracking.mediapipe_tracker import MediaPipeTracker


def handle_mouse_event(sender, button, event):
    if event is None:
        return

    if button == "left":
        if event == "click":
            sender.click("left")
        elif event == "press":
            sender.left_press()
        elif event == "release":
            sender.left_release()

    elif button == "right":
        if event == "click":
            sender.click("right")
        elif event == "press":
            sender.right_press()
        elif event == "release":
            sender.right_release()


def draw_preview(frame, data, fps):
    if data["hand_detected"]:
        thumb = data["thumb"]
        index = data["index"]
        middle = data["middle"]
        palm = data["palm"]

        cv2.circle(frame, thumb, 12, (255, 0, 0), -1)
        cv2.circle(frame, index, 12, (0, 255, 0), -1)
        cv2.circle(frame, middle, 12, (0, 255, 255), -1)
        cv2.circle(frame, palm, 14, (255, 255, 255), -1)

        cv2.putText(
            frame,
            f"INDEX {index}",
            (index[0] + 10, index[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"PALM {palm}",
            (palm[0] + 10, palm[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"L dist: {data['left_distance']:.1f} pressed: {data['left_pressed']}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"R dist: {data['right_distance']:.1f} pressed: {data['right_pressed']}",
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"L event: {data['left_event']}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"R event: {data['right_event']}",
            (20, 185),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

    else:
        cv2.putText(
            frame,
            "No hand detected",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    if config.SHOW_FPS:
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )


def main():
    webcam = Webcam()
    tracker = MediaPipeTracker()
    sender = SerialSender()

    prev_time = time.time()

    try:
        while True:
            frame = webcam.read()

            if frame is None:
                print("Frame read failed")
                break

            data = tracker.process(frame)

            dx = data["move_dx"]
            dy = data["move_dy"]

            if dx != 0 or dy != 0:
                sender.move(dx, dy)

            handle_mouse_event(sender, "left", data["left_event"])
            handle_mouse_event(sender, "right", data["right_event"])

            if config.SHOW_PREVIEW:
                if config.BLACK_BACKGROUND_PREVIEW:
                    display_frame = np.zeros_like(frame)
                else:
                    display_frame = frame.copy()

                now = time.time()
                fps = 1 / (now - prev_time)
                prev_time = now

                draw_preview(display_frame, data, fps)

                cv2.imshow(config.WINDOW_NAME, display_frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    finally:
        if tracker.left_pressed:
            sender.left_release()

        if tracker.right_pressed:
            sender.right_release()

        sender.close()
        tracker.close()
        webcam.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()