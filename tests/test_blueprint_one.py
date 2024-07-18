"""PyTest, Tests the hello API endpoint."""

from flask.testing import FlaskClient


def test_hello(client: FlaskClient):
    """Test the hello API endpoint. This one uses the fixture in conftest.py."""
    response = client.get("/hello/")
    # TEST: The default /hello/ response
    assert response.json["msg"] == "Hello, World!", "Incorrect response from /hello/ when using default config."


def test_hello_with_config(tmp_path, get_test_config):
    """TEST: hello endpoint with different configs."""
    from mycoolapp import create_app

    app = create_app(get_test_config("different_my_message"), instance_path=tmp_path)
    client = app.test_client()
    response = client.get("/hello/")
    # TEST: the hello API endpoint with non-default config
    assert (
        response.json["msg"] == "Hello, PyTest!"
    ), "Wrong response from /hello/ when loading custom message from config."
