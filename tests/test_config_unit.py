"""Test launching the app and config."""

import logging

import pytest
import pytest_mock


def test_config_permissions_error(mocker: pytest_mock.plugin.MockerFixture):
    """Mock a Permissions error with mock_open."""
    import mycoolapp

    conf = mycoolapp.get_mycoolapp_config()

    mock_open_func = mocker.mock_open(read_data="")
    mock_open_func.side_effect = PermissionError("Permission denied")

    mocker.patch("builtins.open", mock_open_func)

    # TEST: PermissionsError is raised.
    with pytest.raises(PermissionError):
        conf._write_config({}, pytest.TEST_CONFIG_FILE_PATH)


def test_dictionary_functions_of_config():
    """Test the functions in the config object that let it behave like a dictionary."""
    import mycoolapp

    conf = mycoolapp.get_mycoolapp_config()

    # TEST: __contains__ method.
    assert "app" in conf, "__contains__ method of config object doesn't work"

    # TEST: __repr__ method.
    assert isinstance(str(conf), str), "__repr__ method of config object doesn't work"

    # TEST: __getitem__ method.
    assert isinstance(conf["app"], dict), "__getitem__ method of config object doesn't work"


def test_config_dictionary_merge(get_test_config: dict):
    """Unit test the dictionary merge in _merge_with_defaults."""
    import mycoolapp
    from mycoolapp import config

    conf = mycoolapp.get_mycoolapp_config()

    test_dictionaries = [
        {},
        get_test_config("logging_path_valid"),
        get_test_config("testing_true_valid"),
    ]

    for test_dictionary in test_dictionaries:
        result_dict = conf._merge_with_defaults(config.DEFAULT_CONFIG, test_dictionary)

        # TEST: Check that the resulting config after ensuring default is valid
        assert isinstance(result_dict["app"], dict)
        assert isinstance(result_dict["logging"], dict)
        assert isinstance(result_dict["logging"]["path"], str)
        assert isinstance(result_dict["logging"]["level"], str)
        assert isinstance(result_dict["flask"], dict)

    # TEST: If an item isn't in the schema, it still ends up around, not that this is a good idea...
    result_dict = conf._merge_with_defaults(config.DEFAULT_CONFIG, {"TEST_CONFIG_ENTRY_NOT_IN_SCHEMA": "lmao"})
    assert result_dict["TEST_CONFIG_ENTRY_NOT_IN_SCHEMA"]


def test_config_dictionary_not_in_schema(caplog: pytest.LogCaptureFixture):
    """Unit test _warn_unexpected_keys."""
    import mycoolapp
    from mycoolapp import config

    caplog.set_level(logging.WARNING)
    conf = mycoolapp.get_mycoolapp_config()
    test_config = {
        "TEST_CONFIG_ROOT_ENTRY_NOT_IN_SCHEMA": "",
        "app": {"my_message": "", "TEST_CONFIG_APP_ENTRY_NOT_IN_SCHEMA": ""},
    }

    # TEST: Warning when config loaded has a key that is not in the schema
    conf._warn_unexpected_keys(config.DEFAULT_CONFIG, test_config, "<root>")
    assert "Config entry key <root>[TEST_CONFIG_ROOT_ENTRY_NOT_IN_SCHEMA] not in schema" in caplog.text
    assert "Config entry key [app][TEST_CONFIG_APP_ENTRY_NOT_IN_SCHEMA] not in schema" in caplog.text
