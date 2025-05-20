from src.auth.application.exeptions.base_exeption import BaseApplicationException


class PermissionNotExistsErorr(BaseApplicationException):
    default_message = "Permission not exists"
