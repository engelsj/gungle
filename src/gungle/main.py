import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .api.v1.api import api_router
from .config import settings
from .database import create_tables

create_tables()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Gungle Game Backend API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/images", exist_ok=True)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GameInfo(BaseModel):
    max_guesses: int
    description: str


class RootResponse(BaseModel):
    message: str
    version: str
    docs_url: str
    game_info: GameInfo


class HealthResponse(BaseModel):
    status: str
    debug: bool
    upload_dir: str


os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/images", exist_ok=True)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    return RootResponse(
        message="Gungle API",
        version="1.0.0",
        docs_url="/docs",
        game_info=GameInfo(
            max_guesses=settings.MAX_GUESSES,
            description="A Wordle-style game for historical firearms",
        ),
    )


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy", debug=settings.DEBUG, upload_dir=settings.UPLOAD_DIR
    )
