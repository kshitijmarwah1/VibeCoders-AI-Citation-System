"""
GPU detection and optimization utilities.
"""
import logging
import torch

logger = logging.getLogger(__name__)

def check_gpu_availability() -> bool:
    """Check if GPU (CUDA) is available."""
    try:
        return torch.cuda.is_available()
    except Exception:
        return False

def get_device() -> str:
    """Get the best available device (cuda or cpu)."""
    if check_gpu_availability():
        device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
        logger.info(f"Using GPU: {device_name}")
        return "cuda"
    else:
        logger.info("Using CPU (GPU not available)")
        return "cpu"

def optimize_model_for_device(model, device: str = None):
    """Move model to appropriate device for faster inference."""
    if device is None:
        device = get_device()
    
    if device == "cuda" and torch.cuda.is_available():
        try:
            model = model.to(device)
            logger.info("Model moved to GPU for faster inference")
        except Exception as e:
            logger.warning(f"Failed to move model to GPU: {e}")
    
    return model

