from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase
from app.core.security import decode_token

from app.core.exceptions import (
    InvalidTokenError,
    UserNotFoundError,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



async def get_db() -> AsyncSession:
    """Dependency для получения асинхронной сессии базы данных."""
    async with AsyncSessionLocal() as session:
        yield session



def get_user_repo(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    """Dependency для получения репозитория пользователей."""
    return UserRepository(session)

def get_auth_usecase(
    user_repo: UserRepository = Depends(get_user_repo),
) -> AuthUseCase:
    """Dependency для бизнес-логики аутентификации."""
    return AuthUseCase(user_repo)

def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> int:
    """Dependency для получения текущего пользователя из JWT."""

    payload = decode_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise InvalidTokenError()

    return int(user_id)
    
async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    user_repo: UserRepository = Depends(get_user_repo),
):
    """
    Dependency для получения текущего пользователя.
    """
    user = await user_repo.get_by_id(user_id)

    if not user:
        raise UserNotFoundError()

    return user    