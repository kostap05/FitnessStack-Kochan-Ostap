from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
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


class ExerciseBase(BaseModel):
    exercise_name: str
    sets: int
    reps: int
    duration: int  # мин


class ExerciseCreate(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    id: int

    class Config:
        orm_mode = True


class WorkoutBase(BaseModel):
    title: str
    category: Optional[str] = None
    is_favorite: Optional[bool] = False
    date: Optional[datetime] = None


class WorkoutCreate(WorkoutBase):
    exercises: List[ExerciseCreate]


class WorkoutUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    is_favorite: Optional[bool] = None
    exercises: Optional[List[ExerciseCreate]] = None


class Workout(WorkoutBase):
    id: int
    date: datetime
    total_duration: int
    total_calories: float
    exercises: List[Exercise]

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


class OwnProgramExerciseBase(BaseModel):
    exercise_name: str
    sets: int
    reps: int


class OwnProgramDayBase(BaseModel):
    day_name: str
    exercises: List[OwnProgramExerciseBase]


class OwnProgramCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    days: List[OwnProgramDayBase]


class OwnProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    days: Optional[List[OwnProgramDayBase]] = None


class OwnProgramExercise(OwnProgramExerciseBase):
    id: int

    class Config:
        orm_mode = True


class OwnProgramDay(OwnProgramDayBase):
    id: int
    exercises: List[OwnProgramExercise]

    class Config:
        orm_mode = True


class OwnProgram(BaseModel):
    id: int
    name: str
    description: str
    days: List[OwnProgramDay]

    class Config:
        orm_mode = True