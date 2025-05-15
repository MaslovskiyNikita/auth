import datetime

import jwt
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.inspection import inspect

from src.auth.application.repositories.verificatation.verification_token import (
    TokenServiceABC,
)
from src.auth.infrastructure.db.models.user import UserDB
from src.auth.main.settings.settings import settings


class ItsDangerousTokenService(TokenServiceABC):
    def __init__(self, secret_key: str, salt: str, max_age: int = 3600):
        self.serializer = URLSafeTimedSerializer(secret_key)
        self.salt = salt
        self.max_age = max_age

    def generate_token(self, data: str) -> str:
        return self.serializer.dumps(data, salt=self.salt)

    def validate_token(self, token: str) -> str:
        return self.serializer.loads(token, salt=self.salt, max_age=self.max_age)

    def create_jwt_token(self, data: UserDB, expires) -> str:  # type: ignore[override]
        to_encode = data.to_dict()
        expire = datetime.datetime.now() + datetime.timedelta(minutes=expires)
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            settings.token_secret_key,
            algorithm=settings.jwt_config.jwt_hashing,
        )

    def decode_jwt_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            settings.token_secret_key,
            algorithm=settings.jwt_config.jwt_hashing,
        )
