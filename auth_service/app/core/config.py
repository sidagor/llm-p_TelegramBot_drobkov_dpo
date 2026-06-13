from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """
    Конфигурация приложения.
    """

    app_name: str
    env: str

    jwt_secret: str
    jwt_alg: str
    access_token_expire_minutes: int

    sqlite_path: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()