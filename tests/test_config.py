"""Test launching the app."""

import logging
import os

import pytest

from mycoolapp import create_app

TEST_INSTANCE_PATH = f"{os.getcwd()}{os.sep}instance_test"
TEST_LOG_PATH = f"{TEST_INSTANCE_PATH}{os.sep}testlog.log"
CONFIG_FILE_PATH = f"{TEST_INSTANCE_PATH}{os.sep}settings.toml"
CONFIG_TESTING_TRUE_VALID = {"app": {}, "logging": {}, "flask": {"TESTING": True}}
CONFIG_TESTING_FALSE_VALID = {"app": {}, "logging": {}, "flask": {}}
CONFIG_LOGGING_PATH_VALID = {
    "app": {},
    "logging": {"path": TEST_LOG_PATH},
    "flask": {"TESTING": True},
}
CONFIG_LOGGING_PATH_INVALID_DIR = {
    "app": {},
    "logging": {"path": f"{TEST_INSTANCE_PATH}"},
    "flask": {"TESTING": True},
}
CONFIG_LOGGING_INVALID = {"app": {}, "logging": {}, "flask": {"TESTING": True}}
CONFIG_LOGGING_INVALID_LOG_LEVEL = {"app": {}, "logging": {"level": "INVALID"}, "flask": {"TESTING": True}}
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


def test_config_invalid_log_level(caplog: pytest.LogCaptureFixture):
    """Test if logging to file works."""
    caplog.set_level(logging.WARNING)
    create_app(CONFIG_LOGGING_INVALID_LOG_LEVEL)
    assert "Invalid logging level" in caplog.text


def test_config_logging_to_dir():
    """Test if logging to directory raises error."""
    with pytest.raises(IsADirectoryError) as exc_info:
        create_app(CONFIG_LOGGING_PATH_INVALID_DIR)

    assert isinstance(exc_info.type, type(IsADirectoryError))

def test_config_logging():
    """Test if len(root_logger.handlers) == 0: since it picks up the pytest logger.

    The code isn't covered otherwise.
    """
    logger = logging.getLogger()

    handlers = logger.handlers.copy()

    for handler in logger.handlers[:]:  # Iterate over a copy to avoid modification issues
        logger.removeHandler(handler)

    app = create_app(CONFIG_TESTING_TRUE_VALID)

    assert app

    # Restore PyTest's handlers
    for handler in handlers:
        logger.addHandler(handler)



def test_config_logging_to_file():
    """Test if logging to file works."""
    app = create_app(CONFIG_LOGGING_PATH_VALID)
    assert app
    os.unlink(TEST_LOG_PATH)


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
