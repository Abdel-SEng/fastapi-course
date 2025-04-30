from sqlalchemy.orm import Session

from ..models import models


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def create_user(db: Session, user: dict):
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
