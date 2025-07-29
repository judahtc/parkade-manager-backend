import pytest
from fastapi import HTTPException
from httpx import RequestError
import httpx
from main import get_user_gists


@pytest.mark.asyncio
async def test_get_user_gists_success(monkeypatch):
    # Mock successful response data
    mock_gists = [
        {
            "id": "1",
            "description": "Test Gist 1",
            "html_url": "https://gist.github.com/octocat/1"
        },
        {
            "id": "2",
            "description": None,  # Testing null description
            "html_url": "https://gist.github.com/octocat/2"
        }
    ]

    class MockResponse:
        status_code = 200

        def json(self):
            return mock_gists

    class MockAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, url):
            return MockResponse()

    # Patch httpx.AsyncClient
    monkeypatch.setattr(httpx, "AsyncClient", MockAsyncClient)

    # Test the function
    result = await get_user_gists("octocat")

    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[0]["description"] == "Test Gist 1"
    assert result[0]["url"] == "https://gist.github.com/octocat/1"
    # Testing default description
    assert result[1]["description"] == "No description"


@pytest.mark.asyncio
async def test_get_user_gists_user_not_found(monkeypatch):
    class MockResponse:
        status_code = 404

        def json(self):
            return {"message": "Not Found"}

    class MockAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, url):
            return MockResponse()

    monkeypatch.setattr(httpx, "AsyncClient", MockAsyncClient)

    with pytest.raises(HTTPException) as exc_info:
        await get_user_gists("nonexistent-user")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
async def test_get_user_gists_api_error(monkeypatch):
    class MockAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, url):
            raise RequestError("Connection error")

    monkeypatch.setattr(httpx, "AsyncClient", MockAsyncClient)

    with pytest.raises(HTTPException) as exc_info:
        await get_user_gists("octocat")

    assert exc_info.value.status_code == 500
    assert "Error connecting to GitHub API" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_user_gists_other_error(monkeypatch):
    class MockResponse:
        status_code = 403

        def json(self):
            return {"message": "Rate limit exceeded"}

    class MockAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, url):
            return MockResponse()

    monkeypatch.setattr(httpx, "AsyncClient", MockAsyncClient)

    with pytest.raises(HTTPException) as exc_info:
        await get_user_gists("octocat")

    assert exc_info.value.status_code == 403
    assert exc_info.value.json() == {"message": "Rate limit exceeded"}
