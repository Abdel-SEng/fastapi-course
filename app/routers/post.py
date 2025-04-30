from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional


from ..db_crud import crud_post
from ..core import security
from ..models import models
from ..schemas import post_schema
from ..db.database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[post_schema.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(security.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    posts = crud_post.get_parameterized_posts_with_votes(
        db, limit=limit, skip=skip, search=search
    )
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=post_schema.Post)
def create_posts(
    post: post_schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(security.get_current_user),
):

    new_post = crud_post.create_post_for_current_user(post, db, current_user.id)

    return new_post


@router.get("/{id}", response_model=post_schema.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
):

    post = crud_post.get_post_by_id_with_votes(db, id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return post


@router.put("/{id}", response_model=post_schema.Post)
def update_post(
    id: int,
    updated_post: post_schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(security.get_current_user),
):

    post = crud_post.get_post_by_id(db, id)

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    update_post = crud_post.update_post_by_id_for_current_user(
        id, updated_post, db, current_user.id
    )

    return update_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(security.get_current_user),
):

    post = crud_post.get_post_by_id(db, id)

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    crud_post.delete_post_by_id(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
