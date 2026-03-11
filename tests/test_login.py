"""
Test suite: Login / Authentication API (DummyJSON)
Endpoint: POST /auth/login
Credentials: username/password (not email)
Token field: accessToken (not token)
"""

import pytest
from utils.api_client import APIClient
from utils.helpers import (
    assert_status_code,
    assert_response_contains_key,
    decode_jwt_unverified,
    validate_schema,
)
from schemas.login_schema import LOGIN_SUCCESS_SCHEMA, LOGIN_ERROR_SCHEMA
from config.settings import settings


# ------------------------------------------------------------------ #
# Fixtures                                                             #
# ------------------------------------------------------------------ #

@pytest.fixture(scope="module")
def client() -> APIClient:
    return APIClient()


# ------------------------------------------------------------------ #
# Happy-path tests                                                     #
# ------------------------------------------------------------------ #

@pytest.mark.smoke
@pytest.mark.auth
class TestLoginSuccess:
    """POST /auth/login – successful scenarios."""

    def test_login_returns_200(self, client: APIClient) -> None:
        response = client.post(
            "/auth/login",
            json={"username": settings.LOGIN_USERNAME, "password": settings.LOGIN_PASSWORD},
        )
        assert_status_code(response, 200)

    def test_login_response_contains_access_token(self, client: APIClient) -> None:
        response = client.post(
            "/auth/login",
            json={"username": settings.LOGIN_USERNAME, "password": settings.LOGIN_PASSWORD},
        )
        assert_response_contains_key(response, "accessToken")

    def test_login_token_is_non_empty_string(self, client: APIClient) -> None:
        response = client.post(
            "/auth/login",
            json={"username": settings.LOGIN_USERNAME, "password": settings.LOGIN_PASSWORD},
        )
        token = response.json().get("accessToken")
        assert isinstance(token, str) and len(token) > 0

    def test_login_response_schema(self, client: APIClient) -> None:
        response = client.post(
            "/auth/login",
            json={"username": settings.LOGIN_USERNAME, "password": settings.LOGIN_PASSWORD},
        )
        validate_schema(response.json(), LOGIN_SUCCESS_SCHEMA)

    def test_login_token_is_decodable_jwt(self, client: APIClient) -> None:
        """DummyJSON returns a real JWT — decode and check structure."""
        response = client.post(
            "/auth/login",
            json={"username": settings.LOGIN_USERNAME, "password": settings.LOGIN_PASSWORD},
        )
        token = response.json().get("accessToken")
        payload = decode_jwt_unverified(token)
        assert "id" in payload or "sub" in payload, "JWT payload missing identity claim."

    def test_authenticated_request_with_token(self, client: APIClient) -> None:
        """Token from /auth/login should be accepted on authenticated endpoints."""
        login_response = client.post(
            "/auth/login",
            json={"username": settings.LOGIN_USERNAME, "password": settings.LOGIN_PASSWORD},
        )
        token = login_response.json().get("accessToken")
        auth_client = APIClient(token=token)
        response = auth_client.get("/auth/me")
        assert_status_code(response, 200)

    def test_login_response_contains_user_info(self, client: APIClient) -> None:
        """DummyJSON login response also contains user details."""
        response = client.post(
            "/auth/login",
            json={"username": settings.LOGIN_USERNAME, "password": settings.LOGIN_PASSWORD},
        )
        body = response.json()
        assert "id" in body
        assert "username" in body
        assert "email" in body


# ------------------------------------------------------------------ #
# JWT generation / decoding (framework-level)                         #
# ------------------------------------------------------------------ #

@pytest.mark.auth
class TestJWTHelpers:
    """Validate the framework's own JWT generation and decoding helpers."""

    def test_generate_and_decode_jwt(self) -> None:
        from utils.helpers import generate_jwt_token, decode_jwt_token
        payload = {"user_id": 42, "role": "admin"}
        token = generate_jwt_token(payload)
        decoded = decode_jwt_token(token)
        assert decoded["user_id"] == 42
        assert decoded["role"] == "admin"
        assert "exp" in decoded
        assert "iat" in decoded

    def test_jwt_payload_claims(self) -> None:
        from utils.helpers import generate_jwt_token, decode_jwt_token
        import time
        before = int(time.time())
        token = generate_jwt_token({"sub": "test"}, expires_in=60)
        after = int(time.time())
        decoded = decode_jwt_token(token)
        assert before <= decoded["iat"] <= after
        assert decoded["exp"] == decoded["iat"] + 60

    def test_expired_jwt_raises(self) -> None:
        import jwt as pyjwt
        from utils.helpers import generate_jwt_token, decode_jwt_token
        token = generate_jwt_token({"sub": "test"}, expires_in=-1)
        with pytest.raises(pyjwt.ExpiredSignatureError):
            decode_jwt_token(token)


# ------------------------------------------------------------------ #
# Negative / error cases                                               #
# ------------------------------------------------------------------ #

@pytest.mark.auth
@pytest.mark.errors
class TestLoginErrors:
    """POST /auth/login – error / negative scenarios."""

    def test_login_wrong_password_returns_400(self, client: APIClient) -> None:
        response = client.post(
            "/auth/login",
            json={"username": settings.LOGIN_USERNAME, "password": "wrongpassword"},
        )
        assert_status_code(response, 400)

    def test_login_wrong_password_error_schema(self, client: APIClient) -> None:
        response = client.post(
            "/auth/login",
            json={"username": settings.LOGIN_USERNAME, "password": "wrongpassword"},
        )
        validate_schema(response.json(), LOGIN_ERROR_SCHEMA)

    def test_login_nonexistent_user_returns_400(self, client: APIClient) -> None:
        response = client.post(
            "/auth/login",
            json={"username": "nobody@nowhere.com", "password": "whatever"},
        )
        assert_status_code(response, 400)

    def test_login_empty_body_returns_400(self, client: APIClient) -> None:
        response = client.post("/auth/login", json={})
        assert_status_code(response, 400)

    def test_login_error_message_present(self, client: APIClient) -> None:
        response = client.post(
            "/auth/login",
            json={"username": settings.LOGIN_USERNAME, "password": "wrongpassword"},
        )
        body = response.json()
        assert "message" in body
        assert len(body["message"]) > 0
