"""PyTest, Tests the hello API endpoint."""

from http import HTTPStatus

from flask.testing import FlaskClient


def test_home(client: FlaskClient):
    """Test the hello API endpoint. This one uses the fixture in conftest.py."""
    response = client.get("/")
    # TEST: HTTP OK
    assert response.status_code == HTTPStatus.OK
    # TEST: Content type
    assert response.content_type == "text/html; charset=utf-8"
    # TEST: It is a webpage that we get back
    assert b"<!doctype html>" in response.data


def test_static_js_exists(client: FlaskClient):
    """Check that /static/mycoolapp.js exists."""
    response = client.get("/static/mycoolapp.js")
    # TEST: That the javascript loads
    assert response.status_code == HTTPStatus.OK
