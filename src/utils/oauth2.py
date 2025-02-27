from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.exceptions import CredentialsError
from src.models.user import User
from src.utils.database import get_db
from src.utils.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = verify_token(token)
    user = db.query(User).filter(User.username == token_data.username).first()

    if user is None:
        raise CredentialsError

    return user
