from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..db_crud import crud_user
from ..schemas import user_schema
from ..db.database import get_db
from ..core import security

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserOut
)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # check if user with email already exists
    existing_user = crud_user.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email: {user.email} already exists",
        )

    # hash the password - user.password
    hashed_password = security.get_password_hash(user.password)
    user.password = hashed_password
    new_user = crud_user.create_user(db, user)
    return new_user


@router.get("/{id}", response_model=user_schema.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
):
    user = crud_user.get_user_by_id(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user
