"""Test launching the app and config."""

import logging
import os

import pytest

from mycoolapp import create_app


def test_config_invalid(tmp_path, get_test_config):
    """Test that program exits when given invalid config."""
    # TEST: Assert that the program exists when provided an invalid config dictionary.
    with pytest.raises(SystemExit) as exc_info:
        create_app(test_config=get_test_config("invalid"), instance_path=tmp_path)

    assert isinstance(exc_info.type, type(SystemExit)), "App did not exit on config validation failure."
    assert exc_info.value.code == 1, "App did not have correct exit code for config validation failure."
    os.unlink(os.path.join(tmp_path, "config.toml"))
