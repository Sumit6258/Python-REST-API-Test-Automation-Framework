"""
Test suite: Pagination (DummyJSON)

DummyJSON uses skip/limit pagination (not page/per_page).
Response shape: {"users": [...], "total": N, "skip": N, "limit": N}
"""

import pytest
from utils.api_client import APIClient
from utils.helpers import (
    assert_status_code,
    assert_pagination_fields,
    validate_schema,
    get_all_pages,
)
from schemas.user_schema import USER_LIST_RESPONSE_SCHEMA


@pytest.fixture(scope="module")
def client() -> APIClient:
    return APIClient()


@pytest.mark.pagination
class TestPaginationStructure:
    """Validate the structure of paginated responses."""

    def test_first_page_has_correct_pagination_fields(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 0})
        assert_status_code(response, 200)
        assert_pagination_fields(response.json())

    def test_pagination_schema_first_page(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 0})
        validate_schema(response.json(), USER_LIST_RESPONSE_SCHEMA)

    def test_pagination_schema_second_page(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 10})
        validate_schema(response.json(), USER_LIST_RESPONSE_SCHEMA)

    @pytest.mark.parametrize("skip", [0, 10])
    def test_skip_reflected_in_response(self, client: APIClient, skip: int) -> None:
        response = client.get("/users", params={"limit": 10, "skip": skip})
        assert_status_code(response, 200)
        assert response.json()["skip"] == skip

    def test_total_is_positive(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 0})
        total = response.json().get("total", 0)
        assert total >= 1

    def test_total_is_consistent_across_pages(self, client: APIClient) -> None:
        r1 = client.get("/users", params={"limit": 10, "skip": 0}).json()
        r2 = client.get("/users", params={"limit": 10, "skip": 10}).json()
        assert r1["total"] == r2["total"], "The 'total' field must be identical on all pages."

    def test_limit_reflected_in_response(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 5, "skip": 0})
        assert response.json()["limit"] == 5


@pytest.mark.pagination
class TestPaginationData:
    """Validate the actual data returned by paginated responses."""

    def test_first_page_data_not_empty(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 0})
        assert len(response.json().get("users", [])) > 0

    def test_second_page_data_not_empty(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 10})
        assert len(response.json().get("users", [])) > 0

    def test_page_1_and_page_2_have_distinct_users(self, client: APIClient) -> None:
        ids_p1 = {u["id"] for u in client.get("/users", params={"limit": 10, "skip": 0}).json()["users"]}
        ids_p2 = {u["id"] for u in client.get("/users", params={"limit": 10, "skip": 10}).json()["users"]}
        overlap = ids_p1 & ids_p2
        assert not overlap, f"Duplicate user IDs found across pages: {overlap}"

    def test_per_page_count_matches_declared(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 0})
        body = response.json()
        assert len(body["users"]) <= body["limit"]

    def test_collect_all_users_matches_total(self, client: APIClient) -> None:
        all_users = get_all_pages(client, "/users", limit=10)
        first_page_total = client.get("/users", params={"limit": 10, "skip": 0}).json()["total"]
        assert len(all_users) == first_page_total

    def test_no_duplicate_ids_across_all_pages(self, client: APIClient) -> None:
        all_users = get_all_pages(client, "/users", limit=10)
        ids = [u["id"] for u in all_users]
        assert len(ids) == len(set(ids)), "Duplicate user IDs found across pages."


@pytest.mark.pagination
class TestPaginationBoundaries:
    """Edge cases for pagination parameters."""

    def test_very_large_skip_returns_empty_data(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 99999})
        assert_status_code(response, 200)
        data = response.json().get("users", [])
        assert data == [], f"Expected empty users on skip=99999, got: {data}"

    def test_default_limit_applied_without_param(self, client: APIClient) -> None:
        r_default = client.get("/users").json()
        assert "users" in r_default
        assert r_default["limit"] > 0
        assert len(r_default["users"]) > 0
