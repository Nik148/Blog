from httpx import AsyncClient
from sqlalchemy import select
import pytest
from typing import List
from .conftest import async_session_maker
from app.database.model import User


@pytest.mark.asyncio
async def test_registration(ac: AsyncClient):
    response = await ac.post("/registration", json={
        "login": "deadpool135",
        "password": "1234"
    })

    assert response.status_code == 201

    response = await ac.post("/registration", json={
        "login": "deadpool135",
        "password": "12345"
    })
    assert response.status_code == 400

    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.login == "deadpool135"))
        user: User = user.scalar()
        assert user


@pytest.mark.asyncio
async def test_login(ac: AsyncClient):
    response = await ac.post("/login", json={
        "login": "deadpool135",
        "password": "12"
    })

    assert response.status_code == 400

    response = await ac.post("/login", json={
        "login": "spider_man",
        "password": "piter_parker"
    })

    assert response.status_code == 400

    response = await ac.post("/login", json={
        "login": "deadpool135",
        "password": "1234"
    })
    assert response.status_code == 200
    assert response.json().get("access_token")
