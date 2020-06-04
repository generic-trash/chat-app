from flask import url_for
import pytest
from time import sleep
from tests.selenium_functions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


def test_register_firefox_4errs(live_server, firefox: webdriver.Firefox):
    wait_for_url(firefox, url_for('signup_html', _external=True))
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
    wait_for_url(firefox, url_for('signup_html', _external=True))
    us_err = firefox.find_element(By.CSS_SELECTOR, '#ush6')
    register(firefox, 'Hello world', 'testing', pwd='pass', conf='conf')
    WebDriverWait(firefox, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "h6")))
    assert us_err.text == 'Username cannot contain whitespace'


def test_register_firefox_tab(live_server, firefox: webdriver.Firefox):
    wait_for_url(firefox, url_for('signup_html', _external=True))
    us_err = firefox.find_element(By.CSS_SELECTOR, '#ush6')
    register(firefox, 'Hello\tworld', 'testing', pwd='pass', conf='conf')
    WebDriverWait(firefox, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "h6")))
    assert us_err.text == 'Username cannot contain whitespace'


def test_register_chrome_4errs(live_server, chrome: webdriver.Chrome):
    wait_for_url(chrome, url_for('signup_html', _external=True))
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
    wait_for_url(chrome, url_for('signup_html', _external=True))
    us_err = chrome.find_element(By.CSS_SELECTOR, '#ush6')
    register(chrome, 'Hello world', 'testing', pwd='pass', conf='conf')
    WebDriverWait(chrome, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "h6")))
    assert us_err.text == 'Username cannot contain whitespace'


def test_register_redirect_firefox(live_server, firefox: webdriver.Firefox):
    wait_for_url(firefox, url_for('signup_html', _external=True))
    link = firefox.find_element(By.CSS_SELECTOR, 'a')
    link.click()
    assert firefox.current_url == url_for('signin_html', _external=True)


def test_register_redirect_chrome(live_server, chrome: webdriver.Chrome):
    wait_for_url(chrome, url_for('signup_html', _external=True))
    link = chrome.find_element(By.CSS_SELECTOR, 'a')
    link.click()
    assert chrome.current_url == url_for('signin_html', _external=True)


def test_signin_firefox_nonexistent_username(live_server, firefox: webdriver.Firefox):
    wait_for_url(firefox, url_for('signin_html', _external=True))
    login(firefox)
    WebDriverWait(firefox, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'h6')))


def test_signin_chrome_nonexistent_username(live_server, chrome: webdriver.Firefox):
    wait_for_url(chrome, url_for('signin_html', _external=True))
    login(chrome)
    WebDriverWait(chrome, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'h6')))


def test_signin_firefox_nonexistent_email(live_server, firefox: webdriver.Firefox):
    wait_for_url(firefox, url_for('signin_html', _external=True))
    login(firefox, user='test@example.com')
    WebDriverWait(firefox, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'h6')))


def test_signin_chrome_nonexistent_email(live_server, chrome: webdriver.Firefox):
    wait_for_url(chrome, url_for('signin_html', _external=True))
    login(chrome, user='test@example.com')
    WebDriverWait(chrome, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'h6')))


def test_signup_firefox_success(live_server, firefox: webdriver.Firefox):
    wait_for_url(firefox, url_for('signup_html', _external=True))
    register(firefox)
    firefox.execute_script("window.open('');")
    firefox.switch_to.window(firefox.window_handles[1])
    firefox.get(url_for('home_html', _external=True))
    assert firefox.current_url == url_for('home_html', _external=True)


def test_signup_chrome_success(live_server, chrome: webdriver.Firefox):
    wait_for_url(chrome, url_for('signup_html', _external=True))
    register(chrome)
    chrome.execute_script("window.open('');")
    chrome.switch_to.window(chrome.window_handles[1])
    chrome.get(url_for('home_html', _external=True))
    assert chrome.current_url == url_for('home_html', _external=True)


def test_signout_firefox(live_server, firefox: webdriver.Firefox):
    wait_for_url(firefox, url_for('signup_html', _external=True))
    register(firefox)
    firefox.execute_script("window.open('');")
    wait_for_url(firefox, url_for('home_html', _external=True))
    assert firefox.current_url == url_for('home_html', _external=True)
    firefox.find_element(By.CSS_SELECTOR, '#themetrig').click()
    firefox.find_element(By.CSS_SELECTOR, '#signout').click()
    assert firefox.current_url == url_for('signin_html', _external=True)


def test_signout_chrome(live_server, chrome: webdriver.Firefox):
    wait_for_url(chrome, url_for('signup_html', _external=True))
    register(chrome)
    chrome.execute_script("window.open('');")
    wait_for_url(chrome, url_for('home_html', _external=True))
    assert chrome.current_url == url_for('home_html', _external=True)
    chrome.find_element(By.CSS_SELECTOR, '#themetrig').click()
    chrome.find_element(By.CSS_SELECTOR, '#signout').click()
    assert chrome.current_url == url_for('signin_html', _external=True)


def test_signin_firefox_success(live_server, firefox: webdriver.Firefox):
    wait_for_url(firefox, url_for('signup_html', _external=True))
    register(firefox)
    firefox.execute_script("window.open('');")
    wait_for_url(firefox, url_for('home_html', _external=True))
    assert firefox.current_url == url_for('home_html', _external=True)
    firefox.find_element(By.CSS_SELECTOR, '#themetrig').click()
    firefox.find_element(By.CSS_SELECTOR, '#signout').click()
    assert firefox.current_url == url_for('signin_html', _external=True)
    login(firefox)
    firefox.execute_script("window.open('');")
    wait_for_url(firefox, url_for('home_html', _external=True))
    assert firefox.current_url == url_for('home_html', _external=True)


def test_signin_chrome_success(live_server, chrome: webdriver.Firefox):
    wait_for_url(chrome, url_for('signup_html', _external=True))
    register(chrome)
    chrome.execute_script("window.open('');")
    wait_for_url(chrome, url_for('home_html', _external=True))
    assert chrome.current_url == url_for('home_html', _external=True)
    chrome.find_element(By.CSS_SELECTOR, '#themetrig').click()
    chrome.find_element(By.CSS_SELECTOR, '#signout').click()
    assert chrome.current_url == url_for('signin_html', _external=True)
    login(chrome)
    chrome.execute_script("window.open('');")
    wait_for_url(chrome, url_for('home_html', _external=True))
    assert chrome.current_url == url_for('home_html', _external=True)



if __name__ == '__main__':
    pytest.main()
