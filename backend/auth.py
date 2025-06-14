from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from backend.models import User
from backend.database import get_db
from backend.schemas import Token, UserOut
import os
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])

AVATAR_DIR = "static/avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=UserOut)
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    weight: float = Form(None),
    height: float = Form(None),
    goal: str = Form(None),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        raise HTTPException(status_code=400, detail="User already exists")

    avatar_url = None
    if avatar is not None:
        filename = f"{uuid4().hex}_{avatar.filename}"
        filepath = os.path.join(AVATAR_DIR, filename)
        os.makedirs(AVATAR_DIR, exist_ok=True)
        with open(filepath, "wb") as buffer:
            buffer.write(await avatar.read())
        avatar_url = f"/static/avatars/{filename}"

    hashed_password = pwd_context.hash(password)

    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        weight=weight,
        height=height,
        goal=goal,
        avatar_url=avatar_url
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}
