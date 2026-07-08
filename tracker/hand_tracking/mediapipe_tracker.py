import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):
        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def get_fingers(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = self.hands.process(rgb)

        if not result.multi_hand_landmarks:
            return None

        hand = result.multi_hand_landmarks[0]

        h, w, _ = frame.shape

        thumb = hand.landmark[4]
        index = hand.landmark[8]
        middle = hand.landmark[12]

        return {
            "thumb": (int(thumb.x * w), int(thumb.y * h)),
            "index": (int(index.x * w), int(index.y * h)),
            "middle": (int(middle.x * w), int(middle.y * h)),
        }