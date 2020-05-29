import unittest
from json import dumps, loads
from web import app


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()

    def test_login(self):
        self.app.post('/register', data=dumps({'username': 'test', 'email': 'test@example.com',
                                               'password': 'testpwd2', 'confirm': 'testpwd2'}))
        self.app.post('/logout')
        assert self.app.post('/login', data=dumps({'username': 'test', 'password': 'testpwd2'})).status_code == 200
        assert self.app.post('/login', data=dumps({'username': 'test', 'password': 'testpw2'})).status_code == 403
        assert self.app.post('/login',
                             data=dumps({'username': 'test@example.com', 'password': 'testpwd2'})).status_code == 200

    def test_register(self):
        assert self.app.post('/register', data=dumps({'username': 'tester', 'email': 'tester@example.com',
                                                      'password': 'testpwd2',
                                                      'confirm': 'testpwd2'})).status_code == 200
        assert self.app.post('/register', data=dumps({'username': 'test', 'email': 'test@example.com',
                                                      'password': 'tpwd2', 'confirm': 'testpw2'})).status_code == 403

    def test_darkmode(self):
        self.app.post('/login', data=dumps({'username': 'test', 'email': 'test@example.com',
                                            'password': 'testpwd2', 'confirm': 'testpwd2'}))
