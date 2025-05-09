class UserAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} already exists")


class InvalidTokenError(Exception):
    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message)
        self.message = message


class UserNotFoundError(Exception):
    def __init__(self, message: str = "User not found"):
        super().__init__(message)
        self.message = message
