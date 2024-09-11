"""Test the logger of the app."""

import logging
from types import FunctionType

import pytest
from flask import Flask

from {{cookiecutter.__app_package}} import create_app


def test_config_invalid_log_level(tmp_path, get_test_config: FunctionType, caplog: pytest.LogCaptureFixture):
    """Test if logging to file works."""
    caplog.set_level(logging.WARNING)
    app = create_app(get_test_config("logging_invalid_log_level.toml"), instance_path=tmp_path)
    # TEST: App still starts
    assert isinstance(app, Flask)
    # TEST: Assert that the invalid logging level message gets logged
    assert "Invalid logging level" in caplog.text
