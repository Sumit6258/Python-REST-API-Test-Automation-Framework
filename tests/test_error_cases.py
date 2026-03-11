"""
Test suite: Error Handling & Negative Tests (DummyJSON)

DummyJSON error shapes:
  - 404: {"message": "User with id 'X' not found"}
  - 400 auth: {"message": "Invalid credentials"}
"""

import pytest
from utils.api_client import APIClient
from utils.helpers import assert_status_code, assert_response_contains_key


@pytest.fixture(scope="module")
def client() -> APIClient:
    return APIClient()


# ------------------------------------------------------------------ #
# 404 – Not Found                                                      #
# ------------------------------------------------------------------ #

@pytest.mark.errors
class Test404NotFound:
    """Verify 404 responses for unknown resources."""

    def test_get_nonexistent_user_returns_404(self, client: APIClient) -> None:
        response = client.get("/users/9999")
        assert_status_code(response, 404)

    def test_get_nonexistent_user_has_message(self, client: APIClient) -> None:
        response = client.get("/users/9999")
        body = response.json()
        assert "message" in body, f"Expected 'message' key in 404 body, got: {body}"

    def test_get_user_id_zero_returns_404(self, client: APIClient) -> None:
        response = client.get("/users/0")
        assert_status_code(response, 404)

    def test_nonexistent_user_message_is_string(self, client: APIClient) -> None:
        response = client.get("/users/9999")
        msg = response.json().get("message", "")
        assert isinstance(msg, str) and len(msg) > 0


# ------------------------------------------------------------------ #
# 400 – Bad Request / Auth Errors                                      #
# ------------------------------------------------------------------ #

@pytest.mark.errors
class Test400BadRequest:
    """Verify 400 responses for malformed / incorrect credentials."""

    def test_login_wrong_password_returns_400(self, client: APIClient) -> None:
        response = client.post("/auth/login", json={"username": "emilys", "password": "wrongpass"})
        assert_status_code(response, 400)
        assert_response_contains_key(response, "message")

    def test_login_nonexistent_user_returns_400(self, client: APIClient) -> None:
        response = client.post("/auth/login", json={"username": "nobody", "password": "nobody"})
        assert_status_code(response, 400)
        assert_response_contains_key(response, "message")

    def test_login_empty_body_returns_400(self, client: APIClient) -> None:
        response = client.post("/auth/login", json={})
        assert_status_code(response, 400)

    def test_error_message_is_non_empty_string(self, client: APIClient) -> None:
        response = client.post("/auth/login", json={"username": "emilys", "password": "bad"})
        msg = response.json().get("message", "")
        assert isinstance(msg, str) and len(msg) > 0


# ------------------------------------------------------------------ #
# Negative value / type edge cases                                     #
# ------------------------------------------------------------------ #

@pytest.mark.errors
class TestEdgeCaseInputs:
    """Boundary and edge-case inputs on user endpoints."""

    def test_get_user_negative_id(self, client: APIClient) -> None:
        """A negative user ID should return 404."""
        response = client.get("/users/-1")
        assert_status_code(response, 404)

    def test_create_user_empty_name(self, client: APIClient) -> None:
        """Creating a user with empty name should not crash (200 or 201 accepted)."""
        response = client.post("/users/add", json={"firstName": "", "lastName": "Test"})
        assert response.status_code in (200, 201, 400), (
            f"Unexpected status {response.status_code}"
        )

    def test_create_user_very_long_name(self, client: APIClient) -> None:
        """Names longer than 255 chars should not cause a 5xx error."""
        long_name = "A" * 300
        response = client.post("/users/add", json={"firstName": long_name, "lastName": "Test"})
        assert response.status_code < 500

    def test_update_nonexistent_user(self, client: APIClient) -> None:
        """PUT on a non-existent ID — DummyJSON returns 404."""
        response = client.put("/users/9999", json={"firstName": "Ghost"})
        # DummyJSON returns 404 for non-existent users on PUT
        assert response.status_code in (200, 404)


# ------------------------------------------------------------------ #
# Authentication errors                                                #
# ------------------------------------------------------------------ #

@pytest.mark.errors
@pytest.mark.auth
class TestAuthErrors:
    """Verify error handling around authentication tokens."""

    def test_auth_me_without_token_returns_401(self, client: APIClient) -> None:
        """Protected endpoint /auth/me should reject unauthenticated requests."""
        response = client.get("/auth/me")
        assert response.status_code in (401, 403)

    def test_invalid_bearer_token_rejected(self, client: APIClient) -> None:
        """Invalid token should be rejected on protected endpoint."""
        bad_client = APIClient(token="this.is.not.a.valid.jwt")
        response = bad_client.get("/auth/me")
        assert response.status_code in (401, 403)

    def test_set_and_clear_token_on_client(self) -> None:
        """Verify set_token / clear_token helpers work correctly."""
        c = APIClient()
        assert c.token is None
        c.set_token("abc123")
        assert c.token == "abc123"
        c.clear_token()
        assert c.token is None


# ------------------------------------------------------------------ #
# General API quality checks                                           #
# ------------------------------------------------------------------ #

@pytest.mark.errors
class TestAPIQuality:
    """General API quality assertions."""

    def test_response_time_within_threshold(self, client: APIClient) -> None:
        """Response time for /users should be under 5 seconds."""
        import time
        start = time.perf_counter()
        client.get("/users")
        elapsed = time.perf_counter() - start
        assert elapsed < 5.0, f"Response took {elapsed:.2f}s – exceeds 5s threshold."

    def test_content_type_is_json(self, client: APIClient) -> None:
        """All API responses should declare application/json content-type."""
        response = client.get("/users")
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, (
            f"Unexpected Content-Type: {content_type}"
        )
