import pytest
from app_fixtures import *


# from tests_app_dev import *


def test_login(app_client):
    create_user(app_client)
    assert login(app_client).status_code == 200
    assert login(app_client, pwd='test_login').status_code == 403
    assert login(app_client, 'test_login@example.com', 'test_login').status_code == 403
    assert login(app_client, 'test_login@example.com').status_code == 200


def test_register(app_client):
    assert create_user(app_client).status_code == 200  # Normal
    assert create_user(app_client, email='null@example.com').status_code == 403  # Duplicate username
    assert create_user(app_client, username='test_register2', email='null@example.com',
                       pwd='pass').status_code == 403  # Too short password
    assert create_user(app_client, username='test 1').status_code == 403  # Space in username
    assert create_user(app_client, username='test\t1').status_code == 403  # Tab in username
    assert create_user(app_client, username='new', email='test_register@example.com').status_code == 403  # Duplicate email
    assert create_user(app_client, username='test@email.com',
                       email='test_register@example.com').status_code == 403  # Username is email
    assert create_user(app_client, username='new', email='test_register').status_code == 403  # Invalid email
    assert create_user(app_client, conf='lollerbot').status_code == 403  # Passwords do not match


def test_darkmode(app_client):
    create_user(app_client)
    assert app_client.post('/darkmode').get_json()['darkmode'] is True
    assert app_client.get('/darkmode').get_json()['darkmode'] is True
    assert app_client.post('/darkmode').get_json()['darkmode'] is False
    assert app_client.get('/darkmode').get_json()['darkmode'] is False


def test_conversation(app_client):
    create_user(app_client, "test")
    create_user(app_client)
    resp = get_conversations(app_client)
    assert not resp.get_json()
    post = create_conversation(app_client, 'test')
    get = get_conversations(app_client)
    assert 'test' in post.get_json().values()
    assert post.data == get.data
    delete = delete_conversation(app_client, list(get.get_json().keys())[0])
    get = get_conversations(app_client)
    assert delete.data == get.data
    assert not delete.get_json()
    assert create_conversation(app_client, 'test2').status_code == 403


def test_delete_user(app_client):
    create_user(app_client)
    assert deluser(app_client, pwd='testingpw').status_code == 403
    assert deluser(app_client).status_code == 200
    assert login(app_client).status_code == 403


def test_change_password(app_client):
    create_user(app_client)
    assert change_password(app_client, new='password2', conf='plusword2').status_code == 403  # Confirm does not match
    assert change_password(app_client, new='pwd2').status_code == 403  # Too short password
    assert change_password(app_client, old='password2').status_code == 403  # Wrong password
    assert change_password(app_client).status_code == 200  # All ok
    logout(app_client)
    assert login(app_client).status_code == 403
    assert login(app_client, pwd='testerpw').status_code == 200


if __name__ == '__main__':
    pytest.main()
