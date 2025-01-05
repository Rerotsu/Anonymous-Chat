import pytest
from httpx import ASGITransport, AsyncClient

from anonymous_chat.main import app


@pytest.mark.parametrize("email,phone_number,password,confirm_password, status_code", [
    ("testik1@mail.ru", "+79877877933", "password1", "password1", 200),
    ("testik2@mail.ru", "+79877877934", "password2", "password22", 400),
    ("testik3@mail.ru", "+79098087733", "password3", "password3", 200),
    ("testik4@mail.ru", "+79877870000007936", "password", "password", 200),
    ("testik5@mail.ru", "str", "password", "password", 422),
    ("testik1@mail.ru", "+79877877939", "password", "password", 409),
    ("strstrstr", "+79877877940", "password", "password", 422),
])
@pytest.mark.asyncio
async def test_register_user(email, phone_number, confirm_password, password, status_code):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/user/auth/register", json={
            "email": email,
            "phone_number": phone_number,
            "password": password,
            "confirm_password": confirm_password,
        })
        assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("testik1@mail.ru", "password", 200),
    ("testik1@mail.ru", "password9999", 400),
    ("testik32@mail.ru", "password", 400),
    ("testik1", "password", 422),
])
@pytest.mark.asyncio
async def test_login_user(email, password, status_code):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/user/auth/login", json={
            "email": email,
            "password": password
        })
        assert response.status_code == status_code
