# URL Shortener API

A minimal DRF API for shortening URLs — create a short code from a long URL, and expand a short code back to the original URL. No auth, no analytics, no branded domains, no extra features.

## Tech stack

- Python 3.14+
- Django 6 + Django REST Framework
- SQLite
- [uv](https://docs.astral.sh/uv/) for dependency management
- mypy (strict) + django-stubs / djangorestframework-stubs for type checking
- ruff for linting and formatting
- pytest / pytest-django for testing
- pre-commit for local checks

## Setup

```bash
uv sync
uv run python manage.py migrate
```

## Running

```bash
uv run python manage.py runserver
```

The API is served at `http://127.0.0.1:8000/`.

## Endpoints

### `POST /shrt/` - create a short URL

Request:

```json
{
  "original_url": "https://example.com/test-url"
}
```

Response — `201 Created` for a new URL, `200 OK` if that URL was already shortened before (idempotent, same `code` returned both times):

```json
{
  "code": "3LNP18Z"
}
```

`400 Bad Request` for a missing or invalid `original_url`.

### `GET /shrt/<code>/` - expand a short URL

Response — `200 OK`:

```json
{
  "original_url": "https://example.com/test-url"
}
```

`404 Not Found` for an unknown code.

## Testing

```bash
# tests/unit and tests/e2e
uv run pytest

# strict type checking
uv run mypy .

# lint
uv run ruff check .

# formatting
uv run ruff format --check .
```

## Pre-commit hooks
- `pre-commit install` to install the hooks
- `pre-commit run --all-files` to run all checks

Please note that `pre-commit` is not installed by default. Once installed it will run automatically on every commit.

## Design decisions & assumptions
- No `django.contrib.auth`: To keep app simple, no users are involved, which is reflected in the settings.
- Extend on GET endpoint with params: Just to demonstrate how to use them in DRF. 
- Duplicate long URLs are idempotent: To ensure expanding a short code always returns the same long URL.
- Short-code generation: `generate_code()` builds a code by choosing `settings.DEFAULT_CODE_LENGTH`
- URL validation: `original_url` is validated by DRF's `URLField`.
