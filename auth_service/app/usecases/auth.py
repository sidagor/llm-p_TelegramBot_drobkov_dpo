from app.repositories.users import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError,
)


class AuthUseCase:
    """
    Бизнес-логика аутентификации пользователей.
    """

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo
    
    async def register(self, email: str, password: str):
        """
        Регистрация нового пользователя.
        """
        existing_user = await self._user_repo.get_by_email(email)

        if existing_user:
            raise UserAlreadyExistsError()

        password_hash = hash_password(password)

        user = await self._user_repo.create(
            email=email,
            password_hash=password_hash,
        )

        return user
    
    async def login(self, email: str, password: str) -> str:
        """
        Аутентификация пользователя и выдача JWT.
        """
        user = await self._user_repo.get_by_email(email)

        if not user:
            raise InvalidCredentialsError()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        
        token = create_access_token(
            user_id=user.id,
            role=user.role,
        )

        return token
    
    async def me(self, user_id: int):
        """
        Получить профиль пользователя.
        """
        user = await self._user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundError()

        return user