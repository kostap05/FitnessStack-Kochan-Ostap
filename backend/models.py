from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    goal = Column(String, nullable=True)

    avatar_url = Column(String, nullable=True)

    workouts = relationship("Workout", back_populates="owner")
    programs = relationship("Program", back_populates="owner")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_duration = Column(Integer)
    total_calories = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

    exercises = relationship("Exercise", back_populates="workout")
    owner = relationship("User", back_populates="workouts")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    exercise_name = Column(String)
    sets = Column(Integer)
    reps = Column(Integer)
    duration = Column(Integer)

    workout = relationship("Workout", back_populates="exercises")


class Program(Base):
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    goal = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="programs")
