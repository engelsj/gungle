from datetime import datetime

from src.gungle.models.firearm import (
    ActionType,
    AttributeComparison,
    Caliber,
    ComparisonResult,
    Firearm,
    FirearmType,
    GameSession,
    ModelType,
    NewGameResponse,
)


def test_firearm_model() -> None:
    firearm = Firearm(
        id="test_rifle",
        name="Test Rifle",
        manufacturer="Test Manufacturer",
        type=FirearmType.RIFLE,
        caliber=Caliber.THREE_OH_THREE_BRITISH,
        country_of_origin="United States",
        model_type=ModelType.MILITARY,
        year_introduced=1936,
        actionType=ActionType.TEST_ACTION,
        description="A test rifle",
        image_url="/test/image.jpg",
    )

    assert firearm.id == "test_rifle"
    assert firearm.name == "Test Rifle"
    assert firearm.type == FirearmType.RIFLE
    assert firearm.model_type == ModelType.MILITARY


def test_attribute_comparison() -> None:
    comparison = AttributeComparison(
        attribute="manufacturer",
        guess_value="Colt",
        correct_value="Springfield Armory",
        result=ComparisonResult.INCORRECT,
    )

    assert comparison.attribute == "manufacturer"
    assert comparison.result == ComparisonResult.INCORRECT


def test_game_session() -> None:
    firearm = Firearm(
        id="test_rifle",
        name="Test Rifle",
        manufacturer="Test Manufacturer",
        type=FirearmType.RIFLE,
        caliber=Caliber.THREE_OH_THREE_BRITISH,
        country_of_origin="United States",
        model_type=ModelType.MILITARY,
        year_introduced=1936,
        description="A test rifle",
        actionType=ActionType.TEST_ACTION,
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
