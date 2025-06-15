from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
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

TEST_USER = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword",
    "weight": 70.5,
    "height": 180,
    "goal": "Lose weight"
}

access_token = None


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": TEST_USER["username"],
            "email": TEST_USER["email"],
            "password": TEST_USER["password"],
            "weight": TEST_USER["weight"],
            "height": TEST_USER["height"],
            "goal": TEST_USER["goal"]
        }
    )
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        data = response.json()
        assert data["username"] == TEST_USER["username"]
    elif response.status_code == 400:
        assert response.json()["detail"] == "User already exists"


def test_login_success():
    global access_token
    response = client.post(
        "/auth/login",
        data={
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    access_token = data["access_token"]


def test_login_invalid_password():
    response = client.post(
        "/auth/login",
        data={
            "username": TEST_USER["username"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_get_profile_authorized():
    global access_token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/profile", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == TEST_USER["username"]


def test_get_profile_unauthorized():
    response = client.get("/profile")
    assert response.status_code == 401