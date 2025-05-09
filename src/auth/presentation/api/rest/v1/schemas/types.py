from typing import Any

from pydantic import BaseModel, GetCoreSchemaHandler, TypeAdapter
from pydantic_core import CoreSchema, core_schema


class EmailPydantic(str):

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls.validate, handler(str))

    @classmethod
    def validate(cls, email: str) -> "EmailPydantic":
        if "@" not in email:
            raise ValueError("Invalid email format")
        return str(email)  # type: ignore [return-value]
