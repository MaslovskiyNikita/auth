from dataclasses import dataclass


@dataclass
class UserDataDTO:
    email: str
    username: str
    first_name: str
    last_name: str
    roles: list
