from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.core.jwt import decode_and_validate
from app.core.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
)
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Стартовая команда бота.
    """
    await message.answer(
        "Привет!\n\n"
        "Для работы с ботом получите JWT в Auth Service "
        "и отправьте его командой:\n\n"
        "/token <jwt>"
    )


@router.message(Command("token"))
async def save_token(message: Message):
    """
    Сохраняет JWT пользователя в Redis.
    """
    parts = message.text.split(maxsplit=1)

    if len(parts) != 2:
        await message.answer(
            "Использование:\n/token <jwt>"
        )
        return

    token = parts[1]

    redis = get_redis()

    await redis.set(
        f"user_token:{message.from_user.id}",
        token,
    )

    await message.answer(
        "Токен успешно сохранён."
    )


@router.message()
async def handle_message(message: Message):
    """
    Обрабатывает сообщения пользователя.
    Проверяет JWT и отправляет задачу в Celery.
    """
    redis = get_redis()

    token = await redis.get(
        f"user_token:{message.from_user.id}"
    )

    if not token:
        await message.answer(
            "Вы не авторизованы.\n"
            "Получите JWT в Auth Service и отправьте:\n"
            "/token <jwt>"
        )
        return

    try:
        decode_and_validate(token)

    except TokenExpiredError:
        await message.answer(
            "Срок действия токена истёк.\n"
            "Авторизуйтесь заново."
        )
        return

    except InvalidTokenError:
        await message.answer(
            "JWT токен недействителен.\n"
            "Получите новый токен в Auth Service."
        )
        return

    llm_request.delay(
        tg_chat_id=message.chat.id,
        prompt=message.text,
    )

    await message.answer(
        "Запрос принят в обработку."
    )