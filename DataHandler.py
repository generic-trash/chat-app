from UserDataHandler import UserConversationManager
from Conversation import Conversation


class DataHandler:
    def __init__(self):
        self._users = {}

    def adduser(self, user):
        self._users[user.lower()] = UserConversationManager(user)

    def add_conversation(self, user1, user2, name):
        conversation = Conversation()
        self._users[user1.lower()].add_conversation(name, conversation)
        self._users[user2.lower()].add_conversation(name, conversation)

    def user_conversation_add_comment(self, user, conversation, comment):
        return self._users[user.lower()].conversation_add_comment(comment, conversation)

    def user_get_conversation(self, user, conversation):
        return self._users[user.lower()].get_conversation(conversation)

    def user_get_conversation_info(self, user):
        data = self._users[user.lower()].get_user_conversations()
        data2 = {}
        for key, val in data.items():
            data2[key] = data[key]['name']
        return data2

    def user_delete_conversation(self, user, conversation):
        self._users[user.lower()].delconvo(conversation)

    def get_username(self, user):
        return self._users[user.lower()].user

    def user_toggle_dark_mode(self, user):
        self._users[user.lower()].toggledarkmode()

    def user_get_dark_mode(self, user):
        return self._users[user.lower()].darkmode
