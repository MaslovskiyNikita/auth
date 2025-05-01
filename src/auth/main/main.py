from fastapi import FastAPI

from src.auth.main.dependencies import get_db
from src.auth.presentation.api.routers.users import router as users_router

app = FastAPI()
app.include_router(users_router)
