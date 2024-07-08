"""Test launching the app."""

import os

import pytest
import shutil

from mycoolapp import create_app

config_testing_true_valid = {"app": {}, "logging": {}, "flask": {"TESTING": True}}
config_testing_false_valid = {"app": {}, "logging": {}, "flask": {}}
config_invalid = {"flask": {"TESTING": True}}
TEST_INSTANCE_PATH = f"{os.getcwd()}{os.sep}instance_test"
settings_path = f"{TEST_INSTANCE_PATH}{os.sep}settings.toml"


def test_config() -> None:
    """Test passing config to app."""
    # TEST: Assert that the settings dictionary can set config attributes successfully.
    assert not create_app(config_testing_false_valid).testing
    assert create_app(config_testing_true_valid).testing

    # TEST: We provided a settings dict, which means that it shouldn't write the settings to disk.
    assert not os.path.exists(settings_path), f"File {settings_path} should not exist"

    # TEST: Assert that the program exists when provided an invalid config dictionary.
    with pytest.raises(SystemExit) as exc_info:
        create_app(config_invalid)

    assert isinstance(exc_info.type, type(SystemExit))
    assert exc_info.value.code == 1


def test_settings_file_creation() -> None:
    """Test creating settings file if done doesnt exist."""
    create_app()
    assert os.path.exists(settings_path), f"File {settings_path} should not exist"
