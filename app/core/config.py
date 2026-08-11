from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Veil Privacy Detector Backend"
    API_V1_STR: str = "/api"
    
    # path buat model yolo (jangan diubah klo ga error)
    WEIGHTS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "weights")
    FACE_MODEL_PATH: str = os.path.join(WEIGHTS_DIR, "face_model.onnx")
    PLATE_MODEL_PATH: str = os.path.join(WEIGHTS_DIR, "plate_model.onnx")
    RECEIPT_MODEL_PATH: str = os.path.join(WEIGHTS_DIR, "receipt_model.onnx")
    
    # batas threshold biar ga false positive mulu pas demo
    FACE_CONF_THRESHOLD: float = 0.5
    PLATE_CONF_THRESHOLD: float = 0.45
    RECEIPT_CONF_THRESHOLD: float = 0.45

settings = Settings()
