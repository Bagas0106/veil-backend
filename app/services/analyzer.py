import re
from typing import Optional

class TextAnalyzerService:
    @staticmethod
    def analyze(text: str) -> Optional[str]:
        # bersihin teks dlu dr spasi dll
        clean_text = text.replace(" ", "").upper()
        alpha_num = re.sub(r'[^A-Z0-9]', '', clean_text)
        
        # cek format ktp indo 16 digit
        if re.search(r"\d{16}", alpha_num):
            return "ktp"
        
        # cek plat nomer indo
        if re.search(r"[A-Z]{1,2}\d{1,4}[A-Z]{1,3}", alpha_num):
            return "plate"
            
        # cek kata kunci alamat rt rw
        address_keywords = ["JALAN", "JL.", "RT", "RW", "KECAMATAN", "KABUPATEN", "KELURAHAN", "PROVINSI", "KOTA"]
        if any(keyword in text.upper() for keyword in address_keywords):
            return "address"
            
        # cek nomer wa
        if re.search(r"(08|62)\d{8,11}", alpha_num):
            return "phone"

        return None
