from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from backend.dependencies import get_current_user, get_db
from backend.models import User
from backend.schemas import UserOut
import os
from uuid import uuid4

router = APIRouter(tags=["user"])
AVATAR_DIR = "static/avatars"

@router.get("/profile", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/profile/update", response_model=UserOut)
async def update_profile(
    weight: float = Form(None),
    height: float = Form(None),
    goal: str = Form(None),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if weight:
        current_user.weight = weight
    if height:
        current_user.height = height
    if goal:
        current_user.goal = goal
    if avatar:
        filename = f"{uuid4().hex}_{avatar.filename}"
        filepath = os.path.join(AVATAR_DIR, filename)
        with open(filepath, "wb") as buffer:
            buffer.write(await avatar.read())
        current_user.avatar_url = f"/{filepath}"

    db.commit()
    db.refresh(current_user)
    return current_user
