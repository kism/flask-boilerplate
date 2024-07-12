# KiSM's Flask Boilerplate

![Check](https://github.com/kism/flask-boilerplate/actions/workflows/check.yml/badge.svg)
![Test](https://github.com/kism/flask-boilerplate/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/github/kism/flask-boilerplate/graph/badge.svg?token=NARIB5JF9M)](https://codecov.io/github/kism/flask-boilerplate)

## Why this boilerplate?

I have made a few simple web apps, this is what I use as a starting point for my future projects.

App features:

- App config loads from a TOML file
- Logging configuration, can log to file too
- Example api call and frontend javascript that utilises it
- 100% test coverage with PyTest

Project features:

- Only Three PyPi packages (and their dependencies) for prod
- Close to all project/tool configs in pyproject.toml
- Virtual environment and dependencies managed by Poetry.

This goes with a simple CSS I made which is close to classless: <https://github.com/kism/zy.css>. Have a look at <https://github.com/dbohdan/classless-css> too if you want a different css.

## Get started

```bash
git clone https://github.com/kism/flask-boilerplate
cd flask-boilerplate
python create_my_new_project.py
```

`create_my_new_project.py` Doesn't require any pip packages and can be run with your operating systems default python.

This will create the new project directory in the parent directory, with the new name.

At the end of the script it will give you some instructions to use poetry, and grab the my css.

## TODO

- See if "my method" of doing config is okay
