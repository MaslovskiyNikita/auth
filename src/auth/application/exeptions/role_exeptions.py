from src.auth.application.exeptions.base_exeption import BaseApplicationException


class RoleAlreadyExistsErorr(BaseApplicationException):
    default_message = "Role already exists"


class RoleNotExistsError(BaseApplicationException):
    default_message = "Role not exsists"
