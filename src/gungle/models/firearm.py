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


class Caliber(str, Enum):
    # Pistols
    NINE_MM = "9mm"
    FORTY_SW = ".40 S&W"
    FORTY_FIVE_ACP = ".45 ACP"
    THREE_EIGHT_SPECIAL = ".38 Special"
    THREE_FIVE_SEVEN = ".357 Magnum"
    THREE_EIGHT_AUTO = ".380 ACP"
    TWO_TWO_LR = ".22 LR"
    TEN_MM = "10mm"
    THREE_TWO_ACP = ".32 ACP"
    FOUR_FOUR_MAGNUM = ".44 Magnum"
    FIVE_SEVEN_X28 = "5.7x28mm"
    NINE_MM_MAKAROV = "9mm Makarov"
    FORTY_FOUR_SPECIAL = ".44 Special"

    # Rifles
    TWO_TWO_THREE_REM = ".223 Remington"
    FIVE_FIVE_SIX_NATO = "5.56x45mm NATO"
    THREE_OH_EIGHT_WIN = ".308 Winchester"
    SEVEN_SIX_TWO_NATO = "7.62x51mm NATO"
    THIRTY_OH_SIX = ".30-06 Springfield"
    SEVEN_SIX_TWO_X39 = "7.62x39mm"
    TWO_FOUR_THREE_WIN = ".243 Winchester"
    TWO_SEVEN_OH_WIN = ".270 Winchester"
    THREE_OH_OH_WIN_MAG = ".300 Winchester Magnum"
    THREE_OH_THREE_BRITISH = ".303 British"
    SEVEN_MM_REM_MAG = "7mm Remington Magnum"
    TWO_TWO_HORNET = ".22 Hornet"
    TWO_TWO_FOUR_VALKYRIE = ".224 Valkyrie"
    SIX_FIVE_CREEDMOOR = "6.5 Creedmoor"

    # Shotguns
    TWELVE_GAUGE = "12 Gauge"
    TWENTY_GAUGE = "20 Gauge"
    FOUR_TEN_BORE = ".410 Bore"
    SIXTEEN_GAUGE = "16 Gauge"


class ComparisonResult(str, Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIAL = "partial"


class Firearm(BaseModel):
    id: str
    name: str
    manufacturer: str
    type: FirearmType
    caliber: Caliber
    country_of_origin: str
    model_type: ModelType
    year_introduced: Optional[int] = None
    action_type: ActionType
    description: Optional[str] = None
    image_url: Optional[str] = None


class AttributeComparison(BaseModel):
    attribute: str
    guess_value: str
    correct_value: str
    result: ComparisonResult


class GuessResult(BaseModel):
    is_correct: bool
    guess_firearm: Firearm
    target_firearm: Firearm
    comparisons: List[AttributeComparison]
    remaining_guesses: int
    game_completed: bool


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
    all_guess_results: List[GuessResult] = []


class GameRevealResponse(BaseModel):
    target_firearm: Firearm
    guesses_made: List[str]
    is_won: bool
    all_guess_results: List[GuessResult]


class NameGuessRequest(BaseModel):
    firearm_name: str
