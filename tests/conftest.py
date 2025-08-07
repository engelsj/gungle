from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.gungle.database import Base, get_db
from src.gungle.main import app
from src.gungle.services.firearm_service import FirearmService


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

    # Initialize sample data using FirearmService
    test_db_session = TestSessionLocal()
    try:
        firearm_service = FirearmService(db_session=test_db_session)
        firearm_service.initialize_sample_data()
    finally:
        test_db_session.close()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_db() -> None:
    pass
