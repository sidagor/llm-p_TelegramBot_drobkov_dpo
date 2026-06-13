# app/bot/factory.py

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession

from app.core.config import settings


def create_bot() -> Bot:
    if settings.telegram_proxy:
        session = AiohttpSession(
            proxy=settings.telegram_proxy,
        )

        return Bot(
            token=settings.telegram_bot_token,
            session=session,
        )

    return Bot(
        token=settings.telegram_bot_token,
    )