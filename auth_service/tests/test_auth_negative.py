import pytest


@pytest.mark.asyncio
async def test_duplicate_registration(client):
    """
    Проверяет, что повторная регистрация
    пользователя с тем же email запрещена.
    """

    payload = {
        "email": "duplicate@example.com",
        "password": "secret123",
    }

    await client.post(
        "/auth/register",
        json=payload,
    )

    response = await client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """
    Проверяет, что логин с неверным паролем
    возвращает ошибку авторизации.
    """

    await client.post(
        "/auth/register",
        json={
            "email": "wrong@example.com",
            "password": "secret123",
        },
    )

    response = await client.post(
        "/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "badpassword",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_without_token(client):
    """
    Проверяет, что доступ к /auth/me
    без JWT токена запрещён.
    """

    response = await client.get("/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_invalid_token(client):
    """
    Проверяет, что доступ к /auth/me
    с невалидным JWT токеном запрещён.
    """

    response = await client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid_token",
        },
    )

    assert response.status_code == 401