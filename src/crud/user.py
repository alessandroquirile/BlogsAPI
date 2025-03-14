from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.exceptions import UserAlreadyExistsError, UserNotFoundError
from src.models.user import User as UserModel
from src.schemas.user import User
from src.utils.hashing import bcrypt


def get_all(db: Session):
    users = db.query(UserModel).all()
    return users


def get(user_id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise UserNotFoundError(user_id)
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


def create(request: User, db: Session):
    try:
        hashed_password = bcrypt(request.password)
        new_user = UserModel(username=request.username, email=request.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise UserAlreadyExistsError(request.username)
