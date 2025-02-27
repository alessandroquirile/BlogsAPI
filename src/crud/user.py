from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.user import User as UserModel
from src.schemas.user import User
from src.utils.hashing import bcrypt


def get(user_id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


def create(request: User, db: Session):
    hashed_password = bcrypt(request.password)
    new_user = UserModel(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
