from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.api import extract
from app.services.detector import ObjectDetectorService
from app.services.pipeline import ExtractionPipeline

# setup logging biar gampang debug klo error
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

detector_service = ObjectDetectorService()
pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pipeline
    logger.info("Starting up AI Services (Loading ONNX engines)...")
    detector_service.load_models()
    pipeline = ExtractionPipeline(detector_service)
    yield
    logger.info("Shutting down AI Services...")
    detector_service.unload_models()

app = FastAPI(title=settings.PROJECT_NAME, version="3.0-Competition-Edition", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://veil-frontend-olive.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_pipeline_to_request(request: Request, call_next):
    # masukin pipeline ke state biar bisa diakses dr route mana aja
    request.state.pipeline = pipeline
    return await call_next(request)

app.include_router(extract.router, prefix=settings.API_V1_STR, tags=["extraction"])

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Competition Backend Online"}
