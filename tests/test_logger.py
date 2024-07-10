"""Test the logger of the app."""

import logging
import os

import pytest
import pytest_mock

from mycoolapp import create_app


def test_config_invalid_log_level(get_test_config: dict, caplog: pytest.LogCaptureFixture):
    """Test if logging to file works."""
    caplog.set_level(logging.WARNING)
    create_app(get_test_config("logging_invalid_log_level"))
    assert "Invalid logging level" in caplog.text


def test_config_logging_to_dir(get_test_config: dict):
    """Test if logging to directory raises error."""
    with pytest.raises(IsADirectoryError) as exc_info:
        create_app(get_test_config("logging_path_invalid"))

    assert isinstance(exc_info.type, type(IsADirectoryError))


def test_config_logging_to_file(get_test_config: dict):
    """Test if logging to file works."""
    app = create_app(get_test_config("logging_path_valid"))
    assert app
    os.unlink(pytest.TEST_LOG_PATH)


def test_config_logging(get_test_config: dict):
    """Test if len(root_logger.handlers) == 0: since it picks up the pytest logger.

    The code isn't covered otherwise.
    """
    logger = logging.getLogger()

    handlers = logger.handlers.copy()

    for handler in logger.handlers[:]:  # Iterate over a copy to avoid modification issues
        logger.removeHandler(handler)

    app = create_app(get_test_config("testing_true_valid"))

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
        _add_file_handler(pytest.TEST_LOG_PATH)
