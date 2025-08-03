from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class FirearmType(str, Enum):
    RIFLE = "Rifle"
    SMG = "Sub Machine Gun"
    PISTOL = "Handgun"
    SHOTGUN = "Shotgun"
    LMG = "Light Machine Gun"
    PRECISION_RIFLE = "Precision Rifle"
    CARBINE = "Carbine"


class ModelType(str, Enum):
    PROTOTYPE = "Prototype"
    CIVILIAN = "Civilian"
    MILITARY = "Military"
    POLICE = "Police"


class ActionType(str, Enum):
    BREECH_BLOCK = "Breech Block"
    DROPPING_BLOCK = "Dropping Block"
    PIVOTING_BLOCK = "Pivoting Block"
    FALLING_BLOCK = "Falling Block"
    ROLLING_BLOCK = "Rolling Block"
    HINGED_BLOCK = "Hinged Block"
    BREAK_ACTION = "Break-action"
    ROTATING_BOLT_ACTION = "Rotating Bolt-action"
    STRAIGHT_PULL_BOLT_ACTION = "Straight-pull Bolt-action"
    ECCENTRIC_SCREW_ACTION = "Eccentric Screw Action"
    SINGLE_ACTION_REVOLVER = "Single Action Revolver"
    DOUBLE_ACTION_REVOLVER = "Double Action Revovler"
    PUMP_ACTION = "Pump-action"
    LEVER_ACTION = "Lever-action"
    SIMPLE_BLOWBACK = "Simple Blowback"
    BLOW_FORWARD = "Blow-forward"
    SHOT_RECOIL = "Short-recoil"
    LONG_RECOIL = "Long-recoil"
    INERTIA = "Inertia"
    SHORT_STROKE_GAS_PISTON = "Short-stroke Gas Piston"
    LONG_STROKE_GAS_PISTON = "Long-stroke Gas Piston"
    DIRECT_IMPINGEMENT = "Direct Impingement"
    GAS_TRAP = "Gas Trap"
    MATCHLOCK = "Matchlock"
    FLINTLOCK = "Flintlock"
    WHEELLOCK = "Wheellock"
    CAPLOCK = "Caplock"
    TEST_ACTION = "Test Action"


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
    model_type: ModelType
    year_introduced: Optional[int] = None
    actionType: ActionType
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
