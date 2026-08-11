from ultralytics import YOLO
import logging
from typing import List
from app.core.config import settings
from app.models.schemas import RedactedRegion, Box
import numpy as np
import os

logger = logging.getLogger(__name__)

class ObjectDetectorService:
    def __init__(self):
        self.models = {}

    def load_models(self):
        logger.info("Initializing YOLO Models (ONNX format)...")
        # load model yolo klo ada filenya
        if os.path.exists(settings.FACE_MODEL_PATH):
            self.models["face"] = YOLO(settings.FACE_MODEL_PATH, task="detect")
        if os.path.exists(settings.PLATE_MODEL_PATH):
            self.models["plate"] = YOLO(settings.PLATE_MODEL_PATH, task="detect")
        if os.path.exists(settings.RECEIPT_MODEL_PATH):
            self.models["receipt"] = YOLO(settings.RECEIPT_MODEL_PATH, task="detect")
        logger.info(f"Loaded {len(self.models)} models successfully.")

    def unload_models(self):
        self.models.clear()

    def detect(self, img: np.ndarray) -> List[RedactedRegion]:
        regions = []
        yolo_tasks = [
            ("face", "face", settings.FACE_CONF_THRESHOLD),
            ("plate", "plate", settings.PLATE_CONF_THRESHOLD),
            ("receipt", "receipt", settings.RECEIPT_CONF_THRESHOLD)
        ]
        
        for model_key, region_type, conf_threshold in yolo_tasks:
            if model_key not in self.models:
                continue
            try:
                results = self.models[model_key](img, verbose=False, imgsz=640, conf=conf_threshold, iou=0.45)
                if len(results) > 0:
                    for box in results[0].boxes:
                        conf = float(box.conf[0].item())
                        if conf >= conf_threshold:
                            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                            w, h = x2 - x1, y2 - y1
                            if w > 0 and h > 0:
                                regions.append(
                                    RedactedRegion(
                                        type=region_type,
                                        value=f"{region_type.capitalize()} Detected ({conf:.2f})",
                                        box=Box(x=x1, y=y1, width=w, height=h)
                                    )
                                )
            except Exception as e:
                logger.error(f"Error during {model_key} detection: {e}", exc_info=True)
                
        return regions
