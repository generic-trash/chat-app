import pytest
from selenium import webdriver
from web import app as application
import urllib3


@pytest.fixture
def app():
    return application


@pytest.fixture
def chrome():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def pool():
    pool = urllib3.PoolManager()
    yield pool


@pytest.fixture
def firefox():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()
