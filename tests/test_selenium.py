from flask import url_for
import pytest
from time import sleep
from tests.selenium_functions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


def test_register_4errs(live_server, selenium: webdriver.Firefox):
    wait_for_url(selenium, url_for('signup_html', _external=True))
    em_err = selenium.find_element(By.CSS_SELECTOR, '#emh6')
    us_err = selenium.find_element(By.CSS_SELECTOR, '#ush6')
    pw_err = selenium.find_element(By.CSS_SELECTOR, '#pwh6')
    cp_err = selenium.find_element(By.CSS_SELECTOR, '#cph6')
    register(selenium, 'test@example.com', 'testing', pwd='pass', conf='conf')
    WebDriverWait(selenium, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "h6")))
    assert em_err.text == 'Invalid email'
    assert us_err.text == 'Username cannot be a valid email'
    assert pw_err.text == 'Password must be at least 8 characters'
    assert cp_err.text == 'Passwords do not match'


def test_register_whitespace(live_server, selenium: webdriver.Firefox):
    wait_for_url(selenium, url_for('signup_html', _external=True))
    us_err = selenium.find_element(By.CSS_SELECTOR, '#ush6')
    register(selenium, 'Hello world', 'testing', pwd='pass', conf='conf')
    WebDriverWait(selenium, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "h6")))
    assert us_err.text == 'Username cannot contain whitespace'


def test_register_tab(live_server, selenium: webdriver.Firefox):
    if isinstance(selenium, webdriver.Chrome):
        pytest.skip("Does not work on Chrome")
    wait_for_url(selenium, url_for('signup_html', _external=True))
    us_err = selenium.find_element(By.CSS_SELECTOR, '#ush6')
    register(selenium, 'Hello\tworld', 'testing', pwd='pass', conf='conf')
    WebDriverWait(selenium, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "h6")))
    assert us_err.text == 'Username cannot contain whitespace'


def test_register_redirect(live_server, selenium: webdriver.Firefox):
    wait_for_url(selenium, url_for('signup_html', _external=True))
    link = selenium.find_element(By.CSS_SELECTOR, 'a')
    link.click()
    assert selenium.current_url == url_for('signin_html', _external=True)


def test_signin_nonexistent_username(live_server, selenium: webdriver.Firefox):
    wait_for_url(selenium, url_for('signin_html', _external=True))
    login(selenium)
    WebDriverWait(selenium, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'h6')))


def test_signin_nonexistent_email(live_server, selenium: webdriver.Firefox):
    wait_for_url(selenium, url_for('signin_html', _external=True))
    login(selenium, user='test@example.com')
    WebDriverWait(selenium, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'h6')))


def test_signup_success(live_server, selenium: webdriver.Firefox):
    wait_for_url(selenium, url_for('signup_html', _external=True))
    register(selenium)
    selenium.execute_script("window.open('');")
    selenium.switch_to.window(selenium.window_handles[1])
    wait_for_url(selenium, url_for('home_html', _external=True))
    assert selenium.current_url == url_for('home_html', _external=True)


def test_signout(live_server, selenium: webdriver.Firefox):
    wait_for_url(selenium, url_for('signup_html', _external=True))
    register(selenium)
    selenium.execute_script("window.open('');")
    selenium.switch_to.window(selenium.window_handles[1])
    wait_for_url(selenium, url_for('home_html', _external=True))
    assert selenium.current_url == url_for('home_html', _external=True)
    selenium.find_element(By.CSS_SELECTOR, '#themetrig').click()
    WebDriverWait(selenium, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#signout')))
    selenium.find_element(By.CSS_SELECTOR, '#signout').click()
    selenium.close()
    selenium.switch_to.window(selenium.window_handles[0])
    wait_for_url(selenium, url_for('testing', _external=True))
    assert selenium.current_url == url_for('signin_html', _external=True)


def test_signin_success_username(live_server, selenium: webdriver.Firefox, pool):
    post(pool, url_for('registeruser', _external=True))
    wait_for_url(selenium, url_for('signin_html', _external=True))
    login(selenium)
    selenium.execute_script("window.open('');")
    wait_for_url(selenium, url_for('home_html', _external=True))
    assert selenium.current_url == url_for('home_html', _external=True)


def test_signin_fail(live_server, selenium: webdriver.Firefox, pool):
    post(pool, url_for('registeruser', _external=True))
    wait_for_url(selenium, url_for('signin_html', _external=True))
    login(selenium, pwd='PSSWORD')
    WebDriverWait(selenium, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h6')))


if __name__ == '__main__':
    pytest.main()
