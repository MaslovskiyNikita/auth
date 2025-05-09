import hashlib

from src.auth.application.repositories.hashing.hashing import PasswordHasherABC
from src.auth.main.settings.settings import settings


class PasswordHasher(PasswordHasherABC):
    def hash(self, password: str) -> str:

        salt = (
            settings.salt.encode() if isinstance(settings.salt, str) else settings.salt
        )

        hashed_bytes = hashlib.pbkdf2_hmac(
            settings.hashing_type, password.encode("utf-8"), salt, settings.iterations
        )

        return hashed_bytes.hex()
