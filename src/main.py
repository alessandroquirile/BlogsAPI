from fastapi import FastAPI
from mangum import Mangum

from src.handlers import init_exception_handlers
from src.routers import blog, user, authentication
from src.utils.database import Base
from src.utils.database import engine

app = FastAPI()
handler = Mangum(app)

Base.metadata.create_all(bind=engine)

init_exception_handlers(app)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
