"""Test launching the app."""

from flask.testing import FlaskClient

from mycoolapp import create_app

config_test_mode = {"flask": {"TESTING": True}}


def test_config() -> None:
    """Test config or something..."""
    assert not create_app().testing
    assert create_app(config_test_mode).testing


def test_hello(client: FlaskClient) -> None:
    """This is a test I wrote."""
    response = client.get("/hello/")
    assert response.json["msg"] == "Hello, World!"
