from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

"""Настройка подключения к базе данных SQLite."""

DATABASE_URL = f"sqlite+aiosqlite:///{settings.sqlite_path}"


engine = create_async_engine(
    DATABASE_URL,
    echo=False,  
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)