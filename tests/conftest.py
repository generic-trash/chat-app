import pytest
from web import app as application


@pytest.fixture
def app():
    return application
