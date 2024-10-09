
# django-lit-urls

Django URLS delivered as string literal functions in Javascript

## Install

If you don't have `poetry` yet perhaps do a `pipx install poetry`

From source: `poetry install` from this directory
From pypi: `pip install django-lit-urls`

## Tests and Linting

The following tests should not raise anything:

```bash
poetry run black --check .
poetry run flake8 .
poetry run isort .
poetry run python -m mypy django_lit_urls/
```

## Publish


If you have not done so yet make an api token.
Fetch an api token from pypi at https://pypi.org/manage/account/token/
It'll be something like pypi-AgEIcHlwaS5vcmc****
`poetry config pypi-token.pypi your-api-token`

Build and publish:

`poetry build && poetry publish`
