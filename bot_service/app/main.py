from fastapi import FastAPI

from app.core.config import settings


def create_app() -> FastAPI:
    """
    Фабрика создания FastAPI приложения Bot Service.
    """
    app = FastAPI(
        title=settings.app_name,
    )

    @app.get("/health")
    async def health():
        """
        Проверка состояния сервиса.
        """
        return {
            "status": "ok",
            "env": settings.env,
        }

    return app


app = create_app()