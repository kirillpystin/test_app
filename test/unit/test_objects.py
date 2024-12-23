import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from app import app, load_store_from_file
from app.configs.storage import store
from app.handlers.store_handlers import save_store_to_file


@pytest.mark.asyncio
async def test_create_item():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.put(
            "/objects/test", json={"data": {"test": "test"}, "expires": 10}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Item stored successfully."}
        assert "test" in store


@pytest.mark.asyncio
async def test_get_item():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.put(
            "/objects/test", json={"data": {"test1": "test1"}, "expires": 100}
        )
        response = await client.get("/objects/test")
        assert response.status_code == 200
        assert response.json() == {"test1": "test1"}


@pytest.mark.asyncio
async def test_liveness():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health/liveness")
        assert response.status_code == 200
        assert response.json() == {"status": "alive"}


@pytest.mark.asyncio
async def test_readiness():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health/readiness")
        assert response.status_code == 503

        await save_store_to_file()
        response = await client.get("/health/readiness")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"


@pytest.mark.asyncio
async def test_metrics():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/metrics")
        assert response.status_code == 200
        assert "items_stored" in response.text
        assert "active_items" in response.text


@pytest.mark.asyncio
async def test_save_and_load_store():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.put("/objects/test", json={"data": {"test1": "test1"}})
        await save_store_to_file()
        store.clear()
        await load_store_from_file()
        assert "test" in store
        assert store["test"]["value"] == {"test1": "test1"}


@pytest.mark.asyncio
async def test_get_expired_item():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.put(
            "/objects/test", json={"data": {"test1": "test1"}, "expires": 1}
        )
        await asyncio.sleep(2)
        response = await client.get("/objects/test")
        assert response.status_code == 404
        assert response.json()["detail"] == "Item expired"
