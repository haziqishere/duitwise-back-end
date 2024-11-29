from transformers import DonutProcessor, VisionEncoderDecoderModel
from app.core.config import settings
import torch
from huggingface_hub import login
import logging

logger = logging.getLogger(__name__)

class MLModels:
    def __init__(self):
        self.processor = None
        self.model = None
        self.device = self._get_optimal_device()

    def _get_optimal_device(self) -> str:
        if torch.cuda.is_available():
            logger.info("Using CUDA device for model inference")
            return "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            try:
                _ = torch.zeros(1).to('mps')
                logger.info("Using MPS device for model inference")
                return "mps"
            except Exception as e:
                logger.warning(f"MPS available but failed to initialize: {e}")
                logger.info("Falling back to CPU")
                return "cpu"
        else:
            logger.info("No GPU available. Using CPU for model inference")
            return "cpu"

    def load_models(self):
        try:
            # Login to Hugging Face
            if settings.HUGGINGFACE_TOKEN:
                login(settings.HUGGINGFACE_TOKEN)
                logger.info("Successfully logged in to Hugging Face")
            else:
                logger.warning("No Hugging Face token provided")

            self.processor = DonutProcessor.from_pretrained(settings.MODEL_PATH)
            self.model = VisionEncoderDecoderModel.from_pretrained(settings.MODEL_PATH)
            
            self.model.to(self.device)
            
            logger.info(f"Models loaded successfully on {self.device}")
            return self.processor, self.model
            
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            raise RuntimeError(f"Model initialization failed: {str(e)}")

ml_models = MLModels()