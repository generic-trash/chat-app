from hashlib import sha3_384 as sha384
from base64 import b64encode
from datetime import datetime, timedelta
from os import urandom


class Authenticator:
    def __init__(self):
        self.emails_to_users = {}
        self.users_to_emails = {}
        self.user_passwds = {}
        self.sids_times = {}
        self.sids_to_users = {}

    def register(self, user):
        passwd = user.get('password')
        username = user.get('username')
        email = user.get('email')
        if username in self.users_to_emails or email in self.emails_to_users or True in (
                not passwd, not username, not email):
            return False
        self.emails_to_users[email] = username
        self.users_to_emails[username] = email
        pwhash = self._hash_pwd(passwd)
        self.user_passwds[username] = pwhash
        return True

    @staticmethod
    def _hash_pwd(passwd):
        return sha384(passwd).hexdigest()

    def authenticate(self, authdata):
        passwd = authdata.get('password')
        username = authdata.get('username')
        if username not in self.users_to_emails or not passwd or not username:
            return False
        if self.user_passwds[username] != self._hash_pwd(passwd):
            return False
        else:
            return self._gen_sessionid(username)

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
        except:
            return False
        return True

    def userexists(self, user):
        return user in self.user_passwds

    def emailexists(self, email):
        return email in self.emails_to_users
