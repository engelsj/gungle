import random
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from ..models.firearm import (
    ComparisonResult,
    Firearm,
    GameRevealResponse,
    GameSession,
    GameStatusResponse,
    GuessComparison,
    GuessResult,
    NewGameResponse,
)
from .firearm_service import firearm_service


class GameService:
    def __init__(self) -> None:
        self._sessions: Dict[str, GameSession] = {}

    def start_new_game(self) -> NewGameResponse:
        available_firearms = firearm_service.get_all_firearms()
        if not available_firearms:
            raise ValueError("No firearms available for game")

        target_firearm = random.choice(available_firearms)

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

        return NewGameResponse(
            session_id=session_id,
            firearm_image_url=target_firearm.image_url,
            max_guesses=game_session.max_guesses,
        )

    def make_guess(self, session_id: str, guess_firearm_id: str) -> GuessResult:
        session = self._get_session(session_id)
        if not session:
            raise ValueError("Game session not found")

        if session.is_completed:
            raise ValueError("Game already completed")

        if len(session.guesses_made) >= session.max_guesses:
            raise ValueError("Maximum guesses reached")

        guess_firearm = firearm_service.get_firearm_by_id(guess_firearm_id)
        if not guess_firearm:
            raise ValueError("Invalid firearm guess")

        session.guesses_made.append(guess_firearm_id)

        is_correct = guess_firearm_id == session.target_firearm.id

        comparisons = self._compare_firearms(guess_firearm, session.target_firearm)

        remaining_guesses = session.max_guesses - len(session.guesses_made)

        if is_correct:
            session.is_completed = True
            session.is_won = True
        elif remaining_guesses == 0:
            session.is_completed = True
            session.is_won = False

        return GuessResult(
            is_correct=is_correct,
            comparisons=comparisons,
            remaining_guesses=remaining_guesses,
        )

    def get_game_status(self, session_id: str) -> Optional[GameStatusResponse]:
        session = self._get_session(session_id)
        if not session:
            return None

        return GameStatusResponse(
            session_id=session_id,
            target_firearm_name=session.target_firearm.name
            if session.is_completed
            else None,
            guesses_made=len(session.guesses_made),
            max_guesses=session.max_guesses,
            is_completed=session.is_completed,
            is_won=session.is_won,
            target_firearm=session.target_firearm if session.is_completed else None,
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
        )

    def get_all_sessions(self) -> List[GameSession]:
        return list(self._sessions.values())

    def _get_session(self, session_id: str) -> Optional[GameSession]:
        return self._sessions.get(session_id)

    def _compare_firearms(
        self, guess_firearm: Firearm, target_firearm: Firearm
    ) -> List[GuessComparison]:
        comparisons = []

        manufacturer_result = (
            ComparisonResult.CORRECT
            if guess_firearm.manufacturer == target_firearm.manufacturer
            else ComparisonResult.INCORRECT
        )
        comparisons.append(
            GuessComparison(
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
            GuessComparison(
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
            GuessComparison(
                attribute="caliber",
                guess_value=guess_firearm.caliber,
                correct_value=target_firearm.caliber,
                result=caliber_result,
            )
        )

        country_result = (
            ComparisonResult.CORRECT
            if guess_firearm.country_of_origin == target_firearm.country_of_origin
            else ComparisonResult.INCORRECT
        )
        comparisons.append(
            GuessComparison(
                attribute="country_of_origin",
                guess_value=guess_firearm.country_of_origin,
                correct_value=target_firearm.country_of_origin,
                result=country_result,
            )
        )

        adoption_result = (
            ComparisonResult.CORRECT
            if guess_firearm.adoption_status == target_firearm.adoption_status
            else ComparisonResult.INCORRECT
        )
        comparisons.append(
            GuessComparison(
                attribute="adoption_status",
                guess_value=guess_firearm.adoption_status.value,
                correct_value=target_firearm.adoption_status.value,
                result=adoption_result,
            )
        )

        return comparisons


game_service = GameService()
