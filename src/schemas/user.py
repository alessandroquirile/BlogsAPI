from typing import List

from pydantic import BaseModel, ConfigDict


# The schemas data classes define the API that FastAPI uses to interact with the database

class User(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False


class UserSummary(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)


class ShowUser(BaseModel):
    username: str
    email: str
    is_admin: bool
    blogs: List["Blog"]  # Stesso nome della relationship in models

    model_config = ConfigDict(from_attributes=True)


from src.schemas.blog import Blog
