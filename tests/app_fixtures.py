import pytest
from inspect import currentframe


def create_user(client, username=None, email=None, pwd="password", conf=None):
    if username is None:
        username = currentframe().f_back.f_code.co_name
    if conf is None:
        conf = pwd
    if email is None:
        email = username + '@example.com'
    return client.post('/register',
                       json={'username': username, 'email': email, 'password': pwd, 'confirm': conf})


def login(client, username=None, pwd='password'):
    if username is None:
        username = currentframe().f_back.f_code.co_name
    return client.post('/login', json={'username': username, 'password': pwd})


def logout(client):
    return client.post('/signout')


def create_conversation(client, username=None):
    if username is None:
        username = currentframe().f_back.f_code.co_name
    return client.post('/Conversations/new', json={'email': username})


def get_conversations(client):
    return client.get('/Conversations/getall')


def delete_conversation(client, id):
    return client.delete('/conversations/' + id)


def deluser(client, pwd='password'):
    return client.post('/deluser', json={'password': pwd})


def change_password(client, old='password', new='testerpw', conf=None):
    if conf is None:
        conf = new
    return client.post('/changepassword', json={'old': old, 'new': new, 'conf': conf})


def block_user(client, user):
    return client.post('/block', json={'user': user})
