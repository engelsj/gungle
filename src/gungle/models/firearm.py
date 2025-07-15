from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class FirearmType(str, Enum):
    RIFLE = "rifle"
    SMG = "smg"
    PISTOL = "pistol"
    SHOTGUN = "shotgun"
    LMG = "lmg"
    SNIPER = "sniper"
    CARBINE = "carbine"


class AdoptionStatus(str, Enum):
    PROTOTYPE = "prototype"
    CIVILIAN = "civilian"
    MILITARY = "military"
    POLICE = "police"
    BOTH = "both"  # civilian and military


class ComparisonResult(str, Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIAL = "partial"


class Firearm(BaseModel):
    id: str
    name: str
    manufacturer: str
    type: FirearmType
    caliber: str
    actionType: str
    country_of_origin: str
    adoption_status: AdoptionStatus
    year_introduced: Optional[int] = None
    image_url: Optional[str] = None


class GuessComparison(BaseModel):
    attribute: str
    guess_value: str
    correct_value: str
    result: ComparisonResult


class GuessResult(BaseModel):
    is_correct: bool
    comparisons: List[GuessComparison]
    remaining_guesses: int


class GameSession(BaseModel):
    session_id: str
    target_firearm: Firearm
    guesses_made: List[str]
    is_completed: bool
    is_won: bool
    created_at: datetime
    max_guesses: int = 5


class NewGameResponse(BaseModel):
    session_id: str
    firearm_image_url: Optional[str]
    max_guesses: int


class GameStatusResponse(BaseModel):
    session_id: str
    target_firearm_name: Optional[str]
    guesses_made: int
    max_guesses: int
    is_completed: bool
    is_won: bool
    target_firearm: Optional[Firearm] = None


class GameRevealResponse(BaseModel):
    target_firearm: Firearm
    guesses_made: List[str]
    is_won: bool
