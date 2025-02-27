from passlib.context import CryptContext
from sqlalchemy.orm import InstrumentedAttribute

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: InstrumentedAttribute) -> bool:
    return pwd_context.verify(plain_password, str(hashed_password))
