"""
Shared test-helper utilities.

Includes:
  - JWT generation / decoding helpers
  - Response assertion shortcuts
  - Schema validation wrapper
  - Pagination helpers
"""

from __future__ import annotations

import time
from typing import Any

import jwt
import jsonschema
from requests import Response

from config.settings import settings
from utils.logger import get_logger

log = get_logger(__name__)


# ------------------------------------------------------------------ #
# JWT helpers                                                          #
# ------------------------------------------------------------------ #

def generate_jwt_token(
    payload: dict[str, Any],
    secret: str | None = None,
    algorithm: str | None = None,
    expires_in: int = 3600,
) -> str:
    """Create a signed JWT token with an expiry claim."""
    secret = secret or settings.JWT_SECRET
    algorithm = algorithm or settings.JWT_ALGORITHM
    payload = {
        **payload,
        "iat": int(time.time()),
        "exp": int(time.time()) + expires_in,
    }
    token = jwt.encode(payload, secret, algorithm=algorithm)
    log.debug("Generated JWT token for payload: %s", payload)
    return token


def decode_jwt_token(
    token: str,
    secret: str | None = None,
    algorithm: str | None = None,
) -> dict[str, Any]:
    """Decode and verify a JWT token; returns the payload."""
    secret = secret or settings.JWT_SECRET
    algorithm = algorithm or settings.JWT_ALGORITHM
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        log.debug("Decoded JWT payload: %s", payload)
        return payload
    except jwt.ExpiredSignatureError:
        log.warning("JWT token has expired.")
        raise
    except jwt.InvalidTokenError as exc:
        log.error("Invalid JWT token: %s", exc)
        raise


def decode_jwt_unverified(token: str) -> dict[str, Any]:
    """Decode a JWT token without signature verification (for inspection only)."""
    payload = jwt.decode(token, options={"verify_signature": False})
    log.debug("Unverified JWT payload: %s", payload)
    return payload


# ------------------------------------------------------------------ #
# Schema validation                                                    #
# ------------------------------------------------------------------ #

def validate_schema(instance: Any, schema: dict[str, Any]) -> None:
    """Assert *instance* conforms to *schema*; raise AssertionError on failure."""
    try:
        jsonschema.validate(instance=instance, schema=schema)
        log.debug("Schema validation passed.")
    except jsonschema.ValidationError as exc:
        log.error("Schema validation FAILED: %s", exc.message)
        raise AssertionError(f"Schema validation failed: {exc.message}") from exc


# ------------------------------------------------------------------ #
# Response assertion helpers                                           #
# ------------------------------------------------------------------ #

def assert_status_code(response: Response, expected: int) -> None:
    actual = response.status_code
    assert actual == expected, (
        f"Expected HTTP {expected}, got {actual}.\n"
        f"URL: {response.url}\n"
        f"Body: {response.text[:500]}"
    )


def assert_response_contains_key(response: Response, key: str) -> None:
    body = response.json()
    assert key in body, (
        f"Key '{key}' not found in response body.\nBody: {body}"
    )


def assert_json_value(response: Response, key: str, expected: Any) -> None:
    body = response.json()
    actual = body.get(key)
    assert actual == expected, (
        f"Expected body['{key}'] == {expected!r}, got {actual!r}."
    )


# ------------------------------------------------------------------ #
# Pagination helpers                                                   #
# ------------------------------------------------------------------ #

def assert_pagination_fields(body: dict[str, Any]) -> None:
    """Assert that a DummyJSON paginated response contains the standard fields."""
    required = {"users", "total", "skip", "limit"}
    missing = required - body.keys()
    assert not missing, f"Pagination fields missing from response: {missing}"


def get_all_pages(client: Any, endpoint: str, limit: int = 10) -> list[dict]:
    """Collect every item from a DummyJSON paginated endpoint (skip/limit style)."""
    all_items: list[dict] = []
    skip = 0
    while True:
        response = client.get(endpoint, params={"limit": limit, "skip": skip})
        assert_status_code(response, 200)
        body = response.json()
        items = body.get("users", [])
        all_items.extend(items)
        skip += len(items)
        if skip >= body.get("total", 0) or not items:
            break
    log.info("Collected %d items from '%s'.", len(all_items), endpoint)
    return all_items
