from json import dumps, loads
import pytest
from web import app


@pytest.fixture
def client():
    with app.test_client() as app_client:
        yield app_client


def create_user(client, username, email, pwd):
    return client.post('/register',
                       data=dumps({'username': username, 'email': email, 'password': pwd, 'confirm': pwd}))


def login(client, username, pwd):
    return client.post('/login', data=dumps({'username': username, 'password': pwd}))


def test_login(client):
    create_user(client, 'test_login', 'test_login@example.com', 'password')
    assert client.post('/login', data=dumps({'username': 'test_login', 'password': 'password'})).status_code == 200
    assert client.post('/login', data=dumps({'username': 'test_login', 'password': 'testpw2'})).status_code == 403
    assert client.post('/login',
                       data=dumps({'username': 'test_login@example.com', 'password': 'password'})).status_code == 200


def test_register(client):
    client.post('/register', data=dumps({'username': 'tester', 'email': 'tester@example.com',
                                         'password': 'testpwd2',
                                         'confirm': 'testpwd2'}))
    assert client.post('/register', data=dumps({'username': 'test', 'email': 'test@example.com',
                                                'password': 'tpwd2', 'confirm': 'testpw2'})).status_code == 403


def test_darkmode(client):
    create_user(client, 'test_darkmode', 'test_darkmode@example.com', 'password')
    assert loads(client.post('/darkmode').data)['darkmode'] is True
    assert loads(client.get('/darkmode').data)['darkmode'] is True
    assert loads(client.post('/darkmode').data)['darkmode'] is True
    assert loads(client.get('/darkmode').data)['darkmode'] is False


if __name__ == '__main__':
    pytest.main()
