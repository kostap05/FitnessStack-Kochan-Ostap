from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from backend.models import Workout, Exercise, User
from backend.schemas import Workout, WorkoutCreate
from backend.dependencies import get_current_user, get_db

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.post("/", response_model=Workout)
def create_workout(
    workout: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_duration = sum(ex.duration for ex in workout.exercises)
    MET = 8
    weight_kg = current_user.weight
    total_calories = (MET * 3.5 * weight_kg / 200) * total_duration

    db_workout = Workout(
        title=workout.title,
        date=workout.date or datetime.utcnow(),
        total_duration=total_duration,
        total_calories=total_calories,
        owner=current_user
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)

    for ex in workout.exercises:
        db_exercise = Exercise(
            workout_id=db_workout.id,
            exercise_name=ex.exercise_name,
            sets=ex.sets,
            reps=ex.reps,
            duration=ex.duration
        )
        db.add(db_exercise)

    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.get("/", response_model=List[Workout])
def list_workouts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Workout).filter(Workout.user_id == current_user.id).all()


@router.delete("/{workout_id}")
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_workout = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == current_user.id).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(db_workout)
    db.commit()
    return {"msg": "Workout deleted"}