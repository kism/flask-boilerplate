"""Test the logger of the app."""

import logging
from types import FunctionType

import pytest
import pytest_mock


def test_logging_permissions_error(mocker: pytest_mock.plugin.MockerFixture):
    """Try mock a persmission error."""
    from mycoolapp.logger import _add_file_handler

    mock_open_func = mocker.mock_open(read_data="")
    mock_open_func.side_effect = PermissionError("Permission denied")

    mocker.patch("builtins.open", mock_open_func)

    logger = logging.getLogger("TEST_LOGGER")

    with pytest.raises(PermissionError):
        _add_file_handler(logger, pytest.TEST_LOG_PATH)


def test_config_logging_to_dir(get_test_config: FunctionType):
    """Test if logging to directory raises error.

    This one needs to go at the end since it interferes with other tests???
    """
    from mycoolapp.logger import _add_file_handler

    logger = logging.getLogger("TEST_LOGGER")

    # TEST: Check that correct exception is caught when you try log to a folder
    with pytest.raises(IsADirectoryError):
        _add_file_handler(logger, pytest.TEST_INSTANCE_PATH)


def test_set_log_level(get_test_config: FunctionType):
    """Test if logging to directory raises error.

    This one needs to go at the end since it interferes with other tests???
    """
    from mycoolapp.logger import _set_log_level

    logger = logging.getLogger("TEST_LOGGER")

    # TEST: Logger ends up with correct values
    _set_log_level(logger, 50)
    assert logger.getEffectiveLevel() == 50  # noqa: PLR2004 50 = 50

    _set_log_level(logger, "INFO")
    assert logger.getEffectiveLevel() == 20  # noqa: PLR2004 Warning = 30

    _set_log_level(logger, "WARNING")
    assert logger.getEffectiveLevel() == 30  # noqa: PLR2004 Warning = 30

    _set_log_level(logger, "INVALID")
    assert logger.getEffectiveLevel() == 20  # noqa: PLR2004 Invalid shoudl result in INFO (20)

    # Reset the object
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()
