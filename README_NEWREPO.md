# mycoolapp

## Run

### Run Dev

```bash
poetry install
poetry shell
flask --app mycoolapp run --port 5000
```

### Run Prod

```bash
poetry install --only main
.venv/bin/waitress-serve \
    --listen "127.0.0.1:5000" \
    --trusted-proxy '*' \
    --trusted-proxy-headers 'x-forwarded-for x-forwarded-proto x-forwarded-port' \
    --log-untrusted-proxy-headers \
    --clear-untrusted-proxy-headers \
    --threads 4 \
    --call mycoolapp:create_app
```

## Testing

Run `pytest`, It will get its config from pyproject.toml

Of course when you start writing your app many of the tests will break. With the comments it serves as a somewhat tutorial on using `pytest`, that being said I am not an expert.

To get the build:passing badge that's on the template repo have a look at <https://shields.io/badges>, the template repo uses <https://shields.io/badges/git-hub-actions-workflow-status>.

### Test Coverage

#### Locally

To get code coverage locally, the config is set in 'pyproject.toml', or run with `pytest --cov=mycoolapp --cov-report=term --cov-report=html`

```bash
python -m http.server -b 127.0.0.1 8000
```

Open the link in your browser and browse into the 'htmlcov' directory.

#### Codecov

The template rero uses codecov to get a badge on the README.md, look at their guides on confing that up since it's stripped out of this repo.

## Config

Defaults are defined in config.py, and config loading and validation are handled in there too.
