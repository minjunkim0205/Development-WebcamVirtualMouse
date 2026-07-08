import cv2
import math
import mediapipe as mp
import config


class MediaPipeTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=config.MAX_NUM_HANDS,
            model_complexity=config.MODEL_COMPLEXITY,
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )

    def process(self, frame):
        h, w, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if not result.multi_hand_landmarks:
            return None

        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark

        thumb = self._to_pixel(lm[4], w, h)
        index = self._to_pixel(lm[8], w, h)
        middle = self._to_pixel(lm[12], w, h)

        thumb_index_distance = self._distance(thumb, index)
        index_middle_distance = self._distance(index, middle)

        return {
            "thumb": thumb,
            "index": index,
            "middle": middle,
            "left_pinch": thumb_index_distance < config.PINCH_THRESHOLD,
            "right_pinch": index_middle_distance < config.PINCH_THRESHOLD,
            "thumb_index_distance": thumb_index_distance,
            "index_middle_distance": index_middle_distance
        }

    def _to_pixel(self, landmark, width, height):
        return int(landmark.x * width), int(landmark.y * height)

    def _distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def close(self):
        self.hands.close()