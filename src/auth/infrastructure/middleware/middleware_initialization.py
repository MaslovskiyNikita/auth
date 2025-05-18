from fastapi import FastAPI

from src.auth.infrastructure.middleware.jwt_validation import JWTAuthMiddleware


def init_middleware(app: FastAPI):
    app.add_middleware(JWTAuthMiddleware)
