from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle приложения.Создаёт таблицы в базе данных при старте.
    """    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    

def create_app() -> FastAPI:
    """
    Фабрика создания FastAPI приложения.
    """
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )
    
    app.include_router(router)
        
    @app.get("/health")
    async def health():
        """
        Технический endpoint для проверки состояния сервера.
        """
        return {
            "status": "ok",
            "env": settings.env,
        }

    return app


app = create_app()