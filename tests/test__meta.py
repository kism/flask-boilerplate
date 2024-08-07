"""Test versioning."""

import tomlkit

import mycoolapp


def test_version():
    """Test version variable."""
    with open("pyproject.toml", "rb") as f:
        pyproject_toml = tomlkit.load(f)
    assert pyproject_toml["tool"]["poetry"]["version"] == mycoolapp.__version__
