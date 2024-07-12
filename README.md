# KiSM's Flask Boilerplate

![Check](https://github.com/kism/flask-boilerplate/actions/workflows/check.yml/badge.svg)
![Test](https://github.com/kism/flask-boilerplate/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/github/kism/flask-boilerplate/graph/badge.svg?token=NARIB5JF9M)](https://codecov.io/github/kism/flask-boilerplate)

## Why this boilerplate?

I have made a few simple web apps, this is what I use as a starting point for my future projects.

App features:

- App config loads from a TOML file
- Example api call and frontend javascript that utilises it
- Logging configuration, can log to file too
- 100% test coverage with PyTest

Project features:

- Only Three PyPi packages (and their dependencies) for prod
- Close to all project/tool configs in pyproject.toml
- Virtual environment and dependencies managed by Poetry.

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

- See if "my method" of doing config is okay
