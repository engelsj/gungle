from typing import Dict, List

from fastapi import APIRouter, HTTPException

from ....models.firearm import Firearm
from ....services.firearm_service import firearm_service

router = APIRouter()


@router.get("/", response_model=List[Firearm])
async def get_all_firearms() -> List[Firearm]:
    return firearm_service.get_all_firearms()


@router.get("/{firearm_id}", response_model=Firearm)
async def get_firearm(firearm_id: str) -> Firearm:
    firearm = firearm_service.get_firearm_by_id(firearm_id)
    if not firearm:
        raise HTTPException(status_code=404, detail="Firearm not found")
    return firearm


@router.post("/", response_model=Firearm)
async def add_firearm(firearm: Firearm) -> Firearm:
    if not firearm_service.add_firearm(firearm):
        raise HTTPException(status_code=400, detail="Firearm already exists")
    return firearm


@router.put("/{firearm_id}", response_model=Firearm)
async def update_firearm(firearm_id: str, firearm: Firearm) -> Firearm:
    if not firearm_service.update_firearm(firearm_id, firearm):
        raise HTTPException(status_code=404, detail="Firearm not found")
    return firearm


@router.delete("/{firearm_id}")
async def delete_firearm(firearm_id: str) -> Dict[str, str]:
    if not firearm_service.delete_firearm(firearm_id):
        raise HTTPException(status_code=404, detail="Firearm not found")
    return {"message": "Firearm deleted successfully"}
