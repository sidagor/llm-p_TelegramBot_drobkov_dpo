import asyncio

from app.bot.factory import create_bot
from app.core.exceptions import ExternalServiceError
from app.infra.celery_app import celery_app
from app.services.openrouter_client import OpenRouterClient


@celery_app.task(name="llm_request")
def llm_request(
    tg_chat_id: int,
    prompt: str,
):
    """
    Обрабатывает запрос к LLM и отправляет ответ
    пользователю в Telegram.
    """

    async def _run():
        client = OpenRouterClient()

        response = await client.generate(prompt)

        bot = create_bot()

        try:
            await bot.send_message(
                chat_id=tg_chat_id,
                text=response,
            )
        finally:
            await bot.session.close()

    try:
        asyncio.run(_run())

    except ExternalServiceError:
        raise