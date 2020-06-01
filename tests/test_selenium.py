from flask import url_for
from tests.selenium_functions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_register_firefox(firefox, live_server):
    firefox.get(url_for('signup_html', _external=True))


def test_register_chrome(chrome, live_server):
    chrome.get(url_for('signup_html', _external=True))
