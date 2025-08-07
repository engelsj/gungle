import hashlib
import uuid
from datetime import date, datetime
from typing import Dict, List, Optional

from ..models.firearm import (
    AttributeComparison,
    ComparisonResult,
    Firearm,
    GameRevealResponse,
    GameSession,
    GameStatusResponse,
    GuessResult,
    NewGameResponse,
)
from .firearm_service import firearm_service


class GameService:
    def __init__(self) -> None:
        self._sessions: Dict[str, GameSession] = {}
        self._guess_history: Dict[str, List[GuessResult]] = {}
        self._current_daily_firearm: Optional[Firearm] = None
        self._current_date: Optional[date] = None

    def start_new_game(self) -> NewGameResponse:
        target_firearm = self._get_daily_firearm()

        session_id = str(uuid.uuid4())
        game_session = GameSession(
            session_id=session_id,
            target_firearm=target_firearm,
            guesses_made=[],
            is_completed=False,
            is_won=False,
            created_at=datetime.now(),
            max_guesses=5,
        )

        self._sessions[session_id] = game_session
        self._guess_history[session_id] = []

        return NewGameResponse(
            session_id=session_id,
            firearm_image_url=target_firearm.image_url,
            max_guesses=game_session.max_guesses,
        )

    def make_guess_by_name(self, session_id: str, firearm_name: str) -> GuessResult:
        session = self._get_session(session_id)
        if not session:
            raise ValueError("Game session not found")

        if session.is_completed:
            raise ValueError("Game already completed")

        if len(session.guesses_made) >= session.max_guesses:
            raise ValueError("Maximum guesses reached")

        guess_firearm = self._find_firearm_by_name(firearm_name)
        if not guess_firearm:
            raise ValueError(f"Firearm '{firearm_name}' not found")

        session.guesses_made.append(guess_firearm.name)

        is_correct = guess_firearm.name.lower() == session.target_firearm.name.lower()

        comparisons = self._compare_firearms(guess_firearm, session.target_firearm)

        remaining_guesses = session.max_guesses - len(session.guesses_made)

        if is_correct:
            session.is_completed = True
            session.is_won = True
        elif remaining_guesses == 0:
            session.is_completed = True
            session.is_won = False

        guess_result = GuessResult(
            is_correct=is_correct,
            guess_firearm=guess_firearm,
            target_firearm=(
                session.target_firearm
                if session.is_completed
                else session.target_firearm
            ),
            comparisons=comparisons,
            remaining_guesses=remaining_guesses,
            game_completed=session.is_completed,
        )

        self._guess_history[session_id].append(guess_result)

        return guess_result

    def get_available_firearm_names(self) -> List[str]:
        return [firearm.name for firearm in firearm_service.get_all_firearms()]

    def get_game_status(self, session_id: str) -> Optional[GameStatusResponse]:
        session = self._get_session(session_id)
        if not session:
            return None

        return GameStatusResponse(
            session_id=session_id,
            target_firearm_name=(
                session.target_firearm.name if session.is_completed else None
            ),
            guesses_made=len(session.guesses_made),
            max_guesses=session.max_guesses,
            is_completed=session.is_completed,
            is_won=session.is_won,
            target_firearm=(session.target_firearm if session.is_completed else None),
            all_guess_results=self._guess_history.get(session_id, []),
        )

    def reveal_answer(self, session_id: str) -> Optional[GameRevealResponse]:
        session = self._get_session(session_id)
        if not session:
            return None

        if not session.is_completed:
            raise ValueError("Game not yet completed")

        return GameRevealResponse(
            target_firearm=session.target_firearm,
            guesses_made=session.guesses_made,
            is_won=session.is_won,
            all_guess_results=self._guess_history.get(session_id, []),
        )

    def get_all_sessions(self) -> List[GameSession]:
        return list(self._sessions.values())

    def _get_session(self, session_id: str) -> Optional[GameSession]:
        return self._sessions.get(session_id)

    def _find_firearm_by_name(self, name: str) -> Optional[Firearm]:
        all_firearms = firearm_service.get_all_firearms()
        for firearm in all_firearms:
            if firearm.name.lower() == name.lower():
                return firearm
        return None

    def _compare_firearms(
        self, guess_firearm: Firearm, target_firearm: Firearm
    ) -> List[AttributeComparison]:
        comparisons = []

        manufacturer_result = (
            ComparisonResult.CORRECT
            if guess_firearm.manufacturer == target_firearm.manufacturer
            else ComparisonResult.INCORRECT
        )
        comparisons.append(
            AttributeComparison(
                attribute="manufacturer",
                guess_value=guess_firearm.manufacturer,
                correct_value=target_firearm.manufacturer,
                result=manufacturer_result,
            )
        )

        type_result = (
            ComparisonResult.CORRECT
            if guess_firearm.type == target_firearm.type
            else ComparisonResult.INCORRECT
        )
        comparisons.append(
            AttributeComparison(
                attribute="type",
                guess_value=guess_firearm.type.value,
                correct_value=target_firearm.type.value,
                result=type_result,
            )
        )

        caliber_result = (
            ComparisonResult.CORRECT
            if guess_firearm.caliber == target_firearm.caliber
            else ComparisonResult.INCORRECT
        )
        comparisons.append(
            AttributeComparison(
                attribute="caliber",
                guess_value=guess_firearm.caliber,
                correct_value=target_firearm.caliber,
                result=caliber_result,
            )
        )

        action_result = (
            ComparisonResult.CORRECT
            if guess_firearm.action_type == target_firearm.action_type
            else ComparisonResult.INCORRECT
        )
        comparisons.append(
            AttributeComparison(
                attribute="action_type",
                guess_value=guess_firearm.action_type,
                correct_value=target_firearm.action_type,
                result=action_result,
            )
        )

        country_result = (
            ComparisonResult.CORRECT
            if (guess_firearm.country_of_origin == target_firearm.country_of_origin)
            else ComparisonResult.INCORRECT
        )
        comparisons.append(
            AttributeComparison(
                attribute="country_of_origin",
                guess_value=guess_firearm.country_of_origin,
                correct_value=target_firearm.country_of_origin,
                result=country_result,
            )
        )

        adoption_result = (
            ComparisonResult.CORRECT
            if guess_firearm.model_type == target_firearm.model_type
            else ComparisonResult.INCORRECT
        )
        comparisons.append(
            AttributeComparison(
                attribute="adoption_status",
                guess_value=guess_firearm.model_type.value,
                correct_value=target_firearm.model_type.value,
                result=adoption_result,
            )
        )

        if guess_firearm.year_introduced and target_firearm.year_introduced:
            year_diff = abs(
                guess_firearm.year_introduced - target_firearm.year_introduced
            )
            if year_diff == 0:
                year_result = ComparisonResult.CORRECT
            else:
                year_result = ComparisonResult.INCORRECT
        else:
            year_result = ComparisonResult.INCORRECT

        comparisons.append(
            AttributeComparison(
                attribute="year_introduced",
                guess_value=str(guess_firearm.year_introduced or "Unknown"),
                correct_value=str(target_firearm.year_introduced or "Unknown"),
                result=year_result,
            )
        )

        return comparisons

    def _get_daily_firearm(self) -> Firearm:
        today = date.today()

        if self._current_date != today or self._current_daily_firearm is None:
            self._current_date = today
            self._current_daily_firearm = self._select_daily_firearm(today)

        return self._current_daily_firearm

    def _select_daily_firearm(self, target_date: date) -> Firearm:
        available_firearms = firearm_service.get_all_firearms()
        if not available_firearms:
            raise ValueError("No firearms available for game")

        date_string = target_date.isoformat()
        seed_hash = hashlib.sha256(date_string.encode()).hexdigest()

        seed_int = int(seed_hash[:8], 16)  # Use first 8 hex chars as integer
        firearm_index = seed_int % len(available_firearms)

        return available_firearms[firearm_index]

    def get_daily_firearm(self) -> Firearm:
        return self._get_daily_firearm()


game_service = GameService()
