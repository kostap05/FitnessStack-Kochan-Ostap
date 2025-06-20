from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
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
    category = Column(String, nullable=True)
    is_favorite = Column(Boolean, default=False)
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


class OwnProgram(Base):
    __tablename__ = "own_programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    days = relationship("OwnProgramDay", back_populates="program", cascade="all, delete")
    owner = relationship("User", back_populates="own_programs")


class OwnProgramDay(Base):
    __tablename__ = "own_program_days"

    id = Column(Integer, primary_key=True, index=True)
    day_name = Column(String)
    program_id = Column(Integer, ForeignKey("own_programs.id"))

    program = relationship("OwnProgram", back_populates="days")
    exercises = relationship("OwnProgramExercise", back_populates="day", cascade="all, delete")


class OwnProgramExercise(Base):
    __tablename__ = "own_program_exercises"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("own_program_days.id"))
    exercise_name = Column(String)
    sets = Column(Integer)
    reps = Column(Integer)

    day = relationship("OwnProgramDay", back_populates="exercises")


User.own_programs = relationship("OwnProgram", back_populates="owner")