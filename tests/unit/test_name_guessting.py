from datetime import date
from unittest.mock import patch

import pytest

from src.gungle.services.game_service import GameService


def test_get_available_firearm_names() -> None:
    service = GameService()
    names = service.get_available_firearm_names()

    assert len(names) > 0
    assert "AK-47" in names


def test_make_guess_by_name_correct() -> None:
    service = GameService()

    response = service.start_new_game()
    session_id = response.session_id

    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    result = service.make_guess_by_name(session_id, target_name)

    assert result.is_correct is True
    assert result.game_completed is True
    assert result.guess_firearm.name == target_name
    assert result.remaining_guesses == 4
    assert len(result.comparisons) == 7


def test_make_guess_by_name_incorrect() -> None:
    service = GameService()

    response = service.start_new_game()
    session_id = response.session_id

    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    available_names = service.get_available_firearm_names()
    wrong_name = next((name for name in available_names if name != target_name), None)

    if wrong_name:
        result = service.make_guess_by_name(session_id, wrong_name)

        assert result.is_correct is False
        assert result.game_completed is False
        assert result.guess_firearm.name == wrong_name
        assert result.remaining_guesses == 4
        assert len(result.comparisons) == 7


def test_invalid_firearm_name() -> None:
    service = GameService()

    response = service.start_new_game()
    session_id = response.session_id

    with pytest.raises(ValueError, match="not found"):
        service.make_guess_by_name(session_id, "Invalid Firearm Name")


def test_case_insensitive_guessing() -> None:
    service = GameService()

    response = service.start_new_game()
    session_id = response.session_id

    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    result = service.make_guess_by_name(session_id, target_name.upper())

    assert result.is_correct is True


def test_game_status_with_guess_history() -> None:
    service = GameService()

    response = service.start_new_game()
    session_id = response.session_id

    available_names = service.get_available_firearm_names()
    service.make_guess_by_name(session_id, available_names[0])

    status = service.get_game_status(session_id)

    assert status is not None
    assert len(status.all_guess_results) == 1
    assert status.guesses_made == 1


def test_max_guesses_reached() -> None:
    service = GameService()

    response = service.start_new_game()
    session_id = response.session_id

    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    available_names = service.get_available_firearm_names()
    wrong_name = next((name for name in available_names if name != target_name), None)

    if wrong_name:
        for i in range(5):
            result = service.make_guess_by_name(session_id, wrong_name)
            expected_remaining = 5 - (i + 1)
            assert result.remaining_guesses == expected_remaining

            if i < 4:
                assert not result.game_completed
            else:
                assert result.game_completed
                assert not result.is_correct
                assert result.remaining_guesses == 0

        with pytest.raises(ValueError, match="Game already completed"):
            service.make_guess_by_name(session_id, wrong_name)


def test_reveal_answer() -> None:
    service = GameService()

    response = service.start_new_game()
    session_id = response.session_id

    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name
    service.make_guess_by_name(session_id, target_name)

    reveal = service.reveal_answer(session_id)

    assert reveal is not None
    assert reveal.is_won is True
    assert session is not None
    assert reveal.target_firearm.name == target_name
    assert len(reveal.all_guess_results) == 1


def test_remaining_guesses_calculation() -> None:
    service = GameService()

    response = service.start_new_game()
    session_id = response.session_id

    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    available_names = service.get_available_firearm_names()
    wrong_name = next((name for name in available_names if name != target_name), None)

    if wrong_name:
        expected_remaining = [4, 3, 2, 1, 0]

        for i in range(5):
            result = service.make_guess_by_name(session_id, wrong_name)
            assert result.remaining_guesses == expected_remaining[i]

            status = service.get_game_status(session_id)
            assert status is not None
            assert status.guesses_made == i + 1


def test_game_completion_logic() -> None:
    service = GameService()

    response = service.start_new_game()
    session_id = response.session_id
    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    result = service.make_guess_by_name(session_id, target_name)
    assert result.is_correct is True
    assert result.game_completed is True
    assert result.remaining_guesses == 4

    response2 = service.start_new_game()
    session_id2 = response2.session_id
    session2 = service._get_session(session_id2)
    assert session2 is not None
    target_name2 = session2.target_firearm.name

    available_names = service.get_available_firearm_names()
    wrong_name = next((name for name in available_names if name != target_name2), None)

    if wrong_name:
        for i in range(5):
            result = service.make_guess_by_name(session_id2, wrong_name)

        assert result.is_correct is False
        assert result.game_completed is True
        assert result.remaining_guesses == 0


def test_daily_firearm_consistency() -> None:
    service = GameService()

    response1 = service.start_new_game()
    response2 = service.start_new_game()
    response3 = service.start_new_game()

    session1 = service._get_session(response1.session_id)
    session2 = service._get_session(response2.session_id)
    session3 = service._get_session(response3.session_id)

    assert session1 is not None
    assert session2 is not None
    assert session3 is not None

    assert session1.target_firearm.name == session2.target_firearm.name
    assert session2.target_firearm.name == session3.target_firearm.name
    assert session1.target_firearm.id == session2.target_firearm.id
    assert session2.target_firearm.id == session3.target_firearm.id


def test_daily_firearm_deterministic_selection() -> None:
    service1 = GameService()
    service2 = GameService()

    test_date = date(2024, 1, 15)

    with patch("src.gungle.services.game_service.date") as mock_date:
        mock_date.today.return_value = test_date
        firearm1 = service1._get_daily_firearm()
        firearm2 = service2._get_daily_firearm()

        assert firearm1.name == firearm2.name
        assert firearm1.id == firearm2.id


def test_daily_firearm_changes_by_date() -> None:
    service = GameService()

    date1 = date(2024, 1, 15)
    date2 = date(2024, 1, 16)

    with patch("src.gungle.services.game_service.date") as mock_date:
        mock_date.today.return_value = date1
        firearm1 = service._get_daily_firearm()

        service._current_daily_firearm = None
        service._current_date = None

        mock_date.today.return_value = date2
        firearm2 = service._get_daily_firearm()

        assert firearm1.name != firearm2.name or firearm1.id != firearm2.id


def test_get_daily_firearm_public_method() -> None:
    """Test the public get_daily_firearm method."""
    service = GameService()

    daily_firearm = service.get_daily_firearm()

    assert daily_firearm is not None
    assert daily_firearm.name is not None
    assert daily_firearm.id is not None

    response = service.start_new_game()
    session = service._get_session(response.session_id)
    assert session is not None

    assert daily_firearm.name == session.target_firearm.name
    assert daily_firearm.id == session.target_firearm.id
