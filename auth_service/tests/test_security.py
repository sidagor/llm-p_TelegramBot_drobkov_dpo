import pytest
from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings
from app.core.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)


def test_hash_password():
    """
    Проверяет, что пароль корректно хешируется
    и может быть успешно проверен.
    """
    password = "secret123"

    password_hash = hash_password(password)

    assert password_hash != password
    assert verify_password(password, password_hash) is True


def test_verify_password_invalid():
    """
    Проверяет, что неверный пароль
    не проходит проверку.
    """
    password_hash = hash_password("secret123")

    assert verify_password(
        "wrong_password",
        password_hash,
    ) is False


def test_create_and_decode_token():
    """
    Проверяет создание JWT токена
    и корректное извлечение payload.
    """
    token = create_access_token(
        user_id=1,
        role="user",
    )

    payload = decode_token(token)

    assert payload["sub"] == "1"
    assert payload["role"] == "user"

    assert "iat" in payload
    assert "exp" in payload


def test_invalid_token():
    """
    Проверяет, что невалидный JWT токен
    вызывает исключение InvalidTokenError.
    """
    with pytest.raises(InvalidTokenError):
        decode_token("invalid.jwt.token")


def test_expired_token():
    """
    Проверяет, что просроченный JWT токен
    вызывает исключение TokenExpiredError.
    """
    payload = {
        "sub": "1",
        "role": "user",
        "iat": datetime.now(timezone.utc) - timedelta(hours=2),
        "exp": datetime.now(timezone.utc) - timedelta(hours=1),
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )

    with pytest.raises(TokenExpiredError):
        decode_token(token)
