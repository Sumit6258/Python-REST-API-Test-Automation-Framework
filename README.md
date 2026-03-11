# 🧪 REST API Test Automation Framework

A **production-grade**, modular Python framework for automated REST API testing.
Built with `pytest`, `behave`, `requests`, `jsonschema`, and `PyJWT`, and designed
to slot into any modern CI/CD pipeline from day one.

---

## 📑 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Technologies Used](#technologies-used)
4. [Setup Instructions](#setup-instructions)
5. [Running pytest Tests](#running-pytest-tests)
6. [Running Behave BDD Tests](#running-behave-bdd-tests)
7. [Test Reports](#test-reports)
8. [CI/CD Pipeline](#cicd-pipeline)
9. [Environment Configuration](#environment-configuration)
10. [Adding New Tests](#adding-new-tests)
11. [Framework Design Decisions](#framework-design-decisions)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    Test Layer                        │
│  pytest tests/          behave features/steps/      │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                  Helper Layer                        │
│  utils/helpers.py  (assertions, JWT, schema checks) │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                  Client Layer                        │
│  utils/api_client.py  (HTTP, retries, logging)      │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                  Config Layer                        │
│  config/settings.py   config/environment.py         │
└─────────────────────────────────────────────────────┘
```

The framework is split into four clean layers:

| Layer | Responsibility |
|-------|----------------|
| **Config** | Loads env vars, resolves active environment, exposes typed settings |
| **Client** | Wraps `requests` – handles base URL, auth headers, retries, logging |
| **Helpers** | Shared assertions, JWT helpers, schema validation, pagination utilities |
| **Tests** | pytest modules and behave features/steps that consume the layers above |

---

## Project Structure

```
api-test-automation-framework/
│
├── config/
│   ├── __init__.py
│   ├── environment.py       # Dev / staging / prod environment resolver
│   └── settings.py          # Typed settings loaded from env vars
│
├── utils/
│   ├── __init__.py
│   ├── api_client.py        # Reusable HTTP client wrapper
│   ├── helpers.py           # JWT, schema, assertion utilities
│   └── logger.py            # Coloured, configurable logging
│
├── schemas/
│   ├── __init__.py
│   ├── login_schema.py      # JSON Schema for auth responses
│   └── user_schema.py       # JSON Schema for user responses
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared pytest fixtures
│   ├── test_login.py        # Auth / JWT tests
│   ├── test_users.py        # CRUD user tests
│   ├── test_pagination.py   # Pagination behaviour tests
│   └── test_error_cases.py  # Negative / error tests
│
├── features/
│   ├── environment.py       # Behave hooks (before/after)
│   ├── login.feature        # BDD scenarios for login
│   └── user.feature         # BDD scenarios for users
│
├── steps/
│   ├── login_steps.py       # Step definitions for login.feature
│   └── user_steps.py        # Step definitions for user.feature
│
├── reports/                 # Generated HTML + JSON reports
│
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions pipeline
│
├── .env.example             # Environment variable template
├── behave.ini               # Behave configuration
├── pytest.ini               # pytest configuration
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Runtime |
| pytest | 7.4 | Test runner |
| pytest-html | 4.1 | HTML test reports |
| behave | 1.2.6 | BDD test runner |
| requests | 2.31 | HTTP client |
| jsonschema | 4.20 | Response schema validation |
| PyJWT | 2.8 | JWT generation & decoding |
| colorlog | 6.7 | Coloured console logging |
| python-dotenv | 1.0 | `.env` file loading |

---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip

### 1 — Clone the repository

```bash
git clone https://github.com/your-org/api-test-automation-framework.git
cd api-test-automation-framework
```

### 2 — Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Configure environment variables

```bash
cp .env.example .env
# Edit .env with your own values if needed
```

---

## Running pytest Tests

### Run the full test suite

```bash
pytest
```

### Run only smoke tests

```bash
pytest -m smoke
```

### Run only authentication tests

```bash
pytest -m auth
```

### Run with a specific marker combination

```bash
pytest -m "smoke and not errors"
```

### Run a single test file

```bash
pytest tests/test_users.py -v
```

### Run a single test by name

```bash
pytest tests/test_users.py::TestGetSingleUser::test_get_user_by_valid_id_returns_200
```

### Run tests in parallel (requires pytest-xdist)

```bash
pytest -n 4
```

### Available markers

| Marker | Description |
|--------|-------------|
| `smoke` | Quick sanity checks – run on every commit |
| `regression` | Full regression – run nightly |
| `auth` | Authentication and JWT token tests |
| `users` | User management endpoint tests |
| `pagination` | Pagination behaviour tests |
| `errors` | Error handling and negative tests |

---

## Running Behave BDD Tests

### Run all feature files

```bash
behave
```

### Run a specific feature file

```bash
behave features/login.feature
behave features/user.feature
```

### Run scenarios by tag

```bash
behave --tags=@smoke
behave --tags=@auth
behave --tags=@smoke,@regression
behave --tags=~@errors          # exclude errors tag
```

### Run with verbose output

```bash
behave --verbose --no-capture
```

---

## Test Reports

### pytest HTML Report

After running `pytest`, open the generated report:

```
reports/pytest_report.html
```

The report includes:

- ✅ Passed / ❌ Failed / ⚠️ Skipped counts
- Per-test execution time
- Full failure tracebacks
- Environment metadata

### Behave Reports

```
reports/behave_report.txt    # Human-readable pretty output
reports/behave_report.json   # Machine-readable for dashboards
```

---

## CI/CD Pipeline

The GitHub Actions workflow in `.github/workflows/ci.yml` runs automatically on:

- **Push** to `main`, `develop`, or any `feature/**` branch
- **Pull Request** targeting `main` or `develop`
- **Nightly schedule** (02:00 UTC) for the regression suite
- **Manual trigger** (`workflow_dispatch`) with selectable suite and environment

### Pipeline Jobs

```
lint  ──► pytest (ubuntu + windows)
      └── behave (ubuntu)
           │
           └── notify (on failure)
```

### Viewing Reports in GitHub Actions

1. Navigate to **Actions** → select a workflow run
2. Scroll to **Artifacts** at the bottom
3. Download `pytest-report-ubuntu-latest` or `behave-report`

### Secrets Required

No secrets are required for the default `reqres.in` target.
For private APIs, add the following repository secrets:

| Secret | Description |
|--------|-------------|
| `BASE_URL` | Target API base URL |
| `LOGIN_EMAIL` | Login email for auth tests |
| `LOGIN_PASSWORD` | Login password for auth tests |
| `JWT_SECRET` | Secret for JWT verification |

---

## Environment Configuration

The framework supports three named environments: `dev`, `staging`, `prod`.

Set the target environment via the `ENV` variable:

```bash
ENV=staging pytest
ENV=prod behave
```

All per-environment settings are defined in `config/environment.py`.

---

## Adding New Tests

### Add a new pytest test module

1. Create `tests/test_<resource>.py`
2. Import `APIClient` and helpers
3. Decorate with relevant `pytest.mark.*` markers

```python
import pytest
from utils.api_client import APIClient
from utils.helpers import assert_status_code

@pytest.fixture(scope="module")
def client():
    return APIClient()

@pytest.mark.smoke
def test_my_new_endpoint(client):
    response = client.get("/my-endpoint")
    assert_status_code(response, 200)
```

### Add a new JSON schema

1. Create `schemas/my_resource_schema.py`
2. Define your schema dict
3. Import and use `validate_schema(response.json(), MY_SCHEMA)`

### Add a new BDD feature

1. Create `features/my_resource.feature` with Gherkin scenarios
2. Implement step definitions in `steps/my_resource_steps.py`
3. Reuse existing steps from `login_steps.py` / `user_steps.py` where possible

---

## Framework Design Decisions

| Decision | Rationale |
|----------|-----------|
| `APIClient` wraps `requests.Session` | Enables connection pooling, retry logic, and shared headers across tests |
| Session-scoped `authenticated_client` fixture | Login is performed once per test session rather than on every test |
| JSON Schemas as plain dicts | No extra libraries needed; schemas live next to the tests that use them |
| `colorlog` for console output | Makes INFO/WARNING/ERROR instantly distinguishable in CI logs |
| `python-dotenv` | Keeps secrets out of source code; easy `.env` overrides for local dev |
| Behave steps reuse helper functions | Avoids logic duplication between pytest and BDD layers |

---

## License

MIT — use freely, attribution appreciated.
