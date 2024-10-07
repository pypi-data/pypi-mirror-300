import os
import sys
import torch
import cv2
import numpy as np
from openface.pytorch_retinaface.models.retinaface import RetinaFace
from openface.pytorch_retinaface.layers.functions.prior_box import PriorBox
from openface.pytorch_retinaface.utils.box_utils import decode, decode_landm
from openface.pytorch_retinaface.utils.nms.py_cpu_nms import py_cpu_nms
from openface.pytorch_retinaface.data import cfg_mnet, cfg_re50
from openface.pytorch_retinaface.detect import load_model
from openface.star.demo import GetCropMatrix, TransformPerspective, TransformPoints2D, Alignment, draw_pts
from openface.multitask_model import MultitaskModel

class FaceFeatureExtractor:
    def __init__(self, device='cpu'):
        # Initialize the models
        self.device = device
        self.face_detector = load_model(RetinaFace(cfg=cfg_mnet))  # Face detection using RetinaFace
        self.face_detector = self.face_detector.to(self.device)
        self.landmark_detector = Alignment()  # Facial landmarks detection using STAR
        self.multitask_model = MultitaskModel(self.device)  # Shared multitasking model for AUs, emotions, and gaze

    def extract_features(self, image):
        # Detect face in the image
        faces = self.face_detector.detect_faces(image)
        if len(faces) == 0:
            print("No face detected")
            return None

        face = faces[0]  # Considering only the first detected face for simplicity
        x1, y1, x2, y2 = face["box"]
        face_region = image[y1:y2, x1:x2]

        # Extract landmarks
        crop_matrix = GetCropMatrix(face_region)
        aligned_face = TransformPerspective(face_region, crop_matrix)
        landmarks = TransformPoints2D(aligned_face, draw_pts(aligned_face))

        # Extract action units, emotions, and gaze using the multitasking model
        action_units, emotions, gaze = self.multitask_model.predict(face_region)

        return {
            "landmarks": landmarks,
            "action_units": action_units,
            "emotions": emotions,
            "gaze": gaze
        }
