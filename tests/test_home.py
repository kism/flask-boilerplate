"""PyTest, Tests the hello API endpoint."""

from http import HTTPStatus

from flask.testing import FlaskClient

CONFIG_VALID_DIFFERENT_MY_MESSAGE = {"app": {"my_message": "Hello, PyTest!"}, "logging": {}, "flask": {"TESTING": True}}


def test_home(client: FlaskClient) -> None:
    """Test the hello API endpoint. This one uses the fixture in conftest.py."""
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
