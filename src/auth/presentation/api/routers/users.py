from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.application.repositories.user_repository import UserRepositoryABC
from src.auth.application.use_cases.user_use_case import CreateUserUseCase
from src.auth.domain.entity.user import User
from src.auth.main.dependencies import get_user_repository
from src.auth.presentation.api.schemas.user import UserModel

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")  # type: ignore [misc]
async def create_user(
    user_data: UserModel, repo: UserRepositoryABC = Depends(get_user_repository)
):
    try:
        use_case = CreateUserUseCase(repo)
        return await use_case(user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
