from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from ....models.firearm import (
    GameRevealResponse,
    GameSession,
    GameStatusResponse,
    GuessResult,
    NameGuessRequest,
    NewGameResponse,
)
from ....services.game_service import game_service

router = APIRouter()


@router.post("/new", response_model=NewGameResponse)
async def start_new_game() -> NewGameResponse:
    try:
        return game_service.start_new_game()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/firearm-names", response_model=List[str])
async def get_firearm_names() -> List[str]:
    return game_service.get_available_firearm_names()


@router.post("/{session_id}/guess", response_model=GuessResult)
async def make_guess_by_name(
    session_id: str, guess_request: NameGuessRequest
) -> GuessResult:
    try:
        return game_service.make_guess_by_name(session_id, guess_request.firearm_name)
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))


@router.get("/{session_id}/status", response_model=GameStatusResponse)
async def get_game_status(session_id: str) -> GameStatusResponse:
    status = game_service.get_game_status(session_id)
    if not status:
        raise HTTPException(status_code=404, detail="Game session not found")
    return status


@router.get("/{session_id}/reveal", response_model=GameRevealResponse)
async def reveal_answer(session_id: str) -> GameRevealResponse:
    try:
        result = game_service.reveal_answer(session_id)
        if not result:
            raise HTTPException(status_code=404, detail="Game session not found")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/admin/sessions", response_model=List[GameSession])
async def get_all_sessions() -> List[GameSession]:
    return game_service.get_all_sessions()


@router.get("/daily-firearm")
async def get_daily_firearm() -> Dict[str, Any]:
    try:
        daily_firearm = game_service.get_daily_firearm()
        return {"firearm": daily_firearm, "message": "Today's firearm"}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
