"""Tests the blueprint's HTTP endpoint."""

from flask.testing import FlaskClient

from mycoolapp import create_app


def test_hello(client: FlaskClient):
    """TEST: The default /hello/ response, This one uses the fixture in conftest.py."""
    response = client.get("/hello/")
    assert response.json["msg"] == "Hello, World!", "Incorrect response from /hello/ when using default config."


def test_hello_with_config(tmp_path, get_test_config):
    """TEST: the hello API endpoint with non-default config."""
    app = create_app(get_test_config("bp_one_different_my_message.toml"), instance_path=tmp_path)
    client = app.test_client()
    response = client.get("/hello/")
    assert (
        response.json["msg"] == "Hello, PyTest!"
    ), "Wrong response from /hello/ when loading custom message from config."
