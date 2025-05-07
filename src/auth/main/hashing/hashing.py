import hashlib

from src.auth.main.settings.settings import settings


def hashed_password(password: str) -> str:

    salt = settings.salt.encode() if isinstance(settings.salt, str) else settings.salt

    hashed_bytes = hashlib.pbkdf2_hmac(
        settings.hashing_type, password.encode("utf-8"), salt, settings.iterations
    )

    return hashed_bytes.hex()
