import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.database import Base, get_db
from backend.models import User
from jose import jwt
from datetime import timedelta, datetime
import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Задаем параметры токена
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def create_test_user():
    db = TestingSessionLocal()
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="$pbkdf2-sha256$29000$PEpZ.Rc4LXeViGEdMecMow$MXUI2fiQ1O/RBp2Eu5kHY9h6BK8CG0d.8bPdhVj4rW8",
        weight=70
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def create_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@pytest.fixture(scope="module")
def auth_headers():
    user = create_test_user()
    token = create_token(user.username)
    return {"Authorization": f"Bearer {token}"}


def test_create_workout(auth_headers):
    response = client.post(
        "/workouts/",
        json={
            "title": "Test Workout",
            "category": "Cardio",
            "exercises": [
                {"exercise_name": "Jumping Jacks", "sets": 3, "reps": 20, "duration": 10},
                {"exercise_name": "Push Ups", "sets": 3, "reps": 15, "duration": 5}
            ]
        },
        headers=auth_headers
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Workout"
    assert len(data["exercises"]) == 2


def test_list_workouts(auth_headers):
    response = client.get("/workouts/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_workout_by_id(auth_headers):
    response = client.get("/workouts/", headers=auth_headers)
    workout_id = response.json()[0]["id"]

    response = client.get(f"/workouts/{workout_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == workout_id