import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_create(client: AsyncClient):
    response = await client.post(
        "/api/v1/polls",
        json={
            "question": "What's your favorite color?",
            "options": [{"text": "Red"}, {"text": "Blue"}, {"text": "Green"}],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["question"] == "What's your favorite color?"
    assert len(data["options"]) == 3
    for text, option in zip(["Red", "Blue", "Green"], data["options"]):
        assert option["text"] == text
