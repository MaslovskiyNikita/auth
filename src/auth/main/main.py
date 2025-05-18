from fastapi import FastAPI

from src.auth.infrastructure.middleware.middleware_manager import middleware_manager
from src.auth.main.dependencies.container import container
from src.auth.presentation.api.rest.v1.exeption_handler.user_exeptions import (
    init_exeptions_handlers,
)
from src.auth.presentation.api.rest.v1.routers.roles import router as roles_router
from src.auth.presentation.api.rest.v1.routers.tokens import router as tokens_router
from src.auth.presentation.api.rest.v1.routers.users import router as users_router

app = FastAPI()

init_exeptions_handlers(app)
middleware_manager.init_middleware(app)

app.include_router(users_router)
app.include_router(tokens_router)
app.include_router(roles_router)
