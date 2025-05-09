from itsdangerous import URLSafeTimedSerializer

from src.auth.application.repositories.verificatation.verification_token import (
    TokenServiceABC,
)


class ItsDangerousTokenService(TokenServiceABC):
    def __init__(self, secret_key: str, salt: str, max_age: int = 3600):
        self.serializer = URLSafeTimedSerializer(secret_key)
        self.salt = salt
        self.max_age = max_age

    def generate_token(self, data: str) -> str:
        return self.serializer.dumps(data, salt=self.salt)

    def validate_token(self, token: str) -> str:
        return self.serializer.loads(token, salt=self.salt, max_age=self.max_age)
