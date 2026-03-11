"""
Environment manager – resolves the active environment and returns
the correct base URL / credentials for that environment.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class EnvironmentConfig:
    name: str
    base_url: str
    login_email: str
    login_password: str


_ENVIRONMENTS: dict[str, EnvironmentConfig] = {
    "dev": EnvironmentConfig(
        name="dev",
        base_url="https://reqres.in/api",
        login_email="eve.holt@reqres.in",
        login_password="cityslicka",
    ),
    "staging": EnvironmentConfig(
        name="staging",
        base_url="https://reqres.in/api",
        login_email="eve.holt@reqres.in",
        login_password="cityslicka",
    ),
    "prod": EnvironmentConfig(
        name="prod",
        base_url="https://reqres.in/api",
        login_email="eve.holt@reqres.in",
        login_password="cityslicka",
    ),
}


def get_environment() -> EnvironmentConfig:
    """Return the EnvironmentConfig for the currently active environment.

    The active environment is resolved from the ENV environment variable
    (defaults to *dev*).
    """
    env_name = os.getenv("ENV", "dev").lower()
    if env_name not in _ENVIRONMENTS:
        raise ValueError(
            f"Unknown environment '{env_name}'. "
            f"Valid options: {list(_ENVIRONMENTS.keys())}"
        )
    return _ENVIRONMENTS[env_name]


# Convenience singleton consumed by the rest of the framework
current_env: EnvironmentConfig = get_environment()
