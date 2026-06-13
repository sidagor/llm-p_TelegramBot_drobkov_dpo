from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """
    Схема запроса для регистрации пользователя.
    """
    
    email: EmailStr
    password: str = Field(
        min_length=6,
        max_length=128,
        description="User password (6-128 chars)",
    )


class TokenResponse(BaseModel):
    """
    Схема ответа с JWT токеном.
    """

    access_token: str
    token_type: str = "bearer"