"""Test launching the app."""

import pytest
from flask.testing import FlaskClient

from mycoolapp import create_app

config_test_mode_valid = {"app": {}, "logging": {}, "flask": {"TESTING": True}}
config_invalid = {"flask": {"TESTING": True}}


def test_config() -> None:
    """Test config or something..."""
    # Assert that the settings dictionary can set config attributes successfully.
    assert not create_app().testing
    assert create_app(config_test_mode_valid).testing

    # Assert that the program exists when provided an invalid config dictionary.
    with pytest.raises(SystemExit) as exc_info:
        create_app(config_invalid)

    assert isinstance(exc_info.type, type(SystemExit))
    assert exc_info.value.code == 1


def test_hello(client: FlaskClient) -> None:
    """Test the hello API endpoint."""
    response = client.get("/hello/")
    assert response.json["msg"] == "Hello, World!"
