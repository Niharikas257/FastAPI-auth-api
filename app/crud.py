# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import hash_password  # single source for hashing

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # ensure uniqueness
    if get_user_by_email(db, user.email):
        raise ValueError("Email already registered")

    db_user = models.User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
