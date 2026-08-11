from fastapi import APIRouter, UploadFile, File, HTTPException, Request
import cv2
import numpy as np
import io
import logging
from PIL import Image

logger = logging.getLogger(__name__)
router = APIRouter()

SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp', '.jfif', '.bmp', '.tiff', '.tif', '.avif')

@router.post("/extract")
async def extract_data(request: Request, file: UploadFile = File(...)):
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()
    
    logger.info(f"Incoming extract request: filename='{file.filename}', content_type='{file.content_type}'")
    
    # Validasi tipe file / extension
    is_valid_ext = any(filename.endswith(ext) for ext in SUPPORTED_EXTENSIONS)
    is_valid_type = content_type.startswith("image/")
    
    if not (is_valid_ext or is_valid_type):
        logger.warning(f"Rejected invalid file format: filename='{file.filename}', content_type='{file.content_type}'")
        raise HTTPException(400, f"Format file tidak valid ({file.filename}). Harap unggah gambar (PNG, JPG, WEBP, dll).")
        
    contents = await file.read()
    if not contents or len(contents) == 0:
        logger.warning("Empty file payload received.")
        raise HTTPException(400, "File yang diunggah kosong.")
    
    # 1. Coba decode pake OpenCV
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # 2. Fallback pake PIL kalau OpenCV gagal decode (misal format webp / format tertentu)
    if img is None:
        try:
            pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
            img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            logger.error(f"Failed to decode image with both OpenCV and PIL: {e}")
            raise HTTPException(400, "Gagal memproses/decode gambar. Pastikan file gambar tidak rusak.")
        
    pipeline = getattr(request.state, "pipeline", None)
    if pipeline is None:
        logger.error("Extraction pipeline is not initialized.")
        raise HTTPException(503, "Layanan AI sedang memuat atau belum siap. Silakan coba beberapa saat lagi.")
        
    logger.info(f"Image decoded successfully (shape: {img.shape}). Running pipeline...")
    return pipeline.process_image(img)

