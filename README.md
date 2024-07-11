# KiSM's Flask Boilerplate

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/kism/flask-boilerplate/main.yml)
[![codecov](https://codecov.io/github/kism/flask-boilerplate/graph/badge.svg?token=NARIB5JF9M)](https://codecov.io/github/kism/flask-boilerplate)

## Get started

Install pipx <https://pipx.pypa.io/stable/>

Install poetry with pipx `pipx install poetry`

```bash
git clone https://github.com/kism/flask-boilerplate
cd flask-boilerplate
python create_my_new_project.py
```

This will create the new project directory in the parent directory, with the new name.

At the end of the script it will give you some instructions to use poetry, and grab the css.

## TODO

- do some wild regex in create_new_project
  - workflow
  - pyproject.toml
- handle when there are flask config items that arent in the default config
- indicate comments written by me
- more comments
- code review
- assert reasons
