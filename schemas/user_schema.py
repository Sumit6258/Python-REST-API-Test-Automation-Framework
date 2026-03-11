"""
JSON Schema definitions for User API responses (DummyJSON).

DummyJSON differences from reqres.in:
  - Single user is returned directly (no 'data' wrapper)
  - Fields are firstName/lastName/image (not first_name/last_name/avatar)
  - List response uses 'users' key and skip/limit pagination
  - Create uses POST /users/add, returns user object with id
"""

# ------------------------------------------------------------------ #
# Single user object (DummyJSON shape)                                #
# ------------------------------------------------------------------ #
USER_OBJECT_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "email", "firstName", "lastName"],
    "properties": {
        "id":        {"type": "integer", "minimum": 1},
        "email":     {"type": "string"},
        "firstName": {"type": "string", "minLength": 1},
        "lastName":  {"type": "string", "minLength": 1},
        "image":     {"type": "string"},
    },
}

# ------------------------------------------------------------------ #
# GET /users/:id  →  user object returned directly (no wrapper)       #
# ------------------------------------------------------------------ #
SINGLE_USER_RESPONSE_SCHEMA: dict = USER_OBJECT_SCHEMA

# ------------------------------------------------------------------ #
# GET /users?limit=N&skip=N  →  paginated list                        #
# ------------------------------------------------------------------ #
USER_LIST_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "required": ["users", "total", "skip", "limit"],
    "properties": {
        "users": {
            "type": "array",
            "items": USER_OBJECT_SCHEMA,
        },
        "total": {"type": "integer", "minimum": 0},
        "skip":  {"type": "integer", "minimum": 0},
        "limit": {"type": "integer", "minimum": 1},
    },
}

# ------------------------------------------------------------------ #
# POST /users/add  →  created user                                    #
# ------------------------------------------------------------------ #
CREATE_USER_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "required": ["id"],
    "properties": {
        "id":        {"type": "integer"},
        "firstName": {"type": "string"},
        "lastName":  {"type": "string"},
        "email":     {"type": "string"},
    },
}

# ------------------------------------------------------------------ #
# PUT /users/:id  →  updated user (DummyJSON echoes full user object) #
# ------------------------------------------------------------------ #
UPDATE_USER_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "required": ["id"],
    "properties": {
        "id":        {"type": "integer"},
        "firstName": {"type": "string"},
        "lastName":  {"type": "string"},
    },
}
