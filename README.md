# KiSM's Flask Boilerplate

## Clone

```bash
git clone https://github.com/kism/kism-flask-boilerplate
cd kism-flask-boilerplate

# CSS
cd mycoolapp
curl -LsS https://github.com/kism/zy.css/releases/download/main/grab.sh | bash
cd ..

rm -rf .git
```

## Prepare

I couldnt get the `rename` command to work...

This repo's app is called mycoolapp, these commands will rename all the files and instances of the name in files, this is tested, though I can't guarentee it if you pick a silly name.

In my example I replace mycoolapp with mydankapp.

```bash
NEWNAME=mydankapp
NEWNAMECAMELCASE=MyDankApp
SETTINGSVAR=mda_sett

# Files, replace in py in j2 files
find . -type f \( -name "*.py" -o -name "*.j2" \) | while read -r file; do
    sed -i "s/mycoolapp/${NEWNAME}/g" "$file" # References to project name in repo
    sed -i "s/MyCoolApp/${NEWNAMECAMELCASE}/g" "$file" # Rename Objects
    sed -i "s/mca_sett/${SETTINGSVAR}/g" "$file" # Rename Settings Variable
done

# Rename folders
mv mycoolapp/static/mycoolapp.js ./mycoolapp/static/${NEWNAME}.js
mv mycoolapp/mycoolapp_blueprint_one.py ./mycoolapp/${NEWNAME}_blueprint_one.py
mv mycoolapp/mycoolapp_settings.py ./mycoolapp/${NEWNAME}_settings.py
mv mycoolapp/mycoolapp_logger.py ./mycoolapp/${NEWNAME}_logger.py
mv mycoolapp $NEWNAME

cd ..
mv kism-flask-boilerplate ${NEWNAME}
cd ${NEWNAME}
```

## Poetry

```bash
poetry init --name="${NEWNAME}" --python=^3.11
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
