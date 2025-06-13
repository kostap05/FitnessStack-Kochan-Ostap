from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.models import User as UserModel, OwnProgram as OwnProgramModel, OwnProgramDay as OwnProgramDayModel, OwnProgramExercise as OwnProgramExerciseModel
from backend.schemas import OwnProgramCreate, OwnProgram, OwnProgramUpdate
from backend.dependencies import get_current_user, get_db

router = APIRouter(prefix="/own-programs", tags=["Own Programs"])


@router.post("/", response_model=OwnProgram)
def create_program(
    program: OwnProgramCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_program = OwnProgramModel(
        name=program.name,
        description=program.description,
        owner=current_user
    )
    db.add(db_program)
    db.commit()
    db.refresh(db_program)

    for day in program.days:
        db_day = OwnProgramDayModel(
            day_name=day.day_name,
            program_id=db_program.id
        )
        db.add(db_day)
        db.commit()
        db.refresh(db_day)

        for ex in day.exercises:
            db_ex = OwnProgramExerciseModel(
                day_id=db_day.id,
                exercise_name=ex.exercise_name,
                sets=ex.sets,
                reps=ex.reps
            )
            db.add(db_ex)
        db.commit()

    return db_program


@router.get("/", response_model=List[OwnProgram])
def list_programs(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return db.query(OwnProgramModel).filter(OwnProgramModel.user_id == current_user.id).all()


@router.get("/{program_id}", response_model=OwnProgram)
def get_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_program = db.query(OwnProgramModel).filter(
        OwnProgramModel.id == program_id,
        OwnProgramModel.user_id == current_user.id
    ).first()
    if not db_program:
        raise HTTPException(status_code=404, detail="Program not found")
    return db_program


@router.put("/{program_id}", response_model=OwnProgram)
def update_program(
    program_id: int,
    program: OwnProgramUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_program = db.query(OwnProgramModel).filter(
        OwnProgramModel.id == program_id,
        OwnProgramModel.user_id == current_user.id
    ).first()

    if not db_program:
        raise HTTPException(status_code=404, detail="Program not found")

    if program.name is not None:
        db_program.name = program.name
    if program.description is not None:
        db_program.description = program.description

    if program.days is not None:
        for day in db_program.days:
            db.query(OwnProgramExerciseModel).filter(OwnProgramExerciseModel.day_id == day.id).delete()
        db.query(OwnProgramDayModel).filter(OwnProgramDayModel.program_id == db_program.id).delete()
        db.commit()

        # Добавляем новые дни и упражнения
        for day in program.days:
            db_day = OwnProgramDayModel(
                day_name=day.day_name,
                program_id=db_program.id
            )
            db.add(db_day)
            db.commit()
            db.refresh(db_day)

            for ex in day.exercises:
                db_ex = OwnProgramExerciseModel(
                    day_id=db_day.id,
                    exercise_name=ex.exercise_name,
                    sets=ex.sets,
                    reps=ex.reps
                )
                db.add(db_ex)
            db.commit()

    db.commit()
    db.refresh(db_program)
    return db_program


@router.delete("/{program_id}")
def delete_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_program = db.query(OwnProgramModel).filter(
        OwnProgramModel.id == program_id,
        OwnProgramModel.user_id == current_user.id
    ).first()
    if not db_program:
        raise HTTPException(status_code=404, detail="Program not found")

    db.delete(db_program)
    db.commit()
    return {"msg": "Program deleted"}
