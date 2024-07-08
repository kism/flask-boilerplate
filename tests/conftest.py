"""The conftest.py file serves as a means of providing fixtures for an entire directory.

Fixtures defined in a conftest.py can be used by any test in that package without needing to import them.
"""

import flask
import pytest

from mycoolapp import create_app

config_testing_true_valid = {"app": {"my_message": "Hello, World!"}, "logging": {}, "flask": {"TESTING": True}}

@pytest.fixture()
def app() -> True:
    """TODO?????"""
    app = create_app(config_testing_true_valid)
    app.config.update(
        {
            "TESTING": True,
        },
    )

    # other setup can go here

    yield app  # Yield, no idea what this is

    # clean up / reset resources here
    return app


@pytest.fixture()
def client(app: flask.Flask) -> any:
    """TODO?????"""
    return app.test_client()


@pytest.fixture()
def runner(app: flask.Flask) -> any:
    """TODO?????"""
    return app.test_cli_runner()
