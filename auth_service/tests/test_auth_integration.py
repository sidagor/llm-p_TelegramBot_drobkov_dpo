import pytest


@pytest.mark.asyncio
async def test_register_login_me(client):
    """
    Интеграционный тест полного сценария аутентификации.

    Проверяет:
    - регистрацию нового пользователя;
    - получение JWT через /auth/login;
    - доступ к защищённому endpoint /auth/me;
    - корректность данных пользователя в ответе.

    Использует тестовую SQLite in-memory через override get_db.
    """

    register_response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "secret123",
        },
    )

    assert register_response.status_code == 200

    login_response = await client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "secret123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    me_response = await client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert me_response.status_code == 200

    data = me_response.json()

    assert data["email"] == "test@example.com"
    assert data["role"] == "user"