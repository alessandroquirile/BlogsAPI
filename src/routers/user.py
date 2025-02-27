from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.crud import user
from src.schemas.user import ShowUser, User
from src.utils.database import get_db
from src.utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=ShowUser)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=ShowUser)
async def users(user_id: int, db: Session = Depends(get_db)):
    return user.get(user_id, db)


@router.post("", response_model=ShowUser)
async def create_user(request: User, db: Session = Depends(get_db)):
    return user.create(request, db)
