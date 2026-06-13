import pytest
import respx
from httpx import Response

from app.services.openrouter_client import OpenRouterClient
from app.core.exceptions import ExternalServiceError



@pytest.mark.asyncio
async def test_generate_success():
    """
    Проверяет успешный запрос к OpenRouter
    и корректное извлечение ответа модели.
    """
    client = OpenRouterClient()

    with respx.mock(assert_all_called=True) as mock:
        route = mock.post(
            "https://openrouter.ai/api/v1/chat/completions"
        ).mock(
            return_value=Response(
                200,
                json={
                    "choices": [
                        {
                            "message": {
                                "content": "Hello from OpenRouter"
                            }
                        }
                    ]
                },
            )
        )

        result = await client.generate("Hello")

        assert result == "Hello from OpenRouter"
        assert route.called

@pytest.mark.asyncio
async def test_generate_http_error():
    """
    Проверяет обработку HTTP ошибки,
    возвращаемой OpenRouter API.
    """
    client = OpenRouterClient()

    with respx.mock:
        respx.post(
            "https://openrouter.ai/api/v1/chat/completions"
        ).mock(
            return_value=Response(500)
        )

        with pytest.raises(ExternalServiceError):
            await client.generate("Hello")

@pytest.mark.asyncio
async def test_generate_invalid_response():
    """
    Проверяет обработку некорректного
    формата ответа OpenRouter API.
    """
    client = OpenRouterClient()

    with respx.mock:
        respx.post(
            "https://openrouter.ai/api/v1/chat/completions"
        ).mock(
            return_value=Response(
                200,
                json={"foo": "bar"},
            )
        )

        with pytest.raises(ExternalServiceError):
            await client.generate("Hello")

