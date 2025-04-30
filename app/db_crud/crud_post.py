from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import post_schema


def get_post_by_id_with_votes(db: Session, post_id: int):
    return (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == post_id)
        .first()
    )


def get_parameterized_posts_with_votes(
    db: Session, skip: int = 0, limit: int = 100, search: str = Optional[str]
):
    return (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )


def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def create_post_for_current_user(
    post: post_schema.PostCreate, db: Session, current_user_id: int
):
    new_post = models.Post(**post.dict(), owner_id=current_user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def update_post_by_id_for_current_user(
    post_id: int, post: post_schema.PostCreate, db: Session, current_user_id: int
):

    db.query(models.Post).filter(models.Post.id == post_id).update(
        post.dict(), synchronize_session=False
    )
    db.commit()
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def delete_post_by_id(post_id: int, db: Session):
    db.query(models.Post).filter(models.Post.id == post_id).delete()
    db.commit()
    return True
