"""
Reusable HTTP API client wrapper.

Provides a thin, opinionated layer on top of *requests* that handles:
  - Base-URL composition
  - Default / per-request headers
  - Bearer-token injection
  - Request / response logging
  - Automatic retries on transient failures
  - Convenient GET / POST / PUT / PATCH / DELETE helpers

Usage::

    from utils.api_client import APIClient

    client = APIClient()
    response = client.get("/users", params={"page": 1})
    response = client.post("/login", json={"email": "x", "password": "y"})
"""

from __future__ import annotations

import json
import time
from typing import Any

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import settings
from utils.logger import get_logger

log = get_logger(__name__)


class APIClient:
    """Thread-safe, reusable REST API client."""

    def __init__(
        self,
        base_url: str | None = None,
        token: str | None = None,
        default_headers: dict[str, str] | None = None,
        timeout: int | None = None,
        max_retries: int | None = None,
    ) -> None:
        self.base_url = (base_url or settings.BASE_URL).rstrip("/")
        self.token = token
        self.timeout = timeout or settings.DEFAULT_TIMEOUT
        self._default_headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if default_headers:
            self._default_headers.update(default_headers)

        self._session = requests.Session()
        retry_strategy = Retry(
            total=max_retries or settings.MAX_RETRIES,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    # ------------------------------------------------------------------ #
    # Public helpers                                                       #
    # ------------------------------------------------------------------ #

    def set_token(self, token: str) -> None:
        """Attach a Bearer token for all subsequent requests."""
        self.token = token
        log.debug("Bearer token updated on client.")

    def clear_token(self) -> None:
        """Remove the Bearer token (e.g. for negative auth tests)."""
        self.token = None

    # ------------------------------------------------------------------ #
    # HTTP verbs                                                           #
    # ------------------------------------------------------------------ #

    def get(self, endpoint: str, **kwargs: Any) -> Response:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> Response:
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> Response:
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs: Any) -> Response:
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> Response:
        return self._request("DELETE", endpoint, **kwargs)

    # ------------------------------------------------------------------ #
    # Internal                                                             #
    # ------------------------------------------------------------------ #

    def _build_headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = dict(self._default_headers)
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if extra:
            headers.update(extra)
        return headers

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._build_headers(kwargs.pop("headers", None))

        # Log request
        payload = kwargs.get("json") or kwargs.get("data")
        log.info("→ %s %s", method, url)
        if payload:
            log.debug("   Payload: %s", json.dumps(payload, indent=2))

        start = time.perf_counter()
        response: Response = self._session.request(
            method,
            url,
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )
        elapsed = (time.perf_counter() - start) * 1000

        # Log response
        log.info(
            "← %s %s  [%d]  %.1f ms",
            method,
            url,
            response.status_code,
            elapsed,
        )
        try:
            log.debug("   Body: %s", json.dumps(response.json(), indent=2))
        except Exception:
            log.debug("   Body (raw): %s", response.text[:500])

        return response
