import easyocr
import cv2
import logging
import numpy as np
from typing import List, Tuple

import torch

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        self.reader = None

    def load_model(self):
        logger.info("Loading EasyOCR model...")
        use_gpu = False
        try:
            use_gpu = torch.cuda.is_available()
            self.reader = easyocr.Reader(['id', 'en'], gpu=use_gpu)
            logger.info(f"EasyOCR loaded successfully (GPU={use_gpu}).")
        except Exception as e:
            logger.warning(f"EasyOCR GPU load failed ({e}), falling back to CPU...")
            try:
                self.reader = easyocr.Reader(['id', 'en'], gpu=False)
                logger.info("EasyOCR loaded successfully on CPU.")
            except Exception as err_cpu:
                logger.error(f"Failed to load EasyOCR on CPU: {err_cpu}")

    def unload_model(self):
        self.reader = None

    def preprocess_image(self, img: np.ndarray) -> np.ndarray:
        # pake clahe buat perjelas gambar sblm masuk ocr
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        return clahe.apply(gray)

    def extract_text(self, img: np.ndarray) -> List[Tuple[List[List[int]], str, float]]:
        if self.reader is None:
            return []
        enhanced_img = self.preprocess_image(img)
        return self.reader.readtext(enhanced_img)
