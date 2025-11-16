import math
import numpy as np
import cv2
import mediapipe as mp

def compute_mpjpe(pred, gt):
    errors = []
    for p, g in zip(pred, gt):
        ex = (p.x - g["x"])
        ey = (p.y - g["y"])
        errors.append(math.sqrt(ex*ex + ey*ey))
    return sum(errors) / len(errors)


def compute_pck(pred, gt, thresh=0.02):
    correct = 0
    for p, g in zip(pred, gt):
        dist = math.sqrt((p.x - g["x"])**2 + (p.y - g["y"])**2)
        if dist < thresh:
            correct += 1
    return correct / len(pred)


def test_mpjpe(pose_processor, test_frame, ground_truth):
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(test_frame, cv2.COLOR_BGR2RGB)
    )

    result = pose_processor.landmarker.detect(mp_image)
    pred = result.pose_landmarks[0]

    mpjpe = compute_mpjpe(pred, ground_truth)
    assert mpjpe < 0.015, f"MPJPE too high: {mpjpe}"


def test_pck(pose_processor, test_frame, ground_truth):
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(test_frame, cv2.COLOR_BGR2RGB)
    )

    result = pose_processor.landmarker.detect(mp_image)
    pred = result.pose_landmarks[0]

    pck = compute_pck(pred, ground_truth)
    assert pck > 0.90, f"PCK too low: {pck}"
