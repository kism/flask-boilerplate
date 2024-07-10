"""PyTest, Tests the hello API endpoint."""

from http import HTTPStatus

from flask.testing import FlaskClient


def test_home(client: FlaskClient) -> None:
    """Test the hello API endpoint. This one uses the fixture in conftest.py."""
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK

def test_static_js_exists(client: FlaskClient) -> None:
    """Check that /static/mycoolapp.js exists."""
    response = client.get("/static/mycoolapp.js")
    assert response.status_code == HTTPStatus.OK
