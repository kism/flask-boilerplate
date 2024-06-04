# KiSM's Flask Boilerplate

## Poetry

```bash
poetry init --name=mycoolapp --python=^3.11
poetry add flask
poetry add waitress # Run in prod
poetry add pyyaml # I like to load config from yaml
poetry add requests # Best way to do webrequests in python
poetry add ruff --group dev # Best linter
poetry add pylance --group dev # Language server, integrates with vscode
poetry install
```

## Run Dev

```bash
poetry shell
flask --app mycoolapp run --port 5000

# Run Prod
```bash
.venv/bin/waitress-serve waitress-serve \
    --listen "127.0.0.1:5000" \
    --trusted-proxy '*' \
    --trusted-proxy-headers 'x-forwarded-for x-forwarded-proto x-forwarded-port' \
    --log-untrusted-proxy-headers \
    --clear-untrusted-proxy-headers \
    --threads 4 \
    --call mycoolapp:mycoolapp

```
