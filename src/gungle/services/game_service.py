import random
import uuid
from datetime import datetime
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
        self._guess_history: Dict[
            str, List[GuessResult]
        ] = {}  # Track all guess results

    def start_new_game(self) -> NewGameResponse:
        # Select random firearm as target
        available_firearms = firearm_service.get_all_firearms()
        if not available_firearms:
            raise ValueError("No firearms available for game")

        target_firearm = random.choice(available_firearms)

        # Create new game session
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
        # Validate session
        session = self._get_session(session_id)
        if not session:
            raise ValueError("Game session not found")

        # Check if game is already completed
        if session.is_completed:
            raise ValueError("Game already completed")

        # Check if max guesses reached
        if len(session.guesses_made) >= session.max_guesses:
            raise ValueError("Maximum guesses reached")

        # Find the guessed firearm by name (case-insensitive)
        guess_firearm = self._find_firearm_by_name(firearm_name)
        if not guess_firearm:
            raise ValueError(f"Firearm '{firearm_name}' not found")

        # Add guess to session
        session.guesses_made.append(guess_firearm.name)

        # Check if guess is correct
        is_correct = guess_firearm.name.lower() == session.target_firearm.name.lower()

        # Generate comparisons between guessed firearm and target
        comparisons = self._compare_firearms(guess_firearm, session.target_firearm)

        # Update session state
        remaining_guesses = session.max_guesses - len(session.guesses_made)

        if is_correct:
            session.is_completed = True
            session.is_won = True
        elif remaining_guesses == 0:
            session.is_completed = True
            session.is_won = False

        # Create guess result
        guess_result = GuessResult(
            is_correct=is_correct,
            guess_firearm=guess_firearm,
            target_firearm=session.target_firearm
            if session.is_completed
            else session.target_firearm,
            comparisons=comparisons,
            remaining_guesses=remaining_guesses,
            game_completed=session.is_completed,
        )

        # Store in guess history
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
            target_firearm_name=session.target_firearm.name
            if session.is_completed
            else None,
            guesses_made=len(session.guesses_made),
            max_guesses=session.max_guesses,
            is_completed=session.is_completed,
            is_won=session.is_won,
            target_firearm=session.target_firearm if session.is_completed else None,
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

        # Compare manufacturer
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

        # Compare type
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

        # Compare caliber
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

        # Compare country of origin
        country_result = (
            ComparisonResult.CORRECT
            if guess_firearm.country_of_origin == target_firearm.country_of_origin
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

        # Compare adoption status
        adoption_result = (
            ComparisonResult.CORRECT
            if guess_firearm.adoption_status == target_firearm.adoption_status
            else ComparisonResult.INCORRECT
        )
        comparisons.append(
            AttributeComparison(
                attribute="adoption_status",
                guess_value=guess_firearm.adoption_status.value,
                correct_value=target_firearm.adoption_status.value,
                result=adoption_result,
            )
        )

        # Compare year introduced (with some tolerance for partial matches)
        if guess_firearm.year_introduced and target_firearm.year_introduced:
            year_diff = abs(
                guess_firearm.year_introduced - target_firearm.year_introduced
            )
            if year_diff == 0:
                year_result = ComparisonResult.CORRECT
            elif year_diff <= 5:  # Within 5 years is partial
                year_result = ComparisonResult.PARTIAL
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


# Global game service instance
game_service = GameService()
