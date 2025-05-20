from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends

from src.auth.application.use_cases.refresh_jwt_tokens import RefreshJWTTokensUseCase
from src.auth.main.dependencies.container import Container

router = APIRouter(prefix="/tokens", tags=["Users"])


@router.post("/refresh")  # type: ignore[misc]
@inject  # type: ignore[misc]
async def refresh(
    refreshToken: str = Body(..., embed=True, alias="refreshToken"),
    use_case: RefreshJWTTokensUseCase = Depends(
        Provide[Container.refresh_jwt_tokens_use_case]
    ),
):
    tokens = await use_case(refreshToken)
    return {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
    }
