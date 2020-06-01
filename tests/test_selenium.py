from flask import url_for
from tests.selenium_functions import *
from selenium.webdriver.support.ui import WebDriverWait


def test_basic(selenium, live_server):
    selenium.get(url_for('testing', _external=True))
