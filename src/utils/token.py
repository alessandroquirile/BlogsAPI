from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from src.exceptions import UnauthorizedError
from src.schemas.token import TokenData

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise UnauthorizedError


def extract_username(payload: dict) -> str:
    username: str = payload.get("sub")
    if username is None:
        raise UnauthorizedError
    return username


def verify_token(token: str) -> TokenData:
    payload = decode_jwt(token)
    username = extract_username(payload)
    return TokenData(username=username)
