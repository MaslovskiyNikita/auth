from fastapi import FastAPI

from src.auth.main.dependencies.container import container
from src.auth.presentation.api.rest.v1.exeption_handler.user_exeptions import (
    init_exeptions_handlers,
)
from src.auth.presentation.api.rest.v1.routers.users import router as users_router

app = FastAPI()

init_exeptions_handlers(app)

app.include_router(users_router)
