import httpx

from app.core.config import settings
from app.core.exceptions import ExternalServiceError


class OpenRouterClient:
    """
    Клиент для работы с OpenRouter API.
    """

    async def generate(self, prompt: str) -> str:
        """
        Отправляет запрос в OpenRouter и возвращает ответ модели.
        """
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        }

        payload = {
            "model": settings.openrouter_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{settings.openrouter_base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except httpx.TimeoutException as e:
            raise ExternalServiceError(
                "OpenRouter request timeout"
            ) from e

        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(
                f"OpenRouter returned status {e.response.status_code}"
            ) from e

        except httpx.RequestError as e:
            raise ExternalServiceError(
                "OpenRouter connection error"
            ) from e

        except (KeyError, IndexError) as e:
            raise ExternalServiceError(
                "Invalid OpenRouter response format"
            ) from e