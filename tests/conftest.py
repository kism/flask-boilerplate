"""The conftest.py file serves as a means of providing fixtures for an entire directory.

Fixtures defined in a conftest.py can be used by any test in that package without needing to import them.
"""

import os

import flask
import pytest

from mycoolapp import create_app

CONFIG_TESTING_TRUE_VALID = {"app": {"my_message": "Hello, World!"}, "logging": {}, "flask": {"TESTING": True}}
TEST_INSTANCE_PATH = f"{os.getcwd()}{os.sep}instance_test"
CONFIG_FILE_PATH = f"{TEST_INSTANCE_PATH}{os.sep}settings.toml"

@pytest.fixture()
def app() -> True:
    """TODO?????"""
    app = create_app(test_config=None, instance_path=TEST_INSTANCE_PATH)
    app.config.update(
        {
            "TESTING": True,
        },
    )

    # other setup can go here

    yield app  # This is the state that the test will get the object, anything below is cleanup.

    os.unlink(CONFIG_FILE_PATH) # Remove any created config



@pytest.fixture()
def client(app: flask.Flask) -> any:
    """TODO?????"""
    return app.test_client()


@pytest.fixture()
def runner(app: flask.Flask) -> any:
    """TODO?????"""
    return app.test_cli_runner()
