from fastapi import APIRouter

from .endpoints import firearms, game

api_router = APIRouter()

api_router.include_router(game.router, prefix="/game", tags=["game"])
api_router.include_router(firearms.router, prefix="/firearms", tags=["firearms"])
