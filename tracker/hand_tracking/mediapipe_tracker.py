import cv2
import math
import time
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

        self.prev_thumb = None
        self.prev_index = None
        self.prev_middle = None

        self.prev_cursor = None

        self.left_pressed = False
        self.right_pressed = False

        self.left_pinch_start_time = None
        self.right_pinch_start_time = None

    def process(self, frame):
        h, w, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if not result.multi_hand_landmarks:
            return self._no_hand_result()

        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark

        thumb_raw = self._to_pixel(lm[4], w, h)
        index_raw = self._to_pixel(lm[8], w, h)
        middle_raw = self._to_pixel(lm[12], w, h)

        thumb = self._smooth_point(self.prev_thumb, thumb_raw)
        index = self._smooth_point(self.prev_index, index_raw)
        middle = self._smooth_point(self.prev_middle, middle_raw)

        self.prev_thumb = thumb
        self.prev_index = index
        self.prev_middle = middle

        dx, dy = self._calculate_move(index)
        self.prev_cursor = index

        left_distance = self._distance(thumb, index)
        right_distance = self._distance(thumb, middle)

        left_action = self._handle_button(
            distance=left_distance,
            pressed=self.left_pressed,
            pinch_start_time=self.left_pinch_start_time
        )

        self.left_pressed = left_action["pressed"]
        self.left_pinch_start_time = left_action["pinch_start_time"]

        right_action = self._handle_button(
            distance=right_distance,
            pressed=self.right_pressed,
            pinch_start_time=self.right_pinch_start_time
        )

        self.right_pressed = right_action["pressed"]
        self.right_pinch_start_time = right_action["pinch_start_time"]

        return {
            "hand_detected": True,

            "thumb": thumb,
            "index": index,
            "middle": middle,

            "move_dx": dx,
            "move_dy": dy,

            "left_event": left_action["event"],
            "right_event": right_action["event"],

            "left_pressed": self.left_pressed,
            "right_pressed": self.right_pressed,

            "left_distance": left_distance,
            "right_distance": right_distance
        }

    def _no_hand_result(self):
        self.prev_thumb = None
        self.prev_index = None
        self.prev_middle = None
        self.prev_cursor = None

        left_event = None
        right_event = None

        if self.left_pressed:
            left_event = "release"

        if self.right_pressed:
            right_event = "release"

        self.left_pressed = False
        self.right_pressed = False

        self.left_pinch_start_time = None
        self.right_pinch_start_time = None

        return {
            "hand_detected": False,

            "thumb": None,
            "index": None,
            "middle": None,

            "move_dx": 0,
            "move_dy": 0,

            "left_event": left_event,
            "right_event": right_event,

            "left_pressed": False,
            "right_pressed": False,

            "left_distance": None,
            "right_distance": None
        }

    def _calculate_move(self, index):
        if self.prev_cursor is None:
            return 0, 0

        dx = index[0] - self.prev_cursor[0]
        dy = index[1] - self.prev_cursor[1]

        dx = self._apply_deadzone(dx)
        dy = self._apply_deadzone(dy)

        dx = int(dx * config.SENSITIVITY_X)
        dy = int(dy * config.SENSITIVITY_Y)

        dx = self._clamp(dx, -config.MAX_MOVE, config.MAX_MOVE)
        dy = self._clamp(dy, -config.MAX_MOVE, config.MAX_MOVE)

        return dx, dy

    def _handle_button(self, distance, pressed, pinch_start_time):
        now = time.time()
        event = None

        if pinch_start_time is None:
            pinch_active = distance < config.PINCH_PRESS_THRESHOLD
        else:
            pinch_active = distance < config.PINCH_RELEASE_THRESHOLD

        if pinch_active and pinch_start_time is None:
            pinch_start_time = now

        if pinch_active and not pressed and pinch_start_time is not None:
            elapsed = now - pinch_start_time

            if elapsed >= config.CLICK_HOLD_TIME:
                event = "press"
                pressed = True

        if not pinch_active and pinch_start_time is not None:
            elapsed = now - pinch_start_time

            if pressed:
                event = "release"
                pressed = False

            elif elapsed < config.CLICK_HOLD_TIME:
                event = "click"

            pinch_start_time = None

        return {
            "event": event,
            "pressed": pressed,
            "pinch_start_time": pinch_start_time
        }

    def _to_pixel(self, landmark, width, height):
        return int(landmark.x * width), int(landmark.y * height)

    def _smooth_point(self, prev, current):
        if not config.ENABLE_SMOOTHING:
            return current

        if prev is None:
            return current

        alpha = config.SMOOTHING_ALPHA

        x = int(prev[0] * (1 - alpha) + current[0] * alpha)
        y = int(prev[1] * (1 - alpha) + current[1] * alpha)

        return x, y

    def _distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def _apply_deadzone(self, value):
        if abs(value) < config.DEADZONE:
            return 0
        return value

    def _clamp(self, value, min_value, max_value):
        return max(min_value, min(max_value, value))

    def close(self):
        self.hands.close()