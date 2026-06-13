from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """
    Базовый класс для всех HTTP-исключений приложения.

    Позволяет создавать доменные исключения с заранее
    определёнными HTTP-статусами и сообщениями об ошибках.
    """

    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )


class UserAlreadyExistsError(BaseHTTPException):
    """
    Пользователь с указанным email уже существует.
    """

    def __init__(self):
        super().__init__(
            status.HTTP_409_CONFLICT,
            "Email already registered",
        )


class InvalidCredentialsError(BaseHTTPException):
    """
    Неверные учётные данные пользователя.

    Возникает при ошибке аутентификации,
    если email или пароль указаны неверно.
    """

    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid credentials",
        )


class InvalidTokenError(BaseHTTPException):
    """
    JWT-токен имеет некорректный формат
    или содержит неверную подпись.
    """

    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid token",
        )


class TokenExpiredError(BaseHTTPException):
    """
    Срок действия JWT-токена истёк.
    """

    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "Token expired",
        )


class UserNotFoundError(BaseHTTPException):
    """
    Пользователь не найден в системе.
    """

    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            "User not found",
        )


class PermissionDeniedError(BaseHTTPException):
    """
    У пользователя недостаточно прав
    для выполнения запрошенной операции.
    """

    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            "Permission denied",
        )
        