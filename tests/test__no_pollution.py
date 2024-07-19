"""This are some tests to ensure that the app you have made won't accidentally my PyTest polluted.

My testing became hell when I realised that tests were interfering with each other since they were using real folders.
PyTest is multi threaded and thus multiple tests can (and will) be running at the same time.
Without tmp_path they will use each other's config/data.

Tests should always use tmp_path as an instance_path as it means they won't pollute each other.
And thus in the boilerplate I have some checks to ensure that your tests aren't possibly getting polluted.
"""

import pytest

from mycoolapp import create_app
from mycoolapp.config import ConfigValidationError


def test_instance_path_check(get_test_config: dict):
    """TEST: When passed a dictionary as a config, the instance path must be specified."""
    with pytest.raises(AttributeError):
        (
            create_app(get_test_config("testing_false_valid.toml")),
            "App needs to fail if no instance path provided when config dict is provided.",
        )


def test_config_validate_test_instance_path(get_test_config: dict):
    """My boilerplate catches when you forget to use tmp_path in testing.

    This test exists because I spent so much time troubleshooting why some tests are using the default instance path.
    """
    import contextlib
    import os
    import random
    import shutil
    import string

    # Please always use tmp_path and never do this outside of this test.
    repo_instance_path = os.path.join(os.getcwd(), "instance")
    incorrect_instance_root = os.path.join(repo_instance_path, "_TEST")
    random_string = "".join(random.choice(string.ascii_uppercase) for _ in range(8))
    incorrect_instance_path = os.path.join(incorrect_instance_root, random_string)

    with contextlib.suppress(FileNotFoundError, FileExistsError):
        os.mkdir(repo_instance_path)
        shutil.rmtree(incorrect_instance_root)
        os.mkdir(incorrect_instance_root)
        os.mkdir(incorrect_instance_path)

    # TEST: The program exits when in testing mode and the instance path is not a temp path.
    with pytest.raises(ConfigValidationError) as exc_info:
        create_app(test_config=get_test_config("testing_true_valid.toml"), instance_path=incorrect_instance_path)

    assert isinstance(exc_info.type, type(ConfigValidationError)), "App did not raise correct exception."
    assert "['flask']['TESTING'] is True but instance_path is not a tmp_path" in str(exc_info.getrepr())

    shutil.rmtree(incorrect_instance_root)
