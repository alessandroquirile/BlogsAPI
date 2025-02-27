from pydantic import BaseModel, ConfigDict


# The schemas data classes define the API that FastAPI uses to interact with the database

class Blog(BaseModel):
    title: str
    description: str
    # user_id: int


class ShowBlog(BaseModel):
    id: int
    title: str
    description: str
    written_by: "UserSummary"  # Stesso nome della relationship in models

    model_config = ConfigDict(from_attributes=True)


from src.schemas.user import UserSummary
