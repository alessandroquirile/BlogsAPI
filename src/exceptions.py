from fastapi import status


class BlogNotFoundError(Exception):
    def __init__(self, blog_id: int):
        self.detail = f"Blog id={blog_id} not found"
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(blog_id)


class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.detail = f"User id={user_id} not found"
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(user_id)


class UnauthorizedError(Exception):
    def __init__(self, detail: str = "Not authorized"):
        self.detail = detail
        self.status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(detail)


class CredentialsError(Exception):
    def __init__(self, detail: str = "Could not validate credentials"):
        self.detail = detail
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(detail)


class UserAlreadyExistsError(Exception):
    def __init__(self, detail: str = "User already exists"):
        self.detail = detail
        self.status_code = status.HTTP_409_CONFLICT
        super().__init__(detail)
