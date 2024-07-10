"""The conftest.py file serves as a means of providing fixtures for an entire directory.

Fixtures defined in a conftest.py can be used by any test in that package without needing to import them.
"""

import os

import flask
import pytest
import tomlkit
from jinja2 import Template

from mycoolapp import create_app

TEST_INSTANCE_PATH = os.path.join(os.getcwd(), "instance_test")
CONFIG_FILE_PATH = os.path.join(TEST_INSTANCE_PATH, "config.toml")
TEST_CONFIGS_LOCATION = os.path.join(os.getcwd(), f"tests{os.sep}configs")
TEST_LOG_PATH = os.path.join(TEST_INSTANCE_PATH, "test.log")


@pytest.fixture()
def app() -> any:
    """This fixture uses the default config within the flask app."""
    app = create_app(test_config=None, instance_path=TEST_INSTANCE_PATH)

    yield app  # This is the state that the test will get the object, anything below is cleanup.

    # Remove any created config/logs
    os.unlink(CONFIG_FILE_PATH)


@pytest.fixture()
def client(app: flask.Flask) -> any:
    """This returns a test client for the default app()."""
    return app.test_client()


@pytest.fixture()
def runner(app: flask.Flask) -> any:
    """TODO?????"""
    return app.test_cli_runner()


@pytest.fixture()
def get_test_config() -> dict:
    """Function returns a function, which is how it needs to be."""

    def _get_test_config(configname: str) -> dict:
        """Load all the .toml configs into a single dict."""
        filename_toml = f"{configname}.toml"
        filename_toml_j2 = f"{configname}.toml.j2"

        filepath_toml = os.path.join(TEST_CONFIGS_LOCATION, os.path.join(TEST_CONFIGS_LOCATION, filename_toml))
        filepath_toml_j2 = os.path.join(TEST_CONFIGS_LOCATION, os.path.join(TEST_CONFIGS_LOCATION, filename_toml_j2))

        assert not (
            os.path.isfile(filepath_toml) and os.path.isfile(filepath_toml_j2)
        ), f"Two configs with the same exist: {filename_toml}, {filename_toml_j2}. Rename or remove one."

        if os.path.isfile(filepath_toml):
            with open(filepath_toml) as file:
                out_config = tomlkit.load(file)

        elif os.path.isfile(filepath_toml_j2):
            with open(filepath_toml_j2) as file:
                template_string = file.read()
                template = Template(template_string)
                rendered_string = template.render(
                    TEST_INSTANCE_PATH=TEST_INSTANCE_PATH,
                    CONFIG_FILE_PATH=CONFIG_FILE_PATH,
                    TEST_CONFIGS_LOCATION=TEST_CONFIGS_LOCATION,
                    TEST_LOG_PATH=TEST_LOG_PATH,
                )
                out_config = tomlkit.loads(rendered_string)

        return out_config

    return _get_test_config


def pytest_configure():
    """This is a magic function for adding things to pytest?"""
    pytest.TEST_INSTANCE_PATH = TEST_INSTANCE_PATH
    pytest.CONFIG_FILE_PATH = CONFIG_FILE_PATH
    pytest.TEST_CONFIGS_LOCATION = TEST_CONFIGS_LOCATION
    pytest.TEST_LOG_PATH = TEST_LOG_PATH
