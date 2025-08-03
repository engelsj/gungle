import pytest

from src.gungle.services.game_service import GameService


def test_get_available_firearm_names() -> None:
    service = GameService()
    names = service.get_available_firearm_names()

    assert len(names) > 0
    assert "AK-47" in names


def test_make_guess_by_name_correct() -> None:
    service = GameService()

    # Start new game
    response = service.start_new_game()
    session_id = response.session_id

    # Get the target firearm name
    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    # Make correct guess
    result = service.make_guess_by_name(session_id, target_name)

    assert result.is_correct is True
    assert result.game_completed is True
    assert result.guess_firearm.name == target_name
    assert result.remaining_guesses == 4
    assert len(result.comparisons) == 6


def test_make_guess_by_name_incorrect() -> None:
    service = GameService()

    # Start new game
    response = service.start_new_game()
    session_id = response.session_id

    # Get a different firearm name
    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    available_names = service.get_available_firearm_names()
    wrong_name = next((name for name in available_names if name != target_name), None)

    if wrong_name:
        # Make incorrect guess
        result = service.make_guess_by_name(session_id, wrong_name)

        assert result.is_correct is False
        assert result.game_completed is False
        assert result.guess_firearm.name == wrong_name
        assert result.remaining_guesses == 4
        assert len(result.comparisons) == 6


def test_invalid_firearm_name() -> None:
    service = GameService()

    # Start new game
    response = service.start_new_game()
    session_id = response.session_id

    # Try invalid name
    with pytest.raises(ValueError, match="not found"):
        service.make_guess_by_name(session_id, "Invalid Firearm Name")


def test_case_insensitive_guessing() -> None:
    service = GameService()

    # Start new game
    response = service.start_new_game()
    session_id = response.session_id

    # Get the target firearm name
    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    # Make guess with different case
    result = service.make_guess_by_name(session_id, target_name.upper())

    assert result.is_correct is True


def test_game_status_with_guess_history() -> None:
    service = GameService()

    # Start new game
    response = service.start_new_game()
    session_id = response.session_id

    # Make a guess
    available_names = service.get_available_firearm_names()
    service.make_guess_by_name(session_id, available_names[0])

    # Check status
    status = service.get_game_status(session_id)

    assert status is not None
    assert len(status.all_guess_results) == 1
    assert status.guesses_made == 1


def test_max_guesses_reached() -> None:
    service = GameService()

    # Start new game
    response = service.start_new_game()
    session_id = response.session_id

    # Get a wrong firearm name
    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    available_names = service.get_available_firearm_names()
    wrong_name = next((name for name in available_names if name != target_name), None)

    if wrong_name:
        # Make 5 wrong guesses
        for i in range(5):
            result = service.make_guess_by_name(session_id, wrong_name)
            expected_remaining = 5 - (i + 1)  # After each guess, remaining decreases
            assert result.remaining_guesses == expected_remaining

            if i < 4:  # First 4 guesses
                assert not result.game_completed
            else:  # 5th guess
                assert result.game_completed
                assert not result.is_correct
                assert result.remaining_guesses == 0

        # Try to make another guess (should fail with "Game already completed")
        with pytest.raises(ValueError, match="Game already completed"):
            service.make_guess_by_name(session_id, wrong_name)


def test_reveal_answer() -> None:
    service = GameService()

    # Start new game
    response = service.start_new_game()
    session_id = response.session_id

    # Complete the game by guessing correctly
    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name
    service.make_guess_by_name(session_id, target_name)

    # Reveal answer
    reveal = service.reveal_answer(session_id)

    assert reveal is not None
    assert reveal.is_won is True
    assert session is not None
    assert reveal.target_firearm.name == target_name
    assert len(reveal.all_guess_results) == 1


def test_remaining_guesses_calculation() -> None:
    service = GameService()

    # Start new game
    response = service.start_new_game()
    session_id = response.session_id

    # Get a wrong firearm name
    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    available_names = service.get_available_firearm_names()
    wrong_name = next((name for name in available_names if name != target_name), None)

    if wrong_name:
        # Test each guess and verify remaining count
        expected_remaining = [4, 3, 2, 1, 0]  # After guesses 1, 2, 3, 4, 5

        for i in range(5):
            result = service.make_guess_by_name(session_id, wrong_name)
            assert result.remaining_guesses == expected_remaining[i]

            # Check session state
            status = service.get_game_status(session_id)
            assert status is not None
            assert status.guesses_made == i + 1


def test_game_completion_logic() -> None:
    service = GameService()

    # Test winning on first guess
    response = service.start_new_game()
    session_id = response.session_id
    session = service._get_session(session_id)
    assert session is not None
    target_name = session.target_firearm.name

    result = service.make_guess_by_name(session_id, target_name)
    assert result.is_correct is True
    assert result.game_completed is True
    assert result.remaining_guesses == 4

    # Test losing after 5 wrong guesses
    response2 = service.start_new_game()
    session_id2 = response2.session_id
    session2 = service._get_session(session_id2)
    assert session2 is not None
    target_name2 = session2.target_firearm.name

    available_names = service.get_available_firearm_names()
    wrong_name = next((name for name in available_names if name != target_name2), None)

    if wrong_name:
        # Make 5 wrong guesses
        for i in range(5):
            result = service.make_guess_by_name(session_id2, wrong_name)

        # Game should be completed and lost
        assert result.is_correct is False
        assert result.game_completed is True
        assert result.remaining_guesses == 0
