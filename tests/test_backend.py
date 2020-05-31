import pytest
from app_fixtures import *


# from tests_app_dev import *


def test_login(client):
    create_user(client)
    assert login(client).status_code == 200
    assert login(client, pwd='test_login').status_code == 403
    assert login(client, 'test_login@example.com', 'test_login').status_code == 403
    assert login(client, 'test_login@example.com').status_code == 200


def test_register(client):
    assert create_user(client).status_code == 200  # Normal
    assert create_user(client, email='null@example.com').status_code == 403  # Duplicate username
    assert create_user(client, username='test_register2', email='null@example.com',
                       pwd='pass').status_code == 403  # Too short password
    assert create_user(client, username='test 1').status_code == 403  # Space in username
    assert create_user(client, username='test\t1').status_code == 403  # Tab in username
    assert create_user(client, username='new',
                       email='test_register@example.com').status_code == 403  # Duplicate email
    assert create_user(client, username='test@email.com',
                       email='test_register@example.com').status_code == 403  # Username is email
    assert create_user(client, username='new', email='test_register').status_code == 403  # Invalid email
    assert create_user(client, conf='lollerbot').status_code == 403  # Passwords do not match


def test_darkmode(client):
    create_user(client)
    assert client.post('/darkmode').get_json()['darkmode'] is True
    assert client.get('/darkmode').get_json()['darkmode'] is True
    assert client.post('/darkmode').get_json()['darkmode'] is False
    assert client.get('/darkmode').get_json()['darkmode'] is False


def test_conversation(client):
    create_user(client, "test")
    create_user(client)
    resp = get_conversations(client)
    assert not resp.get_json()
    post = create_conversation(client, 'test')
    get = get_conversations(client)
    assert 'test' in post.get_json().values()
    assert post.data == get.data
    delete = delete_conversation(client, list(get.get_json().keys())[0])
    get = get_conversations(client)
    assert delete.data == get.data
    assert not delete.get_json()
    assert create_conversation(client, 'test2').status_code == 403


def test_delete_user(client):
    create_user(client)
    assert deluser(client, pwd='testingpw').status_code == 403
    assert deluser(client).status_code == 200
    assert login(client).status_code == 403


def test_change_password(client):
    create_user(client)
    assert change_password(client, new='password2', conf='plusword2').status_code == 403  # Confirm does not match
    assert change_password(client, new='pwd2').status_code == 403  # Too short password
    assert change_password(client, old='password2').status_code == 403  # Wrong password
    assert change_password(client).status_code == 200  # All ok
    logout(client)
    assert login(client).status_code == 403
    assert login(client, pwd='testerpw').status_code == 200


if __name__ == '__main__':
    pytest.main()
