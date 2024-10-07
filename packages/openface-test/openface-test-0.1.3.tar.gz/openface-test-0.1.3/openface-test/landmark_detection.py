from openface.star.demo import Alignment, GetCropMatrix, TransformPerspective, TransformPoints2D, draw_pts

class LandmarkDetector:
    def __init__(self):
        self.alignment = Alignment()

    def detect(self, face_region):
        crop_matrix = GetCropMatrix(face_region)
        aligned_face = TransformPerspective(face_region, crop_matrix)
        landmarks = TransformPoints2D(aligned_face, draw_pts(aligned_face))
        return landmarks
