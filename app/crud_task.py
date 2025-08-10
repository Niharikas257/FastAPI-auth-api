from sqlalchemy.orm import Session

from app import models_task, schemas_task


def create_task(db: Session, task: schemas_task.TaskCreate, user_id: int):
    db_task = models_task.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, user_id: int):
    return db.query(models_task.Task).filter(models_task.Task.owner_id == user_id).all()


def get_task(db: Session, task_id: int, user_id: int):
    return (
        db.query(models_task.Task)
        .filter(models_task.Task.id == task_id, models_task.Task.owner_id == user_id)
        .first()
    )


def update_task(
    db: Session, task_id: int, user_id: int, task_data: schemas_task.TaskCreate
):
    task = get_task(db, task_id, user_id)
    if task:
        task.title = task_data.title
        task.description = task_data.description
        db.commit()
        db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: int):
    task = get_task(db, task_id, user_id)
    if task:
        db.delete(task)
        db.commit()
    return task
