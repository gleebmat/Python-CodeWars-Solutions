from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.database import Base
from app.dependency import get_db
from main import app


TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)


def get_test_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture()
def client():
    yield TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db

    finally:
        db.close()
