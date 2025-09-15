import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_health_check(client: AsyncClient):
    response = await client.get("/api/v1/health")

    assert response.status_code == 200
