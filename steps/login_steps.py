"""
Behave step definitions for features/login.feature
"""

from behave import given, when, then  # type: ignore
from utils.helpers import validate_schema, assert_status_code
from schemas.login_schema import LOGIN_SUCCESS_SCHEMA, REGISTER_SUCCESS_SCHEMA
from config.settings import settings


# ------------------------------------------------------------------ #
# Given                                                                #
# ------------------------------------------------------------------ #

@given("the API base URL is configured")
def step_api_base_url_configured(context):
    assert context.client is not None, "APIClient must be initialised in environment.py"


@given("I have valid login credentials")
def step_valid_login_credentials(context):
    context.payload = {
        "email": settings.LOGIN_EMAIL,
        "password": settings.LOGIN_PASSWORD,
    }


@given("I have login credentials without a password")
def step_credentials_no_password(context):
    context.payload = {"email": "peter@klaven"}


@given("I have login credentials without an email")
def step_credentials_no_email(context):
    context.payload = {"password": "secret"}


@given("I have an empty request payload")
def step_empty_payload(context):
    context.payload = {}


@given("I have valid registration credentials")
def step_valid_register_credentials(context):
    context.payload = {"email": "eve.holt@reqres.in", "password": "pistol"}


@given("I have registration credentials without a password")
def step_register_no_password(context):
    context.payload = {"email": "sydney@fife"}


# ------------------------------------------------------------------ #
# When                                                                 #
# ------------------------------------------------------------------ #

@when('I send a POST request to "{endpoint}"')
def step_send_post(context, endpoint):
    context.response = context.client.post(endpoint, json=context.payload)


# ------------------------------------------------------------------ #
# Then                                                                 #
# ------------------------------------------------------------------ #

@then("the response status code should be {status_code:d}")
def step_check_status_code(context, status_code):
    assert_status_code(context.response, status_code)


@then('the response body should contain a "{field}" field')
def step_response_contains_field(context, field):
    body = context.response.json()
    assert field in body, f"Field '{field}' not found in response: {body}"


@then('the response body should contain an "{field}" field')
def step_response_contains_field_an(context, field):
    body = context.response.json()
    assert field in body, f"Field '{field}' not found in response: {body}"


@then("the token should be a non-empty string")
def step_token_non_empty(context):
    token = context.response.json().get("token")
    assert isinstance(token, str) and len(token) > 0, f"Token invalid: {token!r}"


@then("the response should conform to the login success schema")
def step_login_success_schema(context):
    validate_schema(context.response.json(), LOGIN_SUCCESS_SCHEMA)


@then("the response should conform to the register success schema")
def step_register_success_schema(context):
    validate_schema(context.response.json(), REGISTER_SUCCESS_SCHEMA)
