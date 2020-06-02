import pytest
from selenium import webdriver
from web import app as application


@pytest.fixture('session')
def app():
    return application


@pytest.fixture
def chrome():
    driver = webdriver.Chrome()
    yield driver
    driver.close()


@pytest.fixture
def firefox():
    driver = webdriver.Firefox()
    yield driver
    driver.close()

