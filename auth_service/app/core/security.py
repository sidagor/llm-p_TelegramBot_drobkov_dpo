from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext

from app.core.config import settings

from app.core.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Хеширует пароль пользователя.
    """
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """
    Проверяет пароль пользователя.
    """
    return pwd_context.verify(password, password_hash)


def create_access_token(user_id: int, role: str) -> str:
    """
    Создаёт JWT access token.
    """
    now = datetime.now(timezone.utc)

    payload: Dict[str, Any] = {
        "sub": str(user_id),  
        "role": role,
        "iat": now,  
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )

    return token


def decode_token(token: str) -> Dict[str, Any]:
    """
    Декодирует и валидирует JWT токен.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )
        return payload

    except ExpiredSignatureError:
        raise TokenExpiredError()

    except JWTError:
        raise InvalidTokenError()