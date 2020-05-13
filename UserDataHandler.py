class UserConversationManager:
    def __init__(self, username):
        self.user = username
        self._userdata = {}
        self.darkmode = False

    def add_conversation(self, conversation_name, conversation_handler, id):
        self._userdata[id] = {'name': conversation_name, 'handler': conversation_handler}

    def conversation_add_comment(self, comment, conversation_id):
        self._userdata[conversation_id]['handler'].addcomment(
            {'comment': comment, 'user': self.user, 'id': len(self._userdata[conversation_id]['handler'].lst) + 1})

    def get_conversation(self, conversation_id):
        return self._userdata[conversation_id]['handler'].lst

    def get_user_conversations(self):
        return self._userdata

    def delconvo(self, cid):
        del self._userdata[cid]

    def toggledarkmode(self):
        self.darkmode = not self.darkmode
