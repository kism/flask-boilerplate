"""I don't know what this does really yet. I think this."""

import flask
import pytest

from mycoolapp import create_app


@pytest.fixture()
def app() -> True:
    """TODO?????"""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        },
    )

    # other setup can go here

    yield app  # Yield, no idea what this is

    # clean up / reset resources here
    return app


@pytest.fixture()
def client(app: flask.Flask) -> any:
    """TODO?????"""
    return app.test_client()


@pytest.fixture()
def runner(app: flask.Flask) -> any:
    """TODO?????"""
    return app.test_cli_runner()
