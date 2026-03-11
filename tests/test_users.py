"""
Test suite: Users API (DummyJSON)

Key DummyJSON differences:
  - Single user returned directly (no 'data' wrapper)
  - Fields: firstName, lastName, image (not first_name, last_name, avatar)
  - Create: POST /users/add
  - Delete: returns JSON with isDeleted:true (not 204 empty)
  - Pagination: limit/skip (not page/per_page)
"""

import pytest
from utils.api_client import APIClient
from utils.helpers import (
    assert_status_code,
    #assert_response_contains_key,
    #assert_json_value,
    validate_schema,
)
from schemas.user_schema import (
    SINGLE_USER_RESPONSE_SCHEMA,
    USER_LIST_RESPONSE_SCHEMA,
    CREATE_USER_RESPONSE_SCHEMA,
    UPDATE_USER_RESPONSE_SCHEMA,
)


# ------------------------------------------------------------------ #
# Fixtures                                                             #
# ------------------------------------------------------------------ #

@pytest.fixture(scope="module")
def client() -> APIClient:
    return APIClient()


# ------------------------------------------------------------------ #
# GET /users – list                                                    #
# ------------------------------------------------------------------ #

@pytest.mark.smoke
@pytest.mark.users
class TestGetUsersList:
    """GET /users – list endpoint."""

    def test_get_users_returns_200(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 0})
        assert_status_code(response, 200)

    def test_get_users_response_schema(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 0})
        validate_schema(response.json(), USER_LIST_RESPONSE_SCHEMA)

    def test_get_users_returns_data(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 0})
        users = response.json().get("users", [])
        assert len(users) > 0, "Should return at least one user."

    def test_get_users_limit_respected(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 5, "skip": 0})
        users = response.json().get("users", [])
        assert len(users) == 5

    def test_get_users_data_is_list(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 0})
        assert isinstance(response.json().get("users"), list)

    def test_get_users_each_record_has_required_fields(self, client: APIClient) -> None:
        response = client.get("/users", params={"limit": 10, "skip": 0})
        for user in response.json().get("users", []):
            assert "id" in user
            assert "email" in user
            assert "firstName" in user
            assert "lastName" in user


# ------------------------------------------------------------------ #
# GET /users/:id – single user                                         #
# ------------------------------------------------------------------ #

@pytest.mark.smoke
@pytest.mark.users
class TestGetSingleUser:
    """GET /users/:id – single user endpoint."""

    def test_get_user_by_valid_id_returns_200(self, client: APIClient) -> None:
        response = client.get("/users/2")
        assert_status_code(response, 200)

    def test_get_user_schema_is_valid(self, client: APIClient) -> None:
        response = client.get("/users/2")
        validate_schema(response.json(), SINGLE_USER_RESPONSE_SCHEMA)

    def test_get_user_id_matches_request(self, client: APIClient) -> None:
        response = client.get("/users/2")
        # DummyJSON returns user directly (no 'data' wrapper)
        assert response.json()["id"] == 2

    def test_get_user_email_is_string(self, client: APIClient) -> None:
        response = client.get("/users/2")
        email = response.json()["email"]
        assert isinstance(email, str) and "@" in email

    def test_get_user_image_is_url(self, client: APIClient) -> None:
        response = client.get("/users/2")
        image = response.json().get("image", "")
        assert image.startswith("http")

    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5, 6])
    def test_users_are_retrievable_by_id(
        self, client: APIClient, user_id: int
    ) -> None:
        response = client.get(f"/users/{user_id}")
        assert_status_code(response, 200)
        assert response.json()["id"] == user_id


# ------------------------------------------------------------------ #
# POST /users/add – create                                             #
# ------------------------------------------------------------------ #

@pytest.mark.regression
@pytest.mark.users
class TestCreateUser:
    """POST /users/add – create endpoint."""

    def test_create_user_returns_201(self, client: APIClient) -> None:
        response = client.post(
            "/users/add",
            json={"firstName": "Jane", "lastName": "Doe", "age": 30},
        )
        assert_status_code(response, 201)

    def test_create_user_response_schema(self, client: APIClient) -> None:
        response = client.post(
            "/users/add",
            json={"firstName": "Jane", "lastName": "Doe", "age": 30},
        )
        validate_schema(response.json(), CREATE_USER_RESPONSE_SCHEMA)

    def test_create_user_first_name_matches(self, client: APIClient) -> None:
        response = client.post(
            "/users/add",
            json={"firstName": "John", "lastName": "Smith", "age": 25},
        )
        assert response.json().get("firstName") == "John"

    def test_create_user_last_name_matches(self, client: APIClient) -> None:
        response = client.post(
            "/users/add",
            json={"firstName": "John", "lastName": "Smith", "age": 25},
        )
        assert response.json().get("lastName") == "Smith"

    def test_create_user_has_id(self, client: APIClient) -> None:
        response = client.post(
            "/users/add",
            json={"firstName": "Test", "lastName": "User", "age": 22},
        )
        body = response.json()
        assert "id" in body and body["id"]


# ------------------------------------------------------------------ #
# PUT /users/:id – full update                                         #
# ------------------------------------------------------------------ #

@pytest.mark.regression
@pytest.mark.users
class TestUpdateUser:
    """PUT /users/:id – full-update endpoint."""

    def test_put_user_returns_200(self, client: APIClient) -> None:
        response = client.put(
            "/users/2",
            json={"firstName": "Updated", "lastName": "Name"},
        )
        assert_status_code(response, 200)

    def test_put_user_response_schema(self, client: APIClient) -> None:
        response = client.put(
            "/users/2",
            json={"firstName": "Updated", "lastName": "Name"},
        )
        validate_schema(response.json(), UPDATE_USER_RESPONSE_SCHEMA)

    def test_put_user_name_updated(self, client: APIClient) -> None:
        response = client.put(
            "/users/2",
            json={"firstName": "NewFirst"},
        )
        assert response.json().get("firstName") == "NewFirst"

    def test_patch_user_returns_200(self, client: APIClient) -> None:
        response = client.patch("/users/2", json={"lastName": "PatchedLast"})
        assert_status_code(response, 200)


# ------------------------------------------------------------------ #
# DELETE /users/:id                                                    #
# ------------------------------------------------------------------ #

@pytest.mark.regression
@pytest.mark.users
class TestDeleteUser:
    """DELETE /users/:id – delete endpoint."""

    def test_delete_user_returns_200(self, client: APIClient) -> None:
        # DummyJSON returns 200 with JSON (not 204 empty)
        response = client.delete("/users/2")
        assert_status_code(response, 200)

    def test_delete_user_is_deleted_flag(self, client: APIClient) -> None:
        response = client.delete("/users/2")
        body = response.json()
        assert body.get("isDeleted") is True, "Response should have isDeleted: true"
