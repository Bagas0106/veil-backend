import uvicorn

if __name__ == "__main__":
    # jalanin server di port 8000
    # added reload_includes so that uvicorn auto-restarts when you replace .onnx files
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True, 
        reload_includes=["*.onnx"]
    )
