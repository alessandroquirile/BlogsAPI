from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from src.handlers import init_exception_handlers
from src.routers import blog, user, authentication

app = FastAPI()
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_exception_handlers(app)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
