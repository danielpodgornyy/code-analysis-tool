import pytest
from src.app import app

@pytest.fixture(scope="module")
def flask_app():
    app.config.update({
        "TESTING": True,
    })

    yield app

    app.config.update({
        "TESTING": False,
    })

@pytest.fixture(scope="module")
def client(flask_app):
    return flask_app.test_client()
