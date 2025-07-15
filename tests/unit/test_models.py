from datetime import datetime

from src.gungle.models.firearm import (
    AdoptionStatus,
    ComparisonResult,
    Firearm,
    FirearmType,
    GameSession,
    GuessComparison,
    GuessResult,
    NewGameResponse,
)


def test_firearm_model() -> None:
    firearm = Firearm(
        id="test_rifle",
        name="Test Rifle",
        manufacturer="Test Manufacturer",
        type=FirearmType.RIFLE,
        caliber=".30-06",
        country_of_origin="United States",
        adoption_status=AdoptionStatus.MILITARY,
        year_introduced=1936,
        actionType="TEST ACTION",
        description="A test rifle",
        image_url="/test/image.jpg",
    )

    assert firearm.id == "test_rifle"
    assert firearm.name == "Test Rifle"
    assert firearm.type == FirearmType.RIFLE
    assert firearm.adoption_status == AdoptionStatus.MILITARY


def test_guess_comparison() -> None:
    comparison = GuessComparison(
        attribute="manufacturer",
        guess_value="Colt",
        correct_value="Springfield Armory",
        result=ComparisonResult.INCORRECT,
    )

    assert comparison.attribute == "manufacturer"
    assert comparison.result == ComparisonResult.INCORRECT


def test_guess_result() -> None:
    comparisons = [
        GuessComparison(
            attribute="type",
            guess_value="rifle",
            correct_value="rifle",
            result=ComparisonResult.CORRECT,
        )
    ]

    result = GuessResult(is_correct=False, comparisons=comparisons, remaining_guesses=4)

    assert not result.is_correct
    assert len(result.comparisons) == 1
    assert result.remaining_guesses == 4


def test_game_session() -> None:
    firearm = Firearm(
        id="test_rifle",
        name="Test Rifle",
        manufacturer="Test Manufacturer",
        type=FirearmType.RIFLE,
        caliber=".30-06",
        country_of_origin="United States",
        adoption_status=AdoptionStatus.MILITARY,
        year_introduced=1936,
        description="A test rifle",
        actionType="TEST ACTION",
        image_url="/test/image.jpg",
    )

    session = GameSession(
        session_id="test-session-123",
        target_firearm=firearm,
        guesses_made=["guess1", "guess2"],
        is_completed=False,
        is_won=False,
        created_at=datetime.now(),
        max_guesses=5,
    )

    assert session.session_id == "test-session-123"
    assert len(session.guesses_made) == 2
    assert not session.is_completed
    assert session.max_guesses == 5


def test_new_game_response() -> None:
    response = NewGameResponse(
        session_id="test-session-123",
        firearm_image_url="/uploads/images/test.jpg",
        max_guesses=5,
    )

    assert response.session_id == "test-session-123"
    assert response.firearm_image_url == "/uploads/images/test.jpg"
    assert response.max_guesses == 5
