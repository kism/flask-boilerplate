"""Test versioning."""

import tomlkit

import {{cookiecutter.__app_slug}}


def test_version():
    """Test version variable."""
    with open("pyproject.toml", "rb") as f:
        pyproject_toml = tomlkit.load(f)
    assert pyproject_toml["tool"]["poetry"]["version"] == {{cookiecutter.__app_slug}}.__version__
