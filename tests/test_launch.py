"""Test launching the app."""

import os

import pytest
from flask.testing import FlaskClient

from mycoolapp import create_app

config_testing_true_valid = {"app": {}, "logging": {}, "flask": {"TESTING": True}}
config_testing_false_valid = {"app": {}, "logging": {}, "flask": {}}
config_invalid = {"flask": {"TESTING": True}}


def test_config() -> None:
    """Test config or something..."""
    # TEST: Assert that the settings dictionary can set config attributes successfully.
    assert not create_app(config_testing_false_valid).testing
    assert create_app(config_testing_true_valid).testing

    # TEST: We provided a settings dict, which means that it shouldn't write the settings to disk.
    filename = "instance/settings.toml"
    assert not os.path.exists(filename), f"File {filename} should not exist"

    # TEST: Assert that the program exists when provided an invalid config dictionary.
    with pytest.raises(SystemExit) as exc_info:
        create_app(config_invalid)

    assert isinstance(exc_info.type, type(SystemExit))
    assert exc_info.value.code == 1


def test_hello(client: FlaskClient) -> None:
    """Test the hello API endpoint."""
    response = client.get("/hello/")
    assert response.json["msg"] == "Hello, World!"
