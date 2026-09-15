import cv2
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


class FaceMeshDetector:

    def __init__(self):

        options = FaceLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path="face_landmarker.task"
            ),
            running_mode=VisionRunningMode.VIDEO,
            output_facial_transformation_matrixes=True,
            output_face_blendshapes=True,
            num_faces=1
        )

        self.detector = FaceLandmarker.create_from_options(options)

    def detect(self, frame, timestamp):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        return self.detector.detect_for_video(
            image,
            timestamp
        )