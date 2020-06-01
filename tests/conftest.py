import pytest
from selenium import webdriver
from web import app as application


@pytest.fixture('session')
def app():
    return application
