from hashlib import sha3_512 as sha512
from base64 import b64encode, b32encode
from os import urandom
from UserDataHandler import UserConversationManager
from Conversation import Conversation
import re

email_regex = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')


def isvalidemail(email):
    return bool(email_regex.match(email))


class Authenticator:
    @staticmethod
    def _hash_pwd(passwd):
        return sha512(passwd.encode()).digest()

    def __init__(self):
        self.user_passwds = {}
        self.emails_to_users = {}
        self.users_to_emails = {}
        self.sids_to_users = {}
        self.user_data = {}

    def register(self, user):
        error = {'confirm': None, 'password': None, 'username': None, 'email': None}
        passwd = user.get('password')
        confirm = user.get('confirm')
        username = user.get('username').lower().strip()
        email = user.get('email').strip()
        if passwd != confirm:
            error['confirm'] = "Passwords do not match"
        if len(passwd) < 8:
            error['password'] = 'Password must be at least 8 characters'
        if not isvalidemail(email):
            error['email'] = 'Invalid email'
        if self.emailexists(email):
            error['email'] = 'Email in use'
        if not username:
            error['username'] = 'Empty username'
        if isvalidemail(username):
            error['username'] = 'Username cannot be a valid email'
        if self.userexists(username):
            error['username'] = 'Username in use'
        if ' ' in username or '\t' in username:
            error['username'] = 'Username cannot contain whitespace'

        if len(set(error.values())) == 1:
            self.user_passwds[username] = self._hash_pwd(passwd)
            self.users_to_emails[username] = email
            self.emails_to_users[email] = username
            self.user_data[username] = UserConversationManager(user.get('username').strip())
            return self.authenticate(user)
        return error

    def authenticate(self, authdata):
        passwd = authdata.get('password')
        username = authdata.get('username').lower().strip()
        if self.emailexists(username):
            username = self.emails_to_users[username]
        if username not in self.users_to_emails or not passwd or not username:
            return False
        if self.user_passwds[username] != self._hash_pwd(passwd):
            return False
        else:
            return self._gen_sessionid(username)

    def emailexists(self, email):
        return email in self.emails_to_users

    def userexists(self, user):
        return user in self.users_to_emails

    def _gen_sessionid(self, user):
        token = b64encode(urandom(300)).decode()
        while token in self.sids_to_users:  # Always ensure unique token
            token = b64encode(urandom(300)).decode()
        self.sids_to_users[token] = user
        return token

    def sessidtouser(self, sessid):
        return self.sids_to_users.get(sessid)

    def deauthenticate(self, sessid):
        del self.sids_to_users[sessid]

    def deluser(self, username, pwd):
        if username not in self.user_passwds or self._hash_pwd(pwd) != self.user_passwds[username]:
            return False
        try:
            del self.emails_to_users[self.users_to_emails[username]]
            del self.users_to_emails[username]
            del self.user_passwds[username]
            del self.user_data[username]
        except KeyError:
            raise
        return True

    def add_conversation(self, user1, user2):
        try:
            if isvalidemail(user1):
                user1 = self.emails_to_users[user1]
            if isvalidemail(user2):
                user2 = self.emails_to_users[user2]
            user1 = user1.lower()
            user2 = user2.lower()
            if user1 == user2:
                return False
        except KeyError:
            return False
        id = b32encode(urandom(65)).decode()
        conversation = Conversation(id)
        try:
            self.user_data[user1].add_conversation(self.get_username(user2), conversation, id)
            self.user_data[user2].add_conversation(self.get_username(user1), conversation, id)
        except KeyError:
            return False
        return True

    def get_username(self, username):
        return self.user_data[username].user

    def user_toggle_dark_mode(self, user):
        self.user_data[user].toggledarkmode()

    def user_get_dark_mode(self, user):
        return self.user_data[user].darkmode

    def get_user_conversation_info(self, user):
        return self.user_data[user].get_user_conversations()

    def user_conversation_add_comment(self, user, conversation, comment):
        return self.user_data[user].conversation_add_comment(comment, conversation)

    def user_get_conversation(self, user, conversation):
        return self.user_data[user].get_conversation(conversation)

    def user_delete_conversation(self, user, conversation):
        self.user_data[user].delconvo(conversation)

    def changepassword(self, data):
        error = {'old': None, 'new': None, 'conf': None}
        if self._hash_pwd(data['old']) != self.user_passwds[data['username']]:
            error['old'] = 'Incorrect password'
        if data['new'] != data['conf']:
            error['conf'] = 'Passwords do not match'
        if len(data['new']) < 8:
            error['new'] = 'Password too short'
        if len(set(error.values())) == 1:
            self.user_passwds[data['username']] = self._hash_pwd(data['new'])
            return True
        else:
            return error
