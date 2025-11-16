import cv2
import mediapipe as mp

def test_deterministic_output(pose_processor, test_frame):
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(test_frame, cv2.COLOR_BGR2RGB)
    )

    r1 = pose_processor.landmarker.detect(mp_image)
    r2 = pose_processor.landmarker.detect(mp_image)

    for lm1, lm2 in zip(r1.pose_landmarks[0], r2.pose_landmarks[0]):
        assert abs(lm1.x - lm2.x) < 1e-6
        assert abs(lm1.y - lm2.y) < 1e-6
