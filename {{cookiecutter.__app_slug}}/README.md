# {{cookiecutter.__app_package}}

## Prerequisites

Install pipx <https://pipx.pypa.io/stable/>

Install poetry with pipx `pipx install poetry`

## Run

### Run Dev

```bash
poetry install
poetry shell
flask --app {{cookiecutter.__app_package}} run --port 5000
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
    --call {{cookiecutter.__app_package}}:create_app
```

## Check/Test

### Checking

Run `ruff check .` or get the vscode ruff extension, the rules are defined in pyproject.toml.

### Testing

Run `pytest`, It will get its config from pyproject.toml

Of course when you start writing your app many of the tests will break. With the comments it serves as a somewhat tutorial on using `pytest`, that being said I am not an expert.

### Workflows

The '.github' folder has both a Check and Test workflow.

To get the workflow passing badges on your repo, have a look at <https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge>

Or if you are not using GitHub you can check out workflow badges from your Git hosting service, or use <https://shields.io/> which pretty much covers everything.

### Test Coverage

#### Locally

To get code coverage locally, the config is set in 'pyproject.toml', or run with `pytest --cov={{cookiecutter.__app_package}} --cov-report=term --cov-report=html`

```bash
python -m http.server -b 127.0.0.1 8000
```

Open the link in your browser and browse into the 'htmlcov' directory.

#### Codecov

The template repo uses codecov to get a badge on the README.md, look at their guides on config that up since it's stripped out of this repo.

## Config

Defaults are defined in config.py, and config loading and validation are handled in there too.
