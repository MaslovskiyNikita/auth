from dataclasses import dataclass


@dataclass
class UserDataDTO:
    email: str
    username: str
    first_name: str
    last_name: str
    roles: list[str]


@dataclass
class AuthorizationDataDTO:
    email: str
    password: str
