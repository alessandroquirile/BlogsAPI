from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.exceptions import UserNotFoundError, UnauthorizedError
from src.models.user import User
from src.utils.database import get_db
from src.utils.hashing import verify
from src.utils.token import create_access_token

router = APIRouter(
    tags=["authentication"],
)


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise UserNotFoundError(user_id=request.username)
    if not verify(request.password, user.password):
        raise UnauthorizedError
        # raise CredentialsError
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
