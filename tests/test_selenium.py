from flask import url_for
import pytest
from time import sleep
from tests.selenium_functions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_register_firefox_4errs(live_server, firefox: webdriver.Firefox):
    sleep(1)
    firefox.get(url_for('signup_html', _external=True))
    em_err = firefox.find_element(By.CSS_SELECTOR, '#emh6')
    us_err = firefox.find_element(By.CSS_SELECTOR, '#ush6')
    pw_err = firefox.find_element(By.CSS_SELECTOR, '#pwh6')
    cp_err = firefox.find_element(By.CSS_SELECTOR, '#cph6')
    register(firefox, 'test@example.com', 'testing', pwd='pass', conf='conf')
    WebDriverWait(firefox, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "h6")))
    assert em_err.text == 'Invalid email'
    assert us_err.text == 'Username cannot be a valid email'
    assert pw_err.text == 'Password must be at least 8 characters'
    assert cp_err.text == 'Passwords do not match'


def test_register_firefox_whitespace(live_server, firefox: webdriver.Firefox):
    sleep(1)
    firefox.get(url_for('signup_html', _external=True))
    us_err = firefox.find_element(By.CSS_SELECTOR, '#ush6')
    register(firefox, 'Hello world', 'testing', pwd='pass', conf='conf')
    WebDriverWait(firefox, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "h6")))
    assert us_err.text == 'Username cannot contain whitespace'


def test_register_firefox_tab(live_server, firefox: webdriver.Firefox):
    sleep(1)
    firefox.get(url_for('signup_html', _external=True))
    us_err = firefox.find_element(By.CSS_SELECTOR, '#ush6')
    register(firefox, 'Hello\tworld', 'testing', pwd='pass', conf='conf')
    WebDriverWait(firefox, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "h6")))
    assert us_err.text == 'Username cannot contain whitespace'


def test_register_chrome_4errs(live_server, chrome: webdriver.Chrome):
    sleep(1)
    chrome.get(url_for('signup_html', _external=True))
    em_err = chrome.find_element(By.CSS_SELECTOR, '#emh6')
    us_err = chrome.find_element(By.CSS_SELECTOR, '#ush6')
    pw_err = chrome.find_element(By.CSS_SELECTOR, '#pwh6')
    cp_err = chrome.find_element(By.CSS_SELECTOR, '#cph6')
    register(chrome, 'test@example.com', 'testing', pwd='pass', conf='conf')
    WebDriverWait(chrome, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "h6")))
    assert em_err.text == 'Invalid email'
    assert us_err.text == 'Username cannot be a valid email'
    assert pw_err.text == 'Password must be at least 8 characters'
    assert cp_err.text == 'Passwords do not match'


def test_register_chrome_whitespace(live_server, chrome: webdriver.Chrome):
    sleep(1)
    chrome.get(url_for('signup_html', _external=True))
    us_err = chrome.find_element(By.CSS_SELECTOR, '#ush6')
    register(chrome, 'Hello world', 'testing', pwd='pass', conf='conf')
    WebDriverWait(chrome, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "h6")))
    assert us_err.text == 'Username cannot contain whitespace'



if __name__ == '__main__':
    pytest.main()
