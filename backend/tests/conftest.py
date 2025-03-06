import pytest
from src.backend import app

@pytest.fixture(scope="module")
def client():
    app.config.update({
        "TESTING": True,
    })

    yield app.test_client()

    app.config.update({
        "TESTING": False,
    })
