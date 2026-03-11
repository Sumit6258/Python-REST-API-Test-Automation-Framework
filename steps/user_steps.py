"""
Behave step definitions for features/user.feature
"""

from behave import given, when, then  # type: ignore
from utils.helpers import validate_schema, assert_status_code
from schemas.user_schema import (
    SINGLE_USER_RESPONSE_SCHEMA,
    USER_LIST_RESPONSE_SCHEMA,
    CREATE_USER_RESPONSE_SCHEMA,
)


# ------------------------------------------------------------------ #
# Given                                                                #
# ------------------------------------------------------------------ #

@given("the API base URL is configured")
def step_api_configured(context):
    assert context.client is not None


@given('I have a valid user payload with name "{name}" and job "{job}"')
def step_valid_user_payload(context, name, job):
    context.payload = {"name": name, "job": job}


@given('I have an update payload with name "{name}" and job "{job}"')
def step_update_user_payload(context, name, job):
    context.payload = {"name": name, "job": job}


# ------------------------------------------------------------------ #
# When                                                                 #
# ------------------------------------------------------------------ #

@when('I send a GET request to "{endpoint}"')
def step_send_get(context, endpoint):
    context.response = context.client.get(endpoint)


@when('I send a GET request to "{endpoint}" with query params "{params}"')
def step_send_get_with_params(context, endpoint, params):
    param_dict = {}
    for pair in params.split("&"):
        key, _, value = pair.partition("=")
        # Convert to int if numeric
        param_dict[key] = int(value) if value.isdigit() else value
    context.response = context.client.get(endpoint, params=param_dict)


@when('I send a POST request to "{endpoint}"')
def step_send_post_users(context, endpoint):
    context.response = context.client.post(endpoint, json=context.payload)


@when('I send a PUT request to "{endpoint}"')
def step_send_put(context, endpoint):
    context.response = context.client.put(endpoint, json=context.payload)


@when('I send a DELETE request to "{endpoint}"')
def step_send_delete(context, endpoint):
    context.response = context.client.delete(endpoint)


# ------------------------------------------------------------------ #
# Then – status / body                                                 #
# ------------------------------------------------------------------ #

@then("the response status code should be {status_code:d}")
def step_status_code(context, status_code):
    assert_status_code(context.response, status_code)


@then('the response body should contain a "{field}" field')
def step_body_has_field(context, field):
    body = context.response.json()
    assert field in body, f"'{field}' not found in: {body}"


@then('the response body should contain an "{field}" field')
def step_body_has_field_an(context, field):
    body = context.response.json()
    assert field in body, f"'{field}' not found in: {body}"


@then('the response body should be an empty JSON object')
def step_body_empty_object(context):
    body = context.response.json()
    assert body == {}, f"Expected {{}}, got: {body}"


@then('the user "id" should be {user_id:d}')
def step_user_id_matches(context, user_id):
    actual = context.response.json()["data"]["id"]
    assert actual == user_id, f"Expected id={user_id}, got {actual}"


@then('the "{field}" field should be a non-empty list')
def step_field_non_empty_list(context, field):
    value = context.response.json().get(field)
    assert isinstance(value, list) and len(value) > 0, (
        f"Expected non-empty list for '{field}', got: {value}"
    )


@then('the "page" field in the response should equal {page:d}')
def step_page_field_equals(context, page):
    actual = context.response.json().get("page")
    assert actual == page, f"Expected page={page}, got {actual}"


@then('the response "{field}" should equal "{expected}"')
def step_response_field_equals_str(context, field, expected):
    actual = context.response.json().get(field)
    assert actual == expected, f"Expected {field}={expected!r}, got {actual!r}"


# ------------------------------------------------------------------ #
# Then – schema validation                                             #
# ------------------------------------------------------------------ #

@then("the response should conform to the single user schema")
def step_single_user_schema(context):
    validate_schema(context.response.json(), SINGLE_USER_RESPONSE_SCHEMA)


@then("the response should conform to the user list schema")
def step_user_list_schema(context):
    validate_schema(context.response.json(), USER_LIST_RESPONSE_SCHEMA)


@then("the response should conform to the create user schema")
def step_create_user_schema(context):
    validate_schema(context.response.json(), CREATE_USER_RESPONSE_SCHEMA)
