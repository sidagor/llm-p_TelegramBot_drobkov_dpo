from jose import jwt
import pytest

from app.core.config import settings
from app.core.jwt import decode_and_validate
from app.core.exceptions import (
    InvalidTokenError,
)


def test_decode_valid_token():
    """
    Проверяет корректное декодирование
    валидного JWT токена.
    """
    token = jwt.encode(
        {
            "sub": "123",
            "role": "user",
        },
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )

    payload = decode_and_validate(token)

    assert payload["sub"] == "123"
    assert payload["role"] == "user"


def test_decode_invalid_token():
    """
    Проверяет, что невалидная строка
    вызывает ошибку InvalidTokenError.
    """
    with pytest.raises(InvalidTokenError):
        decode_and_validate("this_is_not_jwt")

def test_token_without_sub():
    """
    Проверяет, что JWT без обязательного
    поля sub считается невалидным.
    """
    token = jwt.encode(
        {
            "role": "user",
        },
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )

    with pytest.raises(InvalidTokenError):
        decode_and_validate(token)        