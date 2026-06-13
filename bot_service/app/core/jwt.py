from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError

from app.core.config import settings
from app.core.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
)


def decode_and_validate(token: str) -> dict:
    """
    Проверяет JWT токен и возвращает payload.

    Проверяет:
    - корректность подписи;
    - срок действия токена (exp).

    Raises:
        ValueError: если токен невалиден или истёк.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )
        
        if "sub" not in payload:
            raise InvalidTokenError()

        return payload

    except ExpiredSignatureError:
        raise TokenExpiredError()

    except JWTError:
        raise InvalidTokenError()
    