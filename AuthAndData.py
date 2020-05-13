from hashlib import sha3_512 as sha512
from base64 import b64encode, b32encode
from datetime import datetime, timedelta
from os import urandom
from UserDataHandler import UserConversationManager
from Conversation import Conversation
import re

email_regex = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')


def isvalidemail(email):
    return bool(email_regex.match(email))


CONFIRM_PASSWD_NOMATCH = 1
PASSWD_LEN_LT8 = 2
INVALID_EMAIL = 4
EMAIL_EXISTS = 8
USERNAME_EXISTS = 16
USERNAME_IS_EMAIL = 32
USERNAME_IS_EMPTY = 64
USERNAME_CONTAINS_WHITESPACE = 128


class Authenticator:
    @staticmethod
    def _hash_pwd(passwd):
        return sha512(passwd.encode()).digest()

    def __init__(self):
        self.user_passwds = {}
        self.emails_to_users = {}
        self.users_to_emails = {}
        self.sids_times = {}
        self.sids_to_users = {}
        self.user_data = {}

    def register(self, user):
        err = 0
        passwd = user.get('password')
        confirm = user.get('confirm')
        username = user.get('username').lower().strip()
        email = user.get('email').strip()
        if passwd != confirm:
            err |= CONFIRM_PASSWD_NOMATCH
        if len(passwd) < 8:
            err |= PASSWD_LEN_LT8
        if not isvalidemail(email):
            err |= INVALID_EMAIL
        if self.emailexists(email):
            err |= EMAIL_EXISTS
        if not username:
            err |= USERNAME_IS_EMPTY
        if isvalidemail(username):
            err |= USERNAME_IS_EMAIL
        if self.userexists(username):
            err |= USERNAME_EXISTS
        if ' ' in username or '\t' in username:
            err |= USERNAME_CONTAINS_WHITESPACE
        if not err:
            self.user_passwds[username] = self._hash_pwd(passwd)
            self.users_to_emails[username] = email
            self.emails_to_users[email] = username
            self.user_data[username] = UserConversationManager(user.get('username').strip())
        return err

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
        while token in self.sids_times:  # Always ensure unique token
            token = b64encode(urandom(300)).decode()
        time = datetime.now() + timedelta(days=1)
        self.sids_times[token] = time
        self.sids_to_users[token] = user
        return token

    def sessidtouser(self, sessid):
        tok_tval = self.sids_times.get(sessid)
        if tok_tval is None:
            return False
        elif datetime.now() > tok_tval:
            del self.sids_to_users[sessid]
            del self.sids_times[sessid]
            return False
        else:
            return self.sids_to_users[sessid]

    def deauthenticate(self, sessid):
        del self.sids_to_users[sessid]
        del self.sids_times[sessid]

    def deluser(self, username):
        if username not in self.users_to_emails:
            return False
        try:
            del self.emails_to_users[self.users_to_emails[username]]
            del self.users_to_emails[username]
            del self.user_passwds[username]
        except KeyError:
            return False
        return True

    def add_conversation(self, user1, user2):
        if isvalidemail(user1):
            user1 = self.emails_to_users[user1]
        if isvalidemail(user2):
            user2 = self.emails_to_users[user2]
        id = b32encode(urandom(65)).decode()
        conversation = Conversation(id)
        self.user_data[user1].add_conversation(self.get_username(user2), conversation, id)
        self.user_data[user2].add_conversation(self.get_username(user1), conversation, id)

    def get_username(self, username):
        return self.user_data[username].user

    def user_toggle_dark_mode(self, user):
        self.user_data[user].toggledarkmode()

    def user_get_dark_mode(self, user):
        return self.user_data[user].darkmode
