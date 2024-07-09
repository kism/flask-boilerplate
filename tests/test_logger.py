"""Test the logger of the app."""

import logging
import os

import pytest
import pytest_mock

from mycoolapp import create_app

TEST_INSTANCE_PATH = f"{os.getcwd()}{os.sep}instance_test"
TEST_LOG_PATH = f"{TEST_INSTANCE_PATH}{os.sep}testlog.log"
CONFIG_TESTING_TRUE_VALID = {"app": {}, "logging": {}, "flask": {"TESTING": True}}
CONFIG_LOGGING_INVALID = {"app": {}, "logging": {}, "flask": {"TESTING": True}}
CONFIG_LOGGING_INVALID_LOG_LEVEL = {"app": {}, "logging": {"level": "INVALID"}, "flask": {"TESTING": True}}
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


def test_config_logging_to_file():
    """Test if logging to file works."""
    app = create_app(CONFIG_LOGGING_PATH_VALID)
    assert app
    os.unlink(TEST_LOG_PATH)


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


def test_logging_permissions_error(mocker: pytest_mock.plugin.MockerFixture):
    """Try mock a persmission error."""
    from mycoolapp.logger import _add_file_handler

    mock_open_func = mocker.mock_open(read_data="")
    mock_open_func.side_effect = PermissionError("Permission denied")

    mocker.patch("builtins.open", mock_open_func)

    with pytest.raises(PermissionError):
      _add_file_handler(TEST_LOG_PATH)
