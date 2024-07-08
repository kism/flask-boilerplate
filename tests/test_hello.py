"""PyTest, Tests the hello API endpoint."""

from flask.testing import FlaskClient


def test_hello(client: FlaskClient) -> None:
    """Test the hello API endpoint."""
    response = client.get("/hello/")
    assert response.json["msg"] == "Hello, World!"
