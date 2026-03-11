"""
Shared pytest fixtures available to all test modules.
"""

import pytest
from utils.api_client import APIClient
from utils.logger import get_logger

log = get_logger("conftest")


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    """Session-scoped unauthenticated API client."""
    log.info("Creating session-scoped API client.")
    return APIClient()


@pytest.fixture(scope="session")
def authenticated_client(api_client: APIClient) -> APIClient:
    """
    Session-scoped API client pre-loaded with a valid Bearer token
    obtained via the /login endpoint.
    """
    log.info("Authenticating client via /login...")
    from config.settings import settings

    response = api_client.post(
        "/login",
        json={"email": settings.LOGIN_EMAIL, "password": settings.LOGIN_PASSWORD},
    )
    assert response.status_code == 200, (
        f"Login failed during fixture setup: {response.text}"
    )
    token = response.json().get("token")
    assert token, "No token returned from /login"

    client = APIClient(token=token)
    log.info("Authenticated client ready. Token: %s…", token[:10])
    return client


@pytest.fixture(scope="function")
def fresh_client() -> APIClient:
    """Function-scoped unauthenticated client (no shared state)."""
    return APIClient()
