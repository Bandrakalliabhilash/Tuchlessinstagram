import cv2
import time
import requests

from face_mesh_detector import FaceMeshDetector
from gesture_controller import GestureController

# ==========================================
# Camera Settings
# ==========================================

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# ==========================================
# Send Gesture to Flask Backend
# ==========================================

def send_gesture(name):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/gesture/send",
            json={"gesture": name},
            timeout=1
        )

        if response.status_code == 200:
            print(f"Gesture Sent : {name}")

    except requests.exceptions.RequestException:
        print("Backend Offline")

# ==========================================
# Camera
# ==========================================

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

if not camera.isOpened():
    print("Cannot open webcam.")
    exit()

# ==========================================
# MediaPipe
# ==========================================

detector = FaceMeshDetector()
controller = GestureController()

print("Look straight at the camera for one second...")

# ==========================================
# Main Loop
# ==========================================

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    timestamp = int(time.time() * 1000)

    result = detector.detect(frame, timestamp)

    # ----------------------------------
    # Face Detected
    # ----------------------------------

    if result.face_landmarks:

        # Optional:
        # if result.facial_transformation_matrixes:
        #     print("Head Pose Matrix Found")

        landmarks = result.face_landmarks[0]

        h, w, _ = frame.shape

        # Draw all landmarks
        for point in landmarks:

            px = int(point.x * w)
            py = int(point.y * h)

            cv2.circle(
                frame,
                (px, py),
                1,
                (0, 255, 0),
                -1
            )

        # Draw Nose Tip

        nose = landmarks[1]

        nose_x = int(nose.x * w)
        nose_y = int(nose.y * h)

        cv2.circle(
            frame,
            (nose_x, nose_y),
            6,
            (0, 0, 255),
            -1
        )

        # Detect Gesture

        gesture = controller.detect(result)

        if gesture:

            print(gesture)

            send_gesture(gesture)

            cv2.putText(
                frame,
                gesture,
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

        # Status

        cv2.putText(
            frame,
            "TouchGram AI Ready",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "No Face Detected",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    cv2.imshow("TouchGram AI", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()