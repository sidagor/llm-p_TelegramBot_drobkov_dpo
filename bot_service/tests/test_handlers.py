import pytest
from unittest.mock import Mock, AsyncMock

from app.bot.handlers import (
    save_token,
    handle_message,
)


@pytest.fixture
def fake_message():
    """
    Тестовое Telegram-сообщение.

    Используется для проверки обработчиков без
    реального Telegram API.
    """
    message = Mock()

    message.chat.id = 123
    message.from_user.id = 777

    message.answer = AsyncMock()

    return message


@pytest.mark.asyncio
async def test_save_token(
    fake_message,
    fake_redis,
):
    """
    Проверяет сохранение JWT токена в Redis
    через команду /token.
    """
    fake_message.text = "/token jwt123"

    await save_token(fake_message)

    token = await fake_redis.get(
        "user_token:777"
    )

    assert token.decode() == "jwt123"

    fake_message.answer.assert_awaited_once_with(
        "Токен успешно сохранён."
    )


@pytest.mark.asyncio
async def test_message_without_token(
    fake_message,
    mocker,
):
    """
    Проверяет, что без сохранённого JWT токена
    задача в Celery не отправляется и пользователь
    получает сообщение об авторизации.
    """
     
    fake_message.text = "Hello"

    delay_mock = mocker.patch(
        "app.bot.handlers.llm_request.delay"
    )

    await handle_message(fake_message)

    delay_mock.assert_not_called()

    fake_message.answer.assert_awaited_once()

    assert "не авторизованы" in (
        fake_message.answer.await_args.args[0]
    )


@pytest.mark.asyncio
async def test_message_with_token(
    fake_message,
    fake_redis,
    mocker,
):
    """
    Проверяет, что при наличии валидного JWT
    создаётся Celery-задача и пользователю
    отправляется подтверждение.
    """
    fake_message.text = "Hello LLM"

    await fake_redis.set(
        "user_token:777",
        "valid-token",
    )

    mocker.patch(
        "app.bot.handlers.decode_and_validate",
        return_value={
            "sub": "1",
        },
    )

    delay_mock = mocker.patch(
        "app.bot.handlers.llm_request.delay"
    )

    await handle_message(fake_message)

    delay_mock.assert_called_once_with(
        tg_chat_id=123,
        prompt="Hello LLM",
    )

    fake_message.answer.assert_awaited_once_with(
        "Запрос принят в обработку."
    )