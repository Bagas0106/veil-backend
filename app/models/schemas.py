from pydantic import BaseModel
from typing import List, Optional

# bentuk box buat kordinat
class Box(BaseModel):
    x: int
    y: int
    width: int
    height: int

# balikan dr ai nya
class RedactedRegion(BaseModel):
    type: str
    value: str
    box: Box

class ExtractResponse(BaseModel):
    image_base64: str
    regions: List[RedactedRegion]
