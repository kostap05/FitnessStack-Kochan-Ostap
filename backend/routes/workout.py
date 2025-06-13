from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from backend.models import Workout, User
from backend.schemas import Workout, WorkoutCreate
from backend.dependencies import get_current_user, get_db

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.post("/", response_model=Workout)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    MET = 8
    weight_kg = current_user.weight
    calories = (MET * 3.5 * weight_kg / 200) * workout.duration

    db_workout = Workout(
        date=workout.date or datetime.utcnow(),
        exercise_type=workout.exercise_type,
        duration=workout.duration,
        sets=workout.sets,
        reps=workout.reps,
        calories=calories,
        owner=current_user
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.get("/", response_model=List[Workout])
def list_workouts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Workout).filter(Workout.user_id == current_user.id).all()


@router.put("/{workout_id}", response_model=Workout)
def update_workout(workout_id: int, workout: WorkoutCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_workout = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == current_user.id).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    db_workout.exercise_type = workout.exercise_type
    db_workout.duration = workout.duration
    db_workout.sets = workout.sets
    db_workout.reps = workout.reps
    db_workout.calories = (8 * 3.5 * current_user.weight / 200) * workout.duration

    db.commit()
    db.refresh(db_workout)
    return db_workout

@router.delete("/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_workout = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == current_user.id).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(db_workout)
    db.commit()
    return {"msg": "Workout deleted"}
