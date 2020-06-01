from flask import url_for
from tests.selenium_functions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_register(selenium, live_server):
    selenium.get(url_for('signup_html', _external=True))
