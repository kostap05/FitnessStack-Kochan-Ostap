from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    weight: Optional[float] = None
    height: Optional[float] = None
    goal: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    weight: Optional[float]
    height: Optional[float]
    goal: Optional[str]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
