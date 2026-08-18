# Veil Backend API

## Deskripsi Singkat
Veil Backend ini adalah layanan API (*Application Programming Interface*) yang nge-handle fitur ekstraksi data berbasis AI. Sistem ini dibuat buat nerima input gambar, terus memprosesnya pakai model *Object Detection* dan OCR (*Optical Character Recognition*) buat mengekstrak teks atau mendeteksi objek secara otomatis. Layanan ini jalan di belakang layar untuk dukung semua fitur di aplikasi web Veil.

## Teknologi (Stack) yang Digunakan
Backend ini dibangun pakai Python dan beberapa *library*, yaitu:
- **FastAPI**: Framework web utama buat bikin REST API.
- **Uvicorn**: Web server ASGI buat ngejalanin aplikasi FastAPInya.
- **Ultralytics (YOLO)**: Dipake buat mendeteksi objek yang ada di gambar.
- **ONNX Runtime**: Engine *inference* biar model AI-nya bisa jalan lebih ngebut.
- **EasyOCR**: Dipakai buat ngebaca dan ngekstrak teks dari gambar.
- **PyZbar**: Buat nge-scan dan baca *Barcode* atau *QR Code*.
- **OpenCV & NumPy**: *Library* standar buat *image processing* dan manipulasi array/matriks.

## Cara Menjalankan Backend (Lokal)
Ikuti langkah-langkah ini kalau mau ngejalanin server backend-nya di komputer lokal:

1. **Pastikan Python udah terinstall** (Disarankan pakai Python 3.9 ke atas).
2. Buka terminal atau command prompt, terus masuk ke folder `veil-backend`.
3. (Opsional tapi sangat disarankan) **Bikin dan aktifin *Virtual Environment***:
   ```bash
   # Bikin virtual environment
   python -m venv venv

   # Aktifin venv (Windows)
   venv\Scripts\activate

   # Aktifin venv (Mac/Linux)
   source venv/bin/activate
   ```
4. **Install semua *library* / *dependencies*** yang dibutuhin:
   ```bash
   pip install -r requirements.txt
   ```
5. **Jalanin server backend-nya**:
   ```bash
   python run.py
   ```
6. Backend bakal jalan di port `8000`, bisa cek dan tes APInya lewat dokumentasi Swagger UI di browser:
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

## Informasi Akun Demo

Tidak ada fitur login, sehingga tidak ada akun demo.