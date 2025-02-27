from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions import BlogNotFoundError, UnauthorizedError, UserAlreadyExistsError


def init_exception_handlers(app):
    @app.exception_handler(BlogNotFoundError)
    async def blog_not_found_handler(request: Request, exc: BlogNotFoundError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_handler(request: Request, exc: UnauthorizedError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(UserAlreadyExistsError)
    async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
