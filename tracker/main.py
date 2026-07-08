import cv2
import time
import numpy as np

import config
from camera.webcam import Webcam
from communication.serial_sender import SerialSender
from hand_tracking.mediapipe_tracker import MediaPipeTracker


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def apply_deadzone(value, deadzone):
    if abs(value) < deadzone:
        return 0
    return value


def main():
    webcam = Webcam()
    tracker = MediaPipeTracker()
    sender = SerialSender()

    prev_index = None

    left_pressed = False
    right_pressed = False

    prev_time = time.time()

    try:
        while True:
            frame = webcam.read()

            if frame is None:
                print("Frame read failed")
                break

            if config.BLACK_BACKGROUND_PREVIEW:
                display_frame = np.zeros_like(frame)
            else:
                display_frame = frame.copy()

            data = tracker.process(frame)

            if data is not None:
                index = data["index"]
                thumb = data["thumb"]
                middle = data["middle"]

                if prev_index is not None:
                    dx = index[0] - prev_index[0]
                    dy = index[1] - prev_index[1]

                    dx = apply_deadzone(dx, config.DEADZONE)
                    dy = apply_deadzone(dy, config.DEADZONE)

                    dx = int(dx * config.SENSITIVITY_X)
                    dy = int(dy * config.SENSITIVITY_Y)

                    dx = clamp(dx, -config.MAX_MOVE, config.MAX_MOVE)
                    dy = clamp(dy, -config.MAX_MOVE, config.MAX_MOVE)

                    if dx != 0 or dy != 0:
                        sender.move(dx, dy)

                prev_index = index

                if data["left_pinch"] and not left_pressed:
                    sender.left_press()
                    left_pressed = True

                elif not data["left_pinch"] and left_pressed:
                    sender.left_release()
                    left_pressed = False

                if data["right_pinch"] and not right_pressed:
                    sender.right_press()
                    right_pressed = True

                elif not data["right_pinch"] and right_pressed:
                    sender.right_release()
                    right_pressed = False

                if config.SHOW_PREVIEW:
                    cv2.circle(display_frame, thumb, 12, (255, 0, 0), -1)
                    cv2.circle(display_frame, index, 12, (0, 255, 0), -1)
                    cv2.circle(display_frame, middle, 12, (0, 255, 255), -1)

                    cv2.putText(
                        display_frame,
                        "THUMB",
                        (thumb[0] + 10, thumb[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 0, 0),
                        2
                    )

                    cv2.putText(
                        display_frame,
                        f"INDEX {index}",
                        (index[0] + 10, index[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        display_frame,
                        "MIDDLE",
                        (middle[0] + 10, middle[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 255),
                        2
                    )

                    cv2.putText(
                        display_frame,
                        f"Left pinch: {data['left_pinch']}",
                        (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        display_frame,
                        f"Right pinch: {data['right_pinch']}",
                        (20, 115),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 255),
                        2
                    )

            else:
                prev_index = None

                if left_pressed:
                    sender.left_release()
                    left_pressed = False

                if right_pressed:
                    sender.right_release()
                    right_pressed = False

            if config.SHOW_PREVIEW:
                if config.SHOW_FPS:
                    now = time.time()
                    fps = 1 / (now - prev_time)
                    prev_time = now

                    cv2.putText(
                        display_frame,
                        f"FPS: {fps:.1f}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                cv2.imshow(config.WINDOW_NAME, display_frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    finally:
        if left_pressed:
            sender.left_release()

        if right_pressed:
            sender.right_release()

        sender.close()
        tracker.close()
        webcam.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()