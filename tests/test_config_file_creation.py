"""Test launching the app and config."""

import logging
import os

import pytest

from mycoolapp import create_app


def test_config_file_creation(tmp_path, caplog: pytest.LogCaptureFixture):
    """Tests relating to config file."""
    # TEST: that file is created when no config is provided.
    import contextlib
    with contextlib.suppress(FileNotFoundError):
        os.unlink(os.path.join(tmp_path, "config.toml"))

    with caplog.at_level(logging.WARNING):
        create_app(test_config=None, instance_path=tmp_path)

    assert "No configuration file found, creating at default location:" in caplog.text
    caplog.clear()
