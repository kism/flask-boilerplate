"""Test launching the app and config."""

import logging
import os

import pytest
import pytest_mock

from mycoolapp import create_app

TEST_INSTANCE_PATH = f"{os.getcwd()}{os.sep}instance_test"
CONFIG_FILE_PATH = f"{TEST_INSTANCE_PATH}{os.sep}settings.toml"
CONFIG_TESTING_TRUE_VALID = {"app": {}, "logging": {}, "flask": {"TESTING": True}}
CONFIG_TESTING_FALSE_VALID = {"app": {}, "logging": {}, "flask": {}}
CONFIG_INVALID = {"app": {"configuration_failure": True}, "logging": {}, "flask": {"TESTING": True}}


def test_config_valid():
    """Test passing config to app."""
    # TEST: Assert that the settings dictionary can set config attributes successfully.
    assert not create_app(test_config=CONFIG_TESTING_FALSE_VALID).testing
    assert create_app(test_config=CONFIG_TESTING_TRUE_VALID).testing


def test_config_invalid():
    """Test that program exits when given invalid config."""
    # TEST: Assert that the program exists when provided an invalid config dictionary.
    with pytest.raises(SystemExit) as exc_info:
        create_app(CONFIG_INVALID)

    assert isinstance(exc_info.type, type(SystemExit))
    assert exc_info.value.code == 1


def test_config_permissions_error(mocker: pytest_mock.plugin.MockerFixture):
    """Try mock a persmission error."""
    import mycoolapp

    sett = mycoolapp.get_mycoolapp_settings()

    mock_open_func = mocker.mock_open(read_data="")
    mock_open_func.side_effect = PermissionError("Permission denied")

    mocker.patch("builtins.open", mock_open_func)

    with pytest.raises(PermissionError):
        sett._write_settings({}, CONFIG_FILE_PATH)


def test_config_file_creation(caplog: pytest.LogCaptureFixture) -> None:
    """Tests relating to settings file."""
    # TEST: that file is created when no config is provided.
    caplog.set_level(logging.WARNING)
    create_app(test_config=None, instance_path=TEST_INSTANCE_PATH)
    assert "No configuration file found, creating at default location:" in caplog.text
    caplog.clear()

    caplog.set_level(logging.WARNING)
    create_app(test_config=CONFIG_TESTING_TRUE_VALID, instance_path=TEST_INSTANCE_PATH)
    assert "No configuration file found, creating at default location:" not in caplog.text


def test_dictionary_functions_of_config():
    """Test the functions in the settings object that let it behave like a dictionary."""
    import mycoolapp

    sett = mycoolapp.get_mycoolapp_settings()

    # TEST: __contains__ method.
    assert "app" in sett

    # TEST: __repr__ method.
    assert isinstance(str(sett), str)

    # TEST: __getitem__ method.
    assert isinstance(sett["app"], dict)
