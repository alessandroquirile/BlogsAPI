from fastapi import status


class BlogNotFoundError(Exception):
    def __init__(self, detail: str = "Blog not found", status_code: int = status.HTTP_404_NOT_FOUND):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class UnauthorizedError(Exception):
    def __init__(self, detail: str = "Not authorized", status_code: int = status.HTTP_401_UNAUTHORIZED):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class CredentialsError(Exception):
    def __init__(self, detail: str = "Could not validate credentials", status_code: int = status.HTTP_401_UNAUTHORIZED):
        self.detail = detail
        self.status_code = status_code
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(detail)


class UserAlreadyExistsError(Exception):
    def __init__(self, detail: str = "User already exists", status_code: int = status.HTTP_409_CONFLICT):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)
