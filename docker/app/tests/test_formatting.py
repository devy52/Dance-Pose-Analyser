import cv2
import numpy as np
import mediapipe as mp

def test_landmark_count(pose_processor, test_frame):
    result = pose_processor.landmarker.detect(
        mp.Image(image_format=mp.ImageFormat.SRGB,
                 data=cv2.cvtColor(test_frame, cv2.COLOR_BGR2RGB))
    )
    assert result.pose_landmarks, "No landmarks detected!"
    assert len(result.pose_landmarks[0]) == 33


def test_landmark_fields(pose_processor, test_frame):
    result = pose_processor.landmarker.detect(
        mp.Image(image_format=mp.ImageFormat.SRGB,
                 data=cv2.cvtColor(test_frame, cv2.COLOR_BGR2RGB))
    )
    lm = result.pose_landmarks[0][0]
    assert hasattr(lm, "x")
    assert hasattr(lm, "y")
    assert hasattr(lm, "z")
    assert hasattr(lm, "presence")
    assert hasattr(lm, "visibility")


def test_coordinate_range(pose_processor, test_frame):
    result = pose_processor.landmarker.detect(
        mp.Image(image_format=mp.ImageFormat.SRGB,
                 data=cv2.cvtColor(test_frame, cv2.COLOR_BGR2RGB))
    )
    for lm in result.pose_landmarks[0]:
        assert 0 <= lm.x <= 1
        assert 0 <= lm.y <= 1


def test_segmentation_mask_shape(pose_processor, test_frame):
    result = pose_processor.landmarker.detect(
        mp.Image(image_format=mp.ImageFormat.SRGB,
                 data=cv2.cvtColor(test_frame, cv2.COLOR_BGR2RGB))
    )

    mask = result.segmentation_masks[0].numpy_view()
    h, w, _ = test_frame.shape
    assert mask.shape == (h, w)
