import pytest
from selenium import webdriver
from web import app as application
import geckodriver_autoinstaller

geckodriver_autoinstaller.install()


@pytest.fixture('session')
def app():
    return application


@pytest.yield_fixture('session')
def selenium():
    with webdriver.Firefox() as driver:
        yield driver
