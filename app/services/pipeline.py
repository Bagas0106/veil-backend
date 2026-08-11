import cv2
import numpy as np
import base64
import logging
from typing import List
from pyzbar.pyzbar import decode
from app.models.schemas import RedactedRegion, Box, ExtractResponse
from app.services.detector import ObjectDetectorService
from app.services.ocr import OCRService
from app.services.analyzer import TextAnalyzerService

logger = logging.getLogger(__name__)

class ExtractionPipeline:
    def __init__(self, detector: ObjectDetectorService, ocr: OCRService):
        self.detector = detector
        self.ocr = ocr
        self.analyzer = TextAnalyzerService()

    def process_image(self, img: np.ndarray) -> ExtractResponse:
        regions: List[RedactedRegion] = []
        
        # cari qr code dlu
        self._extract_qr(img, regions)
        regions.extend(self.detector.detect(img))
        
        # tutup bagian yg udh ketemu pake kotak item biar ocr ga double baca
        masked_img = img.copy()
        for r in regions:
            cv2.rectangle(masked_img, (r.box.x, r.box.y), (r.box.x + r.box.width, r.box.y + r.box.height), (0, 0, 0), -1)
            
        # sisa gambar baru lempar ke ocr
        ocr_results = self.ocr.extract_text(masked_img)
        for (bbox, text, prob) in ocr_results:
            sensitive_type = self.analyzer.analyze(text)
            if sensitive_type:
                x_coords = [p[0] for p in bbox]
                y_coords = [p[1] for p in bbox]
                x = int(min(x_coords))
                y = int(min(y_coords))
                w = int(max(x_coords) - x)
                h = int(max(y_coords) - y)
                regions.append(RedactedRegion(type=sensitive_type, value=text, box=Box(x=x, y=y, width=w, height=h)))
                
        # ubah balik ke base64 buat frontend
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
