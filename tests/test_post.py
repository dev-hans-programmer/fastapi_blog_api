import pytest
from httpx import AsyncClient


async def create_post(title: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/posts/", json={"title": title})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test Post", async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    response = await async_client.post("/posts/", json={"title": "Test title"})
    assert response.status_code == 201
    assert {"id": 1, "title": "Test title"}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient):
    response = await async_client.post("/posts/", json={})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    # the created post is due to the fixture
    response = await async_client.get("/posts/")
    assert len(response.json()) == 1
    assert response.json() == [created_post]
