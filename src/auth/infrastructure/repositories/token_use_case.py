import datetime

import jwt
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.inspection import inspect

from src.auth.application.repositories.verificatation.verification_token import (
    TokenServiceABC,
)
from src.auth.infrastructure.db.models.user import UserDB
from src.auth.main.settings.settings import AppSettings


class ItsDangerousTokenService(TokenServiceABC):
    def __init__(self, settings: AppSettings, max_age: int = 3600):
        self.serializer = URLSafeTimedSerializer(settings.token_secret_key)
        self.salt = settings.salt
        self.max_age = max_age
        self.settings = settings

    def generate_token(self, data) -> str:
        return self.serializer.dumps(data, salt=self.salt)

    def validate_token(self, token: str) -> str:
        return self.serializer.loads(token, salt=self.salt, max_age=self.max_age)

    def create_jwt_token(self, data: dict, expires) -> str:  # type: ignore[override]

        expire = datetime.datetime.now() + datetime.timedelta(minutes=expires)
        data.update({"exp": expire})
        return jwt.encode(
            data,
            self.settings.token_secret_key,
            algorithm=self.settings.jwt_config.jwt_hashing,
        )

    def decode_jwt_token(self, token: str) -> dict:  # type: ignore[override]
        return jwt.decode(
            token,
            self.settings.token_secret_key,
            algorithms=[self.settings.jwt_config.jwt_hashing],
            options={"verify_exp": True},
        )
