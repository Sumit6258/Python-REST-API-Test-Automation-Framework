"""
Global configuration settings for the API Test Automation Framework.
Values are loaded from environment variables with safe defaults.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Centralised settings loaded once at import time."""

    # ------------------------------------------------------------------ #
    # Base URLs                                                            #
    # ------------------------------------------------------------------ #
    BASE_URL: str = os.getenv("BASE_URL", "https://dummyjson.com")

    # ------------------------------------------------------------------ #
    # Authentication                                                       #
    # ------------------------------------------------------------------ #
    LOGIN_USERNAME: str = os.getenv("LOGIN_USERNAME", "emilys")
    LOGIN_PASSWORD: str = os.getenv("LOGIN_PASSWORD", "emilyspass")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "test_secret_key")
    LOGIN_EMAIL: str = os.getenv("LOGIN_EMAIL", "")  # not used by DummyJSON
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    # ------------------------------------------------------------------ #
    # HTTP Client                                                          #
    # ------------------------------------------------------------------ #
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "30"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))

    # ------------------------------------------------------------------ #
    # Pagination defaults                                                  #
    # ------------------------------------------------------------------ #
    DEFAULT_PAGE: int = 1
    DEFAULT_PER_PAGE: int = 6

    # ------------------------------------------------------------------ #
    # Logging                                                              #
    # ------------------------------------------------------------------ #
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_TO_FILE: bool = os.getenv("LOG_TO_FILE", "false").lower() == "true"
    LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", "reports/test_run.log")


settings = Settings()
