"""
Behave environment hooks – runs before/after the suite, features, and scenarios.
"""

from utils.api_client import APIClient
from utils.logger import get_logger

log = get_logger("behave.environment")


def before_all(context):
    """Set up a shared API client available to all steps."""
    log.info("=== BDD Test Suite Starting ===")
    context.client = APIClient()
    context.response = None
    context.payload = {}


def after_all(context):
    log.info("=== BDD Test Suite Finished ===")


def before_feature(context, feature):
    log.info("Feature: %s", feature.name)


def before_scenario(context, scenario):
    log.info("  Scenario: %s", scenario.name)
    # Reset per-scenario state
    context.response = None
    context.payload = {}


def after_scenario(context, scenario):
    status = "PASSED" if scenario.status == "passed" else "FAILED"
    log.info("  [%s] %s", status, scenario.name)
