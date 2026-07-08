import cv2
import mediapipe as mp
import time

CAMERA_INDEX = 0
WIDTH = 1280
HEIGHT = 720
FPS = 30

cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FPS, FPS)

if not cap.isOpened():
    print("Camera open failed")
    exit()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

prev_time = time.time()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Frame read failed")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    index_pos = None

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]

        landmarks = hand_landmarks.landmark

        # 엄지, 검지, 중지 끝 좌표
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]

        thumb_x = int(thumb_tip.x * w)
        thumb_y = int(thumb_tip.y * h)

        index_x = int(index_tip.x * w)
        index_y = int(index_tip.y * h)

        middle_x = int(middle_tip.x * w)
        middle_y = int(middle_tip.y * h)

        index_pos = (index_x, index_y)

        # 엄지
        cv2.circle(frame, (thumb_x, thumb_y), 12, (255, 0, 0), -1)
        cv2.putText(
            frame,
            "THUMB",
            (thumb_x + 10, thumb_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2
        )

        # 검지
        cv2.circle(frame, (index_x, index_y), 12, (0, 255, 0), -1)
        cv2.putText(
            frame,
            f"INDEX ({index_x}, {index_y})",
            (index_x + 10, index_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        # 중지
        cv2.circle(frame, (middle_x, middle_y), 12, (0, 255, 255), -1)
        cv2.putText(
            frame,
            "MIDDLE",
            (middle_x + 10, middle_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )

        print(f"Index tip: x={index_x}, y={index_y}")

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

    if index_pos:
        cv2.putText(
            frame,
            f"Index: {index_pos}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("MediaPipe Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()