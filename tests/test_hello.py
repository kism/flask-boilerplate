"""PyTest, Tests the hello API endpoint."""

from flask.testing import FlaskClient

from mycoolapp import create_app

CONFIG_VALID_DIFFERENT_MY_MESSAGE = {"app": {"my_message": "Hello, PyTest!"}, "logging": {}, "flask": {"TESTING": True}}

def test_hello(client: FlaskClient) -> None:
    """Test the hello API endpoint. This one uses the fixture in conftest.py."""
    response = client.get("/hello/")
    assert response.json["msg"] == "Hello, World!"

def test_hello_with_config() -> None:
    """Test the hello API endpoint with non-default config."""
    app = create_app(test_config=CONFIG_VALID_DIFFERENT_MY_MESSAGE)
    client = app.test_client()
    response = client.get("/hello/")
    assert response.json["msg"] == "Hello, PyTest!"
