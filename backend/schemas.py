from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


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


class WorkoutBase(BaseModel):
    date: Optional[datetime] = None
    exercise_type: str
    duration: int
    sets: int
    reps: int


class WorkoutCreate(WorkoutBase):
    pass


class Workout(WorkoutBase):
    id: int
    calories: float

    class Config:
        orm_mode = True


class ProgramBase(BaseModel):
    name: str
    goal: str
    description: Optional[str] = ""


class ProgramCreate(ProgramBase):
    pass


class Program(ProgramBase):
    id: int

    class Config:
        orm_mode = True
