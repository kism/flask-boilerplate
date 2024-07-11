# KiSM's Flask Boilerplate

![Check](https://github.com/kism/flask-boilerplate/actions/workflows/check.yml/badge.svg)
![Test](https://github.com/kism/flask-boilerplate/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/github/kism/flask-boilerplate/graph/badge.svg?token=NARIB5JF9M)](https://codecov.io/github/kism/flask-boilerplate)

## Why this boilerplate?

I have made a few simple webapps that read a config, and have no database.

This was a learning experience to make something where I was 100% happy with the structure and will use it for my projects.

- Load config from TOML
- 100% test coverage with PyTest
- Only Three PyPi packages (and their dependencies) for prod

This goes with a simple CSS I made which is close to classless: <https://github.com/kism/zy.css>.

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

- code review
