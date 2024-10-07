import torch
from model.MLT import MLT  # Import the multitasking model from your code

class MultitaskModel:
    def __init__(self, device='cpu'):
        # Load the shared multitasking model
        self.device = device
        self.model = MLT()
        self.model.load_state_dict(torch.load("./weights/stage2_epoch_7_loss_1.1606_acc_0.5589.pth", map_location=torch.device(device)))
        self.model = self.model.to(self.device)
        self.model.eval()  # Set to evaluation mode

    def predict(self, face_region):
        # Convert the face region to a tensor
        face_tensor = self.preprocess(face_region)

        # Make prediction using the multitasking model
        with torch.no_grad():
            emotion_output, gaze_output, au_output = self.model(face_tensor)

        # Parse the outputs into action units, emotions, and gaze
        action_units = au_output.tolist()
        emotions = emotion_output.argmax().item()  # Assuming emotions are output as logits
        gaze = gaze_output.tolist()

        return action_units, emotions, gaze

    def preprocess(self, face_region):
        # Convert face_region to tensor
        face_tensor = torch.from_numpy(face_region).float().permute(2, 0, 1).unsqueeze(0)  # (C, H, W) format
        face_tensor /= 255.0  # Normalize to [0, 1]
        face_tensor = face_tensor.to(self.device)
        return face_tensor
