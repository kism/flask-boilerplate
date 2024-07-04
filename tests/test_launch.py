"""Test launching the app."""

from flask.testing import FlaskClient


from mycoolapp import create_app

def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client: FlaskClient) -> None:
    """This is a test I wrote."""
    response = client.get("/hello/")
    assert response.json["msg"] == "Hello, World!"
