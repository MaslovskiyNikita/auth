from dataclasses import dataclass
from enum import StrEnum


@dataclass
class PermissionPool(StrEnum):
    TASK_CREATE = "user:task_create"
    TASK_READ = "user:task_read"
    TASK_UPDATE = "user:task_update"
    TASK_PARTIAL_UPDATE = "user:partial_update"
    TASK_DESTROY = "user:task_destroy"
    TASK_ADD_MEMBER = "user:task_add_member"
    TASK_UPDATE_MEMBER = "user:task_update_member"
    TASK_DELETE_MEMBER = "user:task_delete_member"

    PROJECT_CREATE = "user:project_create"
    PROJECT_READ = "user:project_read"
    PROJECT_UPDATE = "user:project_update"
    PROJECT_PARTIAL_UPDATE = "user:project_partial_update"
    PROJECT_DESTROY = "user:project_destroy"
    PROJECT_ADD_MEMBER = "user:project_add_member"
    PROJECT_UPDATE_MEMBER = "user:project_update_member"
    PROJECT_DELETE_MEMBER = "user:project_delete_member"
