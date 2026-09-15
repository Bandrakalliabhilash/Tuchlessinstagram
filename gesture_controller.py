import time


class GestureController:

    def __init__(self):

        self.center_x = None
        self.center_y = None

        self.X_THRESHOLD = 0.05
        self.Y_THRESHOLD = 0.05

        self.CENTER_MARGIN = 0.02

        self.ACTION_DELAY = 0.5
        self.last_action_time = 0

        self.locked = False

        # ==========================================
        # DOUBLE GESTURE
        # ==========================================

        self.last_gesture = None
        self.last_gesture_time = 0
        self.DOUBLE_DELAY = 1.0

        # ==========================================
        # MOUTH CONTROL
        # ==========================================

        self.mouth_open = False
        self.last_mouth_time = 0

        # Minimum time between mouth actions
        self.MOUTH_DELAY = 1.5

    def detect(self, result):

        if not result.face_landmarks:
            return None

        landmarks = result.face_landmarks[0]

        # ==========================================
        # NOSE
        # ==========================================

        nose = landmarks[1]

        x = nose.x
        y = nose.y

        # ==========================================
        # CALIBRATION
        # ==========================================

        if self.center_x is None:

            self.center_x = x
            self.center_y = y

            print("Calibration Complete")

            return None

        dx = x - self.center_x
        dy = y - self.center_y

        current = time.time()

        # ==========================================
        # MOUTH DETECTION
        # ==========================================

        # Upper lip
        upper_lip = landmarks[13]

        # Lower lip
        lower_lip = landmarks[14]

        mouth_distance = abs(
            lower_lip.y - upper_lip.y
        )

        MOUTH_THRESHOLD = 0.045

        detected_mouth_open = (
            mouth_distance > MOUTH_THRESHOLD
        )

        # ------------------------------------------
        # Mouth OPEN
        # ------------------------------------------

        if detected_mouth_open:

            # Only trigger when mouth changes
            # from CLOSED -> OPEN

            if not self.mouth_open:

                if (
                    current - self.last_mouth_time
                    > self.MOUTH_DELAY
                ):

                    self.mouth_open = True
                    self.last_mouth_time = current

                    print(
                        f"MOUTH OPEN detected "
                        f"(distance={mouth_distance:.3f})"
                    )

                    return "MOUTH_OPEN"

        else:

            # Mouth is closed again
            self.mouth_open = False

        # ==========================================
        # UNLOCK HEAD GESTURE
        # ==========================================

        if (
            abs(dx) < self.CENTER_MARGIN
            and abs(dy) < self.CENTER_MARGIN
        ):

            self.locked = False

        if self.locked:
            return None

        if (
            current - self.last_action_time
            < self.ACTION_DELAY
        ):

            return None

        gesture = None

        # ==========================================
        # RIGHT
        # ==========================================

        if dx > self.X_THRESHOLD:

            gesture = "RIGHT"

        # ==========================================
        # LEFT
        # ==========================================

        elif dx < -self.X_THRESHOLD:

            gesture = "LEFT"

        # ==========================================
        # DOWN
        # ==========================================

        elif dy > self.Y_THRESHOLD:

            gesture = "DOWN"

        # ==========================================
        # UP
        # ==========================================

        elif dy < -self.Y_THRESHOLD:

            gesture = "UP"

        if gesture is None:
            return None

        self.locked = True
        self.last_action_time = current

        # ==========================================
        # DOUBLE GESTURE
        # ==========================================

        if (
            gesture == self.last_gesture
            and
            current - self.last_gesture_time
            < self.DOUBLE_DELAY
        ):

            self.last_gesture = None

            print(
                "DOUBLE GESTURE:",
                gesture
            )

            return "DOUBLE_" + gesture

        self.last_gesture = gesture
        self.last_gesture_time = current

        print(
            "GESTURE:",
            gesture
        )

        return gesture