from inspect import currentframe
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.errorhandler import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from json import dumps
import urllib3
import requests
from time import sleep
from selenium.webdriver.common.by import By


def clear_and_send_keys(element, keys):
    element.clear()
    element.send_keys(keys)


def register(driver, user=None, email=None, pwd='password', conf=None):
    if user is None:
        user = currentframe().f_back.f_code.co_name
    if conf is None:
        conf = pwd
    if email is None:
        email = user + '@example.com'

    username_in = driver.find_element(By.CSS_SELECTOR, '#username')
    email_in = driver.find_element(By.CSS_SELECTOR, '#email')
    pwd_in = driver.find_element(By.CSS_SELECTOR, '#password')
    conf_in = driver.find_element(By.CSS_SELECTOR, '#cpassword')
    submit = driver.find_element(By.CSS_SELECTOR, '[type=\'submit\'')
    clear_and_send_keys(username_in, user)
    clear_and_send_keys(email_in, email)
    clear_and_send_keys(pwd_in, pwd)
    clear_and_send_keys(conf_in, conf)
    submit.click()


def wait_for_url(driver, url):
    for i in range(10):
        try:
            driver.get(url)
            break
        except WebDriverException:
            sleep(3)


def login(driver, user=None, pwd='password'):
    if user is None:
        user = currentframe().f_back.f_code.co_name
    username_in = driver.find_element(By.CSS_SELECTOR, '#username')
    pwd_in = driver.find_element(By.CSS_SELECTOR, '#password')
    submit = driver.find_element(By.CSS_SELECTOR, '[type=\'submit\'')
    clear_and_send_keys(username_in, user)
    clear_and_send_keys(pwd_in, pwd)
    submit.click()


def post(pool: urllib3.PoolManager, url, user=None, email=None, pwd='password', conf=None):
    if user is None:
        user = currentframe().f_back.f_code.co_name
    if conf is None:
        conf = pwd
    if email is None:
        email = user + '@example.com'
    return pool.request('POST', url, body=dumps({'username': user, 'email': email, 'password': pwd, 'confirm': conf}))
