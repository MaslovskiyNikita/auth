class BaseAppException(Exception):  # Для создания новых логик для базовых эксепшинов
    def __init__(self, message: str, *args):
        super().__init__(message, *args)
        self.message = message
        self.args = args


class DefaultMessageException(BaseAppException):

    default_message: str

    def __init__(self, message: str = None, *args):  # type: ignore[assignment]
        if message is None:
            message = self.default_message
        super().__init__(message, *args)


class UserAlreadyExistsError(BaseAppException):
    def __init__(self, email: str):
        message = f"User with email {email} already exists"
        super().__init__(message)
        self.email = email


class InvalidTokenError(DefaultMessageException):
    default_message = "Invalid or expired token"


class UserNotFoundError(DefaultMessageException):
    default_message = "User not found"
