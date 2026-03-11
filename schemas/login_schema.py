"""
JSON Schema definitions for Login / Auth API responses (DummyJSON).

DummyJSON differences:
  - Endpoint is /auth/login
  - Success returns 'accessToken' and 'refreshToken' (not 'token')
  - Errors return 'message' (not 'error')
  - No /register endpoint; use LOGIN_SUCCESS_SCHEMA for auth tests
"""

# ------------------------------------------------------------------ #
# POST /auth/login  →  successful login                               #
# ------------------------------------------------------------------ #
LOGIN_SUCCESS_SCHEMA: dict = {
    "type": "object",
    "required": ["accessToken", "refreshToken"],
    "properties": {
        "accessToken":  {"type": "string", "minLength": 1},
        "refreshToken": {"type": "string", "minLength": 1},
    },
}

# ------------------------------------------------------------------ #
# POST /auth/login  →  failed login                                   #
# ------------------------------------------------------------------ #
LOGIN_ERROR_SCHEMA: dict = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {"type": "string", "minLength": 1},
    },
}

# ------------------------------------------------------------------ #
# Kept for import compatibility (DummyJSON has no /register)          #
# ------------------------------------------------------------------ #
REGISTER_SUCCESS_SCHEMA: dict = LOGIN_SUCCESS_SCHEMA
REGISTER_ERROR_SCHEMA: dict = LOGIN_ERROR_SCHEMA
