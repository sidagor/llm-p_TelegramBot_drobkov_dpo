
class BotServiceError(Exception):
    """
    Базовое исключение Bot Service.
    """
    pass


class InvalidTokenError(BotServiceError):
    """
    JWT токен невалиден.
    """
    pass


class TokenExpiredError(BotServiceError):
    """
    JWT токен истёк.
    """
    pass


class ExternalServiceError(BotServiceError):
    """
    Ошибка внешнего сервиса (OpenRouter).
    """
    pass
