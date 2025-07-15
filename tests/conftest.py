from typing import Generator

import pytest
from fastapi.testclient import TestClient

from src.gungle.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_db() -> None:
    pass
