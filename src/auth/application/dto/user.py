from dataclasses import dataclass


@dataclass
class UserDataDTO:
    user_id: str
    email: str
    username: str
    first_name: str
    last_name: str
    roles: list[str]
    is_active: bool
    exp: int


@dataclass
class AuthorizationDataDTO:
    email: str
    password: str
