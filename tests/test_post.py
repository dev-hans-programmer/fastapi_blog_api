import pytest
from httpx import AsyncClient


async def create_post(title: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/posts/", json={"title": title})
    return response.json()


async def create_comment(post_id: int, title: str, async_client: AsyncClient) -> dict:
    response = await async_client.post(
        "/posts/comment", json={"post_id": post_id, "title": title}
    )
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test Post", async_client)


@pytest.fixture
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment(created_post["id"], "Test Comment", async_client)


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


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    response = await async_client.post(
        "/posts/comment", json={"post_id": created_post["id"], "title": "Test Comment"}
    )
    assert response.status_code == 201
    assert {"post_id": 1, "title": "Test Comment"}.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_all_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/posts/comment/{created_post["id"]}")
    print(f"LENGTH {len(response.json()["comments"])}")

    assert response.json()["comments"] == [created_comment]
