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
    PRECISION_RIFLE = "sniper"
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
    country_of_origin: str
    adoption_status: AdoptionStatus
    year_introduced: Optional[int] = None
    actionType: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class AttributeComparison(BaseModel):
    attribute: str
    guess_value: str
    correct_value: str
    result: ComparisonResult


class GuessResult(BaseModel):
    is_correct: bool
    guess_firearm: Firearm  # The firearm that was guessed
    target_firearm: Firearm  # The correct answer (only shown if game complete)
    comparisons: List[AttributeComparison]
    remaining_guesses: int
    game_completed: bool


class GameSession(BaseModel):
    session_id: str
    target_firearm: Firearm
    guesses_made: List[str]  # List of firearm names that were guessed
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
    target_firearm_name: Optional[str]  # Only shown when game is complete
    guesses_made: int
    max_guesses: int
    is_completed: bool
    is_won: bool
    target_firearm: Optional[Firearm] = None  # Only shown when game is complete
    all_guess_results: List[GuessResult] = []  # History of all guesses made


class GameRevealResponse(BaseModel):
    target_firearm: Firearm
    guesses_made: List[str]
    is_won: bool
    all_guess_results: List[GuessResult]


class NameGuessRequest(BaseModel):
    firearm_name: str
