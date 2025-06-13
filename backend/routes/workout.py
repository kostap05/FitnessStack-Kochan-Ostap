from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from backend.models import Workout as WorkoutModel, Exercise as ExerciseModel, User as UserModel
from backend.schemas import Workout as WorkoutSchema, WorkoutCreate, WorkoutUpdate
from backend.dependencies import get_current_user, get_db

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.post("/", response_model=WorkoutSchema)
def create_workout(
    workout: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    total_duration = sum(ex.duration for ex in workout.exercises)
    MET = 8
    weight_kg = current_user.weight
    total_calories = (MET * 3.5 * weight_kg / 200) * total_duration

    db_workout = WorkoutModel(
        title=workout.title,
        category=workout.category,
        is_favorite=workout.is_favorite or False,
        date=workout.date or datetime.utcnow(),
        total_duration=total_duration,
        total_calories=total_calories,
        owner=current_user
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)

    for ex in workout.exercises:
        db_exercise = ExerciseModel(
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


@router.get("/", response_model=List[WorkoutSchema])
def list_workouts(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    query = db.query(WorkoutModel).filter(WorkoutModel.user_id == current_user.id)
    if category:
        query = query.filter(WorkoutModel.category == category)
    return query.all()


@router.put("/{workout_id}", response_model=WorkoutSchema)
def update_workout(
    workout_id: int,
    workout: WorkoutUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_workout = db.query(WorkoutModel).filter(
        WorkoutModel.id == workout_id,
        WorkoutModel.user_id == current_user.id
    ).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    if workout.title:
        db_workout.title = workout.title
    if workout.category:
        db_workout.category = workout.category
    if workout.is_favorite is not None:
        db_workout.is_favorite = workout.is_favorite

    if workout.exercises is not None:
        db.query(ExerciseModel).filter(ExerciseModel.workout_id == db_workout.id).delete()

        total_duration = 0
        for ex in workout.exercises:
            new_ex = ExerciseModel(
                exercise_name=ex.exercise_name,
                sets=ex.sets,
                reps=ex.reps,
                duration=ex.duration,
                workout_id=db_workout.id
            )
            total_duration += ex.duration
            db.add(new_ex)

        db_workout.total_duration = total_duration
        MET = 8
        db_workout.total_calories = (MET * 3.5 * current_user.weight / 200) * total_duration

    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.delete("/{workout_id}")
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_workout = db.query(WorkoutModel).filter(
        WorkoutModel.id == workout_id,
        WorkoutModel.user_id == current_user.id
    ).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(db_workout)
    db.commit()
    return {"msg": "Workout deleted"}


@router.post("/{workout_id}/favorite", response_model=WorkoutSchema)
def toggle_favorite(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_workout = db.query(WorkoutModel).filter(
        WorkoutModel.id == workout_id,
        WorkoutModel.user_id == current_user.id
    ).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    db_workout.is_favorite = not db_workout.is_favorite
    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.get("/favorites/", response_model=List[WorkoutSchema])
def list_favorites(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return db.query(WorkoutModel).filter(
        WorkoutModel.user_id == current_user.id,
        WorkoutModel.is_favorite == True
    ).all()


@router.post("/{workout_id}/repeat", response_model=WorkoutSchema)
def repeat_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    workout = db.query(WorkoutModel).filter(
        WorkoutModel.id == workout_id,
        WorkoutModel.user_id == current_user.id
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    new_workout = WorkoutModel(
        title=workout.title + " (Repeated)",
        category=workout.category,
        is_favorite=workout.is_favorite,
        date=datetime.utcnow(),
        total_duration=workout.total_duration,
        total_calories=workout.total_calories,
        owner=current_user
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    for ex in workout.exercises:
        new_ex = ExerciseModel(
            workout_id=new_workout.id,
            exercise_name=ex.exercise_name,
            sets=ex.sets,
            reps=ex.reps,
            duration=ex.duration
        )
        db.add(new_ex)

    db.commit()
    db.refresh(new_workout)
    return new_workout