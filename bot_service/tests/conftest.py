import pytest
import fakeredis.aioredis
import pytest_asyncio

from app.bot import handlers


@pytest_asyncio.fixture
async def fake_redis():
    """
    Тестовый Redis.
    """
    redis = fakeredis.aioredis.FakeRedis()

    yield redis

    await redis.flushall()
    await redis.aclose()


@pytest.fixture(autouse=True)
def patch_redis(fake_redis, monkeypatch):
    """
    Подменяет get_redis в handlers.py
    на тестовый Redis.
    """

    def _get_redis():
        return fake_redis

    monkeypatch.setattr(
        handlers,
        "get_redis",
        _get_redis,
    )