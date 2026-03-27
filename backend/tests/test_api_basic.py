import asyncio
import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app


@pytest.mark.asyncio
async def test_root_ok():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		resp = await ac.get("/")
	assert resp.status_code == status.HTTP_200_OK
	assert resp.json().get("status") == "ok"
















