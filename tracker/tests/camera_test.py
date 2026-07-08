import cv2
import time

CAMERA_INDEX = 0
WIDTH = 1280
HEIGHT = 720
FPS = 30

cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FPS, FPS)

print("Requested:")
print(f"  Width : {WIDTH}")
print(f"  Height: {HEIGHT}")
print(f"  FPS   : {FPS}")

print("Actual:")
print(f"  Width : {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
print(f"  Height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
print(f"  FPS   : {cap.get(cv2.CAP_PROP_FPS)}")

if not cap.isOpened():
    print("Camera open failed")
    exit()

prev_time = time.time()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Frame read failed")
        break

    now = time.time()
    real_fps = 1 / (now - prev_time)
    prev_time = now

    cv2.putText(
        frame,
        f"FPS: {real_fps:.1f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()