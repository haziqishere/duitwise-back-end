from transformers import DonutProcessor, VisionEncoderDecoderModel
from core.config import settings
import torch

class MLModels:
    def __init__(self):
        self.processor = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_models(self):
        self.processor = DonutProcessor.from_pretrained(settings.MODEL_PATH)
        self.model = VisionEncoderDecoderModel.from_pretrained(settings.MODEL_PATH)
        self.model.to(self.device)
        return self.processor, self.model

ml_models = MLModels()