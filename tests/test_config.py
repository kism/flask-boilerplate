"""Test launching the app and config."""

import logging

import pytest
import pytest_mock

from mycoolapp import create_app


def test_config_valid(get_test_config: dict):
    """Test passing config to app."""
    # TEST: Assert that the settings dictionary can set config attributes successfully.
    assert not create_app(get_test_config("testing_false_valid")).testing
    assert create_app(get_test_config("testing_true_valid")).testing


def test_config_invalid(get_test_config: dict):
    """Test that program exits when given invalid config."""
    # TEST: Assert that the program exists when provided an invalid config dictionary.
    with pytest.raises(SystemExit) as exc_info:
        create_app(get_test_config("invalid"))

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
        sett._write_settings({}, pytest.CONFIG_FILE_PATH)


def test_config_file_creation(get_test_config: dict, caplog: pytest.LogCaptureFixture) -> None:
    """Tests relating to settings file."""
    # TEST: that file is created when no config is provided.
    caplog.set_level(logging.WARNING)
    create_app(test_config=None, instance_path=pytest.TEST_INSTANCE_PATH)
    assert "No configuration file found, creating at default location:" in caplog.text
    caplog.clear()

    caplog.set_level(logging.WARNING)
    create_app(test_config=get_test_config("testing_true_valid"), instance_path=pytest.TEST_INSTANCE_PATH)
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
