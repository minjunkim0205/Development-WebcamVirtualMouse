import cv2
import mediapipe as mp

class HandTracker:

    def __init__(self):

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def get_index_finger(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = self.hands.process(rgb)

        if not result.multi_hand_landmarks:
            return None

        hand = result.multi_hand_landmarks[0]

        h, w, _ = frame.shape

        tip = hand.landmark[8]

        return (
            int(tip.x * w),
            int(tip.y * h)
        )