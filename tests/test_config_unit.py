"""Test launching the app and config."""

import pytest
import pytest_mock


def test_config_permissions_error(mocker: pytest_mock.plugin.MockerFixture):
    """Try mock a persmission error."""
    import mycoolapp

    sett = mycoolapp.get_mycoolapp_config()

    mock_open_func = mocker.mock_open(read_data="")
    mock_open_func.side_effect = PermissionError("Permission denied")

    mocker.patch("builtins.open", mock_open_func)

    with pytest.raises(PermissionError):
        sett._write_config({}, pytest.TEST_CONFIG_FILE_PATH)


def test_dictionary_functions_of_config():
    """Test the functions in the config object that let it behave like a dictionary."""
    import mycoolapp

    sett = mycoolapp.get_mycoolapp_config()

    # TEST: __contains__ method.
    assert "app" in sett

    # TEST: __repr__ method.
    assert isinstance(str(sett), str)

    # TEST: __getitem__ method.
    assert isinstance(sett["app"], dict)


def test_dictionary_merge(get_test_config: dict):
    """Unit test the dictionary merge in _ensure_all_default_config."""
    import mycoolapp
    from mycoolapp import config

    sett = mycoolapp.get_mycoolapp_config()

    test_dictionaries = [
        {},
        get_test_config("logging_path_valid"),
        get_test_config("testing_true_valid"),
    ]

    for test_dictionary in test_dictionaries:
        result_dict = sett._ensure_all_default_config(config.DEFAULT_CONFIG, test_dictionary)

        assert isinstance(result_dict["app"], dict)
        assert isinstance(result_dict["logging"], dict)
        assert isinstance(result_dict["logging"]["path"], str)
        assert isinstance(result_dict["logging"]["level"], str)
        assert isinstance(result_dict["flask"], dict)
