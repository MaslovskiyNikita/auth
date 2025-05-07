from pydantic import UUID4, BaseModel, Field

from src.auth.presentation.api.rest.v1.schemas.types import EmailPydantic


class UserBaseSchema(BaseModel):
    email: EmailPydantic
    username: str
    first_name: str
    last_name: str


class UserCreateSchema(BaseModel):
    email: EmailPydantic
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)


class UserResponseSchema(UserBaseSchema):
    id: UUID4

    class Config:
        from_attributes = True
