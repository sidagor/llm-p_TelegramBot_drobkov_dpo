from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_usecase, get_current_user_id
from app.usecases.auth import AuthUseCase
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic



router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic)
async def register(
    data: RegisterRequest,
    usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """
    Регистрация нового пользователя.
    """
    user = await usecase.register(
        email=data.email,
        password=data.password,
    )
    
    return user

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """
    Аутентификация пользователя и получение JWT токена.
    """
    token = await usecase.login(
        email=form_data.username,
        password=form_data.password,
    )

    return {
            "access_token": token,
            "token_type": "bearer",
    }

    
@router.get("/me", response_model=UserPublic)
async def me(
    user_id: int = Depends(get_current_user_id),
    usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """
    Получение профиля текущего пользователя.
    """

    user = await usecase.me(user_id)

    return user

   