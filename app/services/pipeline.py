import cv2
import numpy as np
import base64
import logging
from typing import List
from pyzbar.pyzbar import decode
from app.models.schemas import RedactedRegion, Box, ExtractResponse
from app.services.detector import ObjectDetectorService

logger = logging.getLogger(__name__)

class ExtractionPipeline:
    def __init__(self, detector: ObjectDetectorService):
        self.detector = detector

    def process_image(self, img: np.ndarray) -> ExtractResponse:
        regions: List[RedactedRegion] = []
        
        # 1. cari qr code terlebih dahulu (paling cepat)
        self._extract_qr(img, regions)
        
        # 2. deteksi menggunakan semua model yolo yang aktif
        # proses deteksi nik, no hp, alamat, dll. kini murni 100% menggunakan model ai (tidak ada hard-coded regex)
        regions.extend(self.detector.detect(img))
        
        # 3. ubah balik ke base64 buat frontend
        _, buffer = cv2.imencode('.jpg', img)
        img_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return ExtractResponse(image_base64=img_b64, regions=regions)

    def _extract_qr(self, img: np.ndarray, regions: List[RedactedRegion]):
        try:
            for obj in decode(img):
                x, y, w, h = obj.rect
                try:
                    val = obj.data.decode('utf-8')
                    regions.append(RedactedRegion(type="qr", value=val, box=Box(x=x, y=y, width=w, height=h)))
                except UnicodeDecodeError:
                    pass
        except Exception as e:
            pass
