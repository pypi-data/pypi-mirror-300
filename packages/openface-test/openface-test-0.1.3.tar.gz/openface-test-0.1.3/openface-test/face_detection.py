import torch
from openface.pytorch_retinaface.models.retinaface import RetinaFace
from openface.pytorch_retinaface.detect import load_model
from openface.pytorch_retinaface.data import cfg_mnet

class FaceDetector:
    def __init__(self, device='cpu'):
        self.device = device
        self.model = load_model(RetinaFace(cfg=cfg_mnet))
        self.model = self.model.to(self.device)

    def detect(self, image):
        faces = self.model.detect_faces(image)
        return faces[0] if len(faces) > 0 else None
