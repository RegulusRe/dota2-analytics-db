"""
Конфігурація pytest для тестування API
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
import os

# Додаємо батьківську директорію до Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ORM.main import app
from ORM.database import Base, get_db
from ORM.auth.models import User

# Використовуємо SQLite in-memory для тестів
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Створює нову сесію БД для кожного тесту"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Створює тестовий клієнт FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Створює тестового користувача"""
    from ORM.auth.security import get_password_hash
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(client, test_user):
    """Отримує JWT токен для тестового користувача"""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Створює headers з токеном авторизації"""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def sample_team(db_session):
    """Створює тестову команду"""
    from ORM.models import Teams
    team = Teams(name="Test Team")
    db_session.add(team)
    db_session.commit()
    db_session.refresh(team)
    return team


@pytest.fixture
def sample_player(db_session, sample_team):
    """Створює тестового гравця"""
    from ORM.models import Players
    player = Players(
        name="Test Player",
        nickname="TestNick",
        position="Carry",
        team_id=sample_team.team_id
    )
    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)
    return player


@pytest.fixture
def sample_hero(db_session):
    """Створює тестового героя"""
    from ORM.models import Heroes
    hero = Heroes(
        name="Test Hero",
        role="Carry",
        ultimate="Test Ultimate"
    )
    db_session.add(hero)
    db_session.commit()
    db_session.refresh(hero)
    return hero


@pytest.fixture
def sample_tournament(db_session):
    """Створює тестовий турнір"""
    from ORM.models import Tournaments
    from datetime import date
    tournament = Tournaments(
        name="Test Tournament",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 10)
    )
    db_session.add(tournament)
    db_session.commit()
    db_session.refresh(tournament)
    return tournament
