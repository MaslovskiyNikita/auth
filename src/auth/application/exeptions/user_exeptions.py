from src.auth.application.exeptions.base_exeption import BaseApplicationException


class UserAlreadyExistsError(BaseApplicationException):
    def __init__(self, email: str):
        message = f"User with email {email} already exists"
        super().__init__(message)
        self.email = email


class InvalidTokenError(BaseApplicationException):
    default_message = "Invalid or expired token"


class UserNotFoundError(BaseApplicationException):
    default_message = "User not found"


class UserNotActiveError(BaseApplicationException):
    default_message = "not verifyed email"


class UserNotLogged(BaseApplicationException):
    default_message = "you are not logged"


class InvalidPasswordError(BaseApplicationException):
    default_message = "Invalid password"
