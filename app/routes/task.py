from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud_task, schemas_task
from app.auth import get_current_user
from app.database import SessionLocal
from app.models import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tasks", response_model=schemas_task.Task)
def create_task(
    task: schemas_task.TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_task.create_task(db, task, current_user.id)


@router.get("/tasks", response_model=list[schemas_task.Task])
def read_tasks(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return crud_task.get_tasks(db, current_user.id)


@router.put("/tasks/{task_id}", response_model=schemas_task.Task)
def update(
    task_id: int,
    task: schemas_task.TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = crud_task.update_task(db, task_id, current_user.id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/tasks/{task_id}")
def delete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = crud_task.delete_task(db, task_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
