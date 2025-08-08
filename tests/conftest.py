from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.gungle.database import Base, get_db
from src.gungle.main import app
from src.gungle.services.firearm_service import FirearmService
from tests.unit.test_firearm_repository import TestFirearmRepository


@pytest.fixture(scope="session", autouse=True)
def setup_test_database() -> None:
    test_engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator:
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session", autouse=True)
def setup_test_firearm_service() -> Generator:
    import src.gungle.api.v1.endpoints.firearms as firearms_endpoint_module
    import src.gungle.services.firearm_service as firearm_service_module
    import src.gungle.services.game_service as game_service_module

    test_repository = TestFirearmRepository()
    test_service = FirearmService(repository=test_repository)

    original_service = firearm_service_module.firearm_service

    firearm_service_module.firearm_service = test_service
    game_service_module.firearm_service = test_service
    firearms_endpoint_module.firearm_service = test_service

    yield test_service

    firearm_service_module.firearm_service = original_service


@pytest.fixture
def test_db() -> None:
    pass
