class UserConversationManager:
    def __init__(self, username, pwd_hash, email):
        self.user = username
        self._userdata = {}
        self.darkmode = False
        self.pwd_hash = pwd_hash
        self.email = email
        self.blocklist = []

    def add_conversation(self, conversation_name, conversation_handler, id):
        self._userdata[id] = {'name': conversation_name, 'handler': conversation_handler}

    def conversation_add_comment(self, comment, conversation_id):
        self._userdata[conversation_id]['handler'].addcomment(
            {'comment': comment, 'user': self.user, 'id': len(self._userdata[conversation_id]['handler'].lst) + 1})

    def get_conversation(self, conversation_id):
        return self._userdata[conversation_id]['handler'].lst

    def get_user_conversations(self):
        data = {}
        for id, val in self._userdata.items():
            data[id] = val['name']
        return data

    def delconvo(self, cid):
        del self._userdata[cid]

    def toggledarkmode(self):
        self.darkmode = not self.darkmode

    def match_passwd(self, hash):
        return hash == self.pwd_hash

    def set_passwd(self, hash):
        self.pwd_hash = hash

    def block(self, user):
        if not self.isblocked(user):
            self.blocklist.append(user)

    def isblocked(self, user):
        return user in self.blocklist

    def unblock(self, user):
        try:
            self.blocklist.remove(user)
        except ValueError:
            pass

    def get_blocked(self):
        return self.blocklist
